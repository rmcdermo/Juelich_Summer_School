#!/usr/bin/env python3
"""Compare the three pressure solver settings on Example 5.

Usage:
    python eval.py [WHAT] [--dir DIR] [--step N] [--svg]

WHAT is one of:
    iterations  pressure iterations against time, log scale (default)
    cost        wall clock time against simulated time
    error       velocity error against pressure iteration, within one time
                step -- one panel per variant
    all         all three
    slice       cut the one time step the error figure needs out of each
                _pressit.csv and write it beside them, so the full files do
                not have to be carried anywhere

Every figure overlays the three runs; whichever are present get plotted and the
rest are named as missing. DIR defaults to 'results', where FDS writes when you
run the case yourself, and falls back to 'reference' when you have not.

Two files per run carry everything:

    <run>_devc.csv      iter, error and cputime, one row per output interval --
                        the three &DEVC lines at the end of each input. This is
                        the whole of the iterations and cost figures.
    <run>_pressit.csv   one row per pressure iteration rather than per time
                        step, written because each input asks &DUMP for
                        VELOCITY_ERROR_FILE. This is the whole of the error
                        figure. FDS 6.10 and earlier called it _vel_err.csv.

Nothing else from a run is needed to redraw the slides, which matters because
the plain FFT variant is a couple of hours on eight cores: bring those two
files back per variant and the figures can be made anywhere.
"""
import argparse
import glob
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

CHID = "Example_5"

# The velocity tolerance the FFT variants are asked for, in m/s. It is the line
# the iteration loop is trying to get under, so the error figure draws it.
VELOCITY_TOLERANCE = 0.001

# The window the error figure's panels share. The deck's own is the first:
# six decades, which is all the FFT variants need. A global solver leaves
# machine zero instead, so as soon as one of those is in the figure the floor
# has to come down to make room for it.
ERROR_YLIM = (1e-4, 1e2)
ERROR_YLIM_EXACT = (1e-15, 1e2)

# The three inputs, with the label and colour each keeps across every figure.
# Red dashed FFT, blue TP and black UGLMAT are the deck's own, so a figure made
# here drops into the slide it replaces without the legend changing under the
# reader.
VARIANTS = [
    ("FFT",          "FFT",               "#ff0000", "--"),
    ("FFT_TP",       "FFT with TP",       "#0000ff", "-"),
    ("UGLMAT",       "UGLMAT",            "#000000", "-"),
]

SVG = False     # set by --svg; the slide assets are SVG, the case ships PDF


def pick_dir(here, explicit):
    """Where to read run output from: your own runs, else the shipped ones."""
    if explicit:
        return os.path.join(here, explicit)
    results = os.path.join(here, "results")
    ran = os.path.isdir(results) and any(
        f.endswith("_devc.csv") for f in os.listdir(results))
    if ran:
        return results
    reference = os.path.join(here, "reference")
    if os.path.isdir(reference):
        print("no runs in results/, using the reference runs")
        return reference
    return results


def read(where, variant, kind):
    """One run's CSV, or None when that variant has not been run.

    _devc.csv carries a units line above the header, so its header is the
    second row; _pressit.csv does not.
    """
    path = os.path.join(where, "%s_%s_%s.csv" % (CHID, variant, kind))
    if not os.path.exists(path) and kind == "pressit":
        # A full _pressit.csv for the plain FFT run is 2000 iterations a half
        # step for the length of the run -- upwards of a gigabyte, which is not
        # something to carry back from a cluster or keep in git. `eval.py slice`
        # cuts out the single time step the figure draws, and that is what
        # reference/ ships.
        cut = glob.glob(os.path.join(
            where, "%s_%s_pressit_step*.csv" % (CHID, variant)))
        if not cut:
            return None
        path = sorted(cut)[-1]
    if not os.path.exists(path):
        return None
    try:
        frame = pd.read_csv(path, skiprows=1 if kind == "devc" else 0)
    except pd.errors.EmptyDataError:
        return None
    frame.columns = [c.strip() for c in frame.columns]
    # A run still in flight has written the header and nothing else.
    return frame if not frame.empty else None


def present(where, kind, only=None):
    have, missing = [], []
    for row in VARIANTS:
        if only and row[0] not in only:
            continue
        (have if read(where, row[0], kind) is not None else missing).append(row)
    if missing:
        print("not plotted (no %s file yet): %s"
              % (kind, ", ".join(r[1] for r in missing)))
    return have


def end_time(where, have):
    """The latest simulated time any of the plotted runs reached."""
    return max(read(where, n, "devc")["Time"].iloc[-1] for n, _l, _c, _s in have)


def save(fig, here, name):
    plots = os.path.join(here, "plots")
    os.makedirs(plots, exist_ok=True)
    for ext in ("pdf", "svg") if SVG else ("pdf",):
        out = os.path.join(plots, "%s_%s.%s" % (CHID, name, ext))
        fig.savefig(out, bbox_inches="tight")
        print("wrote %s" % out)


def iterations(where, here, only=None):
    """Pressure iterations against time, log scale.

    The figure the tunnel preconditioner slide is built on. Plain FFT sits on
    its MAX_PRESSURE_ITERATIONS=2000 cap for the whole run, which means the
    velocity tolerance is never reached; the same solver with the tunnel
    preconditioner reaches it in a few dozen.

    The count is a time average: &DEVC defaults to TIME_AVERAGED=.TRUE., so a
    step that took 3 iterations and one that took 4 read as 3.5 between them.
    """
    have = present(where, "devc", only)
    if not have:
        return
    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    for name, label, colour, style in have:
        devc = read(where, name, "devc")
        ax.plot(devc["Time"], devc["iter"], color=colour, linestyle=style,
                linewidth=2, label=label)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Iterations")
    ax.set_yscale("log")
    # The longest run sets the axis, not whichever happened to be drawn last.
    # A variant that went unstable stops partway, and its curve ending early is
    # the thing to see -- so the window has to be wide enough to show that it
    # ended early rather than cropping everyone else down to it.
    ax.set_xlim(0, end_time(where, have))
    ax.grid(True)
    # Pinned top right, over the FFT band, which is where the deck put it. Left
    # to place itself matplotlib drops it bottom right, on top of the UGLMAT
    # curve; an opaque frame over the noisy red band costs less than that.
    ax.legend(loc="upper right", framealpha=1.0)
    fig.tight_layout()
    save(fig, here, "iterations")
    plt.close(fig)


def cost(where, here, only=None):
    """Wall clock time against simulated time.

    cputime is FDS's CPU TIME device: seconds of processor time for the rank
    that wrote it, which is the run's wall clock when every rank owns a core.
    Divided by 60 here, so this axis really is in minutes -- unlike the same
    figure for Example 4, where the deck's [min] label sits over seconds.
    """
    have = present(where, "devc", only)
    if not have:
        return
    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    for name, label, colour, style in have:
        devc = read(where, name, "devc")
        ax.plot(devc["Time"], devc["cputime"] / 60.0, color=colour,
                linestyle=style, linewidth=2, label=label)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Wall Time [min]")
    ax.set_xlim(0, end_time(where, have))
    ax.grid(True)
    # Every curve rises from the origin, so the top left corner is the empty one.
    ax.legend(loc="upper left", framealpha=1.0)
    fig.tight_layout()
    save(fig, here, "wall_time")
    plt.close(fig)


def blocks(pressit):
    """Split the file into pressure loops.

    FDS restarts the Iteration column at 1 every time it enters the pressure
    loop, so a drop in that column is a loop boundary. The loops do not come
    two per time step: when CHECK_STABILITY rejects a predictor the step is
    retaken with a smaller dt, and the rejected attempt is in the file too --
    which is why an early step here usually holds three loops, not two.
    """
    start = (pressit["Iteration"]
             <= pressit["Iteration"].shift(fill_value=1 << 30))
    return [b for _, b in pressit.groupby(start.cumsum(), sort=False)]


def halves(pressit, step):
    """The accepted predictor and corrector of one time step.

    Every row carries the time at which it was written, and inside a step that
    takes exactly two values: the predictor advances the clock, so its rows
    carry the time the step started and the corrector's the time it ended. Any
    rejected attempt shares a time stamp with the attempt that replaced it, so
    the one that counts is the last loop at each of the two times.
    """
    rows = pressit[pressit["Time Step"] == step]
    out = []
    for _, at_time in rows.groupby("Time", sort=True):
        out.append(blocks(at_time)[-1])
    return out


def clean_step(pressit):
    """The last time step FDS took without rejecting and retaking a half of it.

    Two loops in the file means a predictor and a corrector and nothing thrown
    away, which is what an ordinary step looks like once the run has settled --
    and what the figure should be showing.
    """
    counts = {}
    for b in blocks(pressit):
        step = int(b["Time Step"].iloc[0])
        counts[step] = counts.get(step, 0) + 1
    clean = [s for s, n in counts.items() if n == 2]
    return max(clean) if clean else int(pressit["Time Step"].max())


def error(where, here, step, only=None):
    """Velocity error against pressure iteration, inside one time step.

    One panel per variant, each with its own x axis, because the whole point is
    how far apart the counts are: plain FFT walks its 2000 iteration cap twice
    without crossing the tolerance, and the preconditioned run crosses it in a
    few dozen. Those two are what the slide shows -- pass
    --variants FFT,FFT_TP for exactly that figure. The comparison is between a
    solver and the same solver preconditioned, so a global solver in the same
    frame would be answering a different question; what UGLMAT costs belongs in
    the iterations and cost figures.

    The panels are split at the predictor/corrector boundary and the tolerance
    is drawn across them, as on the slide.
    """
    have = present(where, "pressit", only)
    if not have:
        return
    exact = any(read(where, n, "pressit")["Velocity Error"].min() < 1e-10
                for n, _l, _c, _s in have)
    ylim = ERROR_YLIM_EXACT if exact else ERROR_YLIM
    fig, axes = plt.subplots(1, len(have), figsize=(5.0 * len(have), 4.6),
                             squeeze=False)
    for ax, (name, label, colour, style) in zip(axes[0], have):
        pressit = read(where, name, "pressit")
        want = step if step is not None else clean_step(pressit)
        stages = halves(pressit, want)
        if not stages:
            ax.set_title("%s -- no time step %d" % (label, want))
            continue
        n = 0
        for half, tag in zip(stages, ("Predictor", "Corrector")):
            x = range(n + 1, n + 1 + len(half))
            ax.plot(x, half["Velocity Error"], color=colour, linestyle=style,
                    linewidth=1.4, marker="." if len(half) < 40 else None)
            middle = n + 1 + (len(half) - 1) / 2.0
            ax.annotate(tag, xy=(middle, 1.0), xycoords=("data", "axes fraction"),
                        xytext=(0, -14), textcoords="offset points",
                        ha="center", fontsize=9)
            n += len(half)
            if half is not stages[-1]:
                ax.axvline(n + 0.5, color="#808080", linewidth=0.8)
        ax.axhline(VELOCITY_TOLERANCE, color="#ff0000", linewidth=1.2)
        ax.annotate("VELOCITY_TOLERANCE %g m/s" % VELOCITY_TOLERANCE,
                    xy=(0.02, VELOCITY_TOLERANCE), xycoords=("axes fraction", "data"),
                    xytext=(0, -11), textcoords="offset points",
                    color="#ff0000", fontsize=8)
        ax.set_yscale("log")
        # The same y range in every panel, so they are read against each other
        # rather than each against itself.
        ax.set_ylim(*ylim)
        ax.set_xlim(0.5, n + 0.5)
        # The deck's own axis label, which carries the step number, and its
        # variant name above the panel -- in the variant's colour rather than
        # the deck's red, so four panels stay tellable apart.
        ax.set_xlabel("Time Step %d, Pressure iterations" % want)
        ax.set_ylabel("Velocity Error [m/s]")
        ax.set_title(label, fontsize=11, color=colour)
        ax.grid(True)
        print("%-19s step %d: %s iterations, error %.2e -> %.2e m/s"
              % (label, want, " + ".join(str(len(h)) for h in stages),
                 stages[0]["Velocity Error"].iloc[0],
                 stages[-1]["Velocity Error"].iloc[-1]))
    fig.tight_layout()
    save(fig, here, "velocity_error")
    plt.close(fig)


def slice_pressit(where, step):
    """Cut one time step out of each _pressit.csv and write it beside them.

    The error figure needs one time step. The file it comes from holds every
    pressure iteration of the whole run, which for the plain FFT variant is
    2000 a half step and around a gigabyte -- too big to bring back from a
    cluster and far too big for git. This writes
    <run>_pressit_step<N>.csv, a few hundred kilobytes, and `read` picks it up
    when the full file is absent, so reference/ can ship the slice alone.

    Run it in the directory the run output is in, before copying anything.
    """
    for name, label, _c, _s in VARIANTS:
        pressit = read(where, name, "pressit")
        if pressit is None:
            continue
        want = step if step is not None else clean_step(pressit)
        rows = pressit[pressit["Time Step"] == want]
        if rows.empty:
            print("%-19s has no time step %d" % (label, want))
            continue
        out = os.path.join(where, "%s_%s_pressit_step%d.csv"
                           % (CHID, name, want))
        rows.to_csv(out, index=False)
        print("wrote %s  (%d rows)" % (out, len(rows)))


def summary(where):
    """One line per run: what it cost and what it bought.

    The averaging window is the same for every run -- the second half of the
    longest one -- rather than each run's own second half, or a run that
    stopped early would be averaged over a different part of the flow and
    silently compared against the others on unequal terms. A run that did not
    reach the end says so, and says where it got to.
    """
    have = [v for v in VARIANTS if read(where, v[0], "devc") is not None]
    if not have:
        return
    last = end_time(where, have)
    print("averaged over %.1f to %.1f s:" % (last / 2.0, last))
    for name, label, _c, _s in have:
        devc = read(where, name, "devc")
        reached = devc["Time"].iloc[-1]
        steady = devc[devc["Time"] >= last / 2.0]
        window = ("%8.1f iterations, velocity error %.2e m/s"
                  % (steady["iter"].mean(), steady["error"].mean())
                  if not steady.empty else "%40s" % "never reached that window")
        note = "" if reached >= last - 1e-6 else "  STOPPED at %.2f s" % reached
        print("%-19s %s, %7.1f min%s"
              % (label, window, devc["cputime"].iloc[-1] / 60.0, note))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", nargs="?", default="iterations",
                    choices=("iterations", "cost", "error", "all", "slice"))
    ap.add_argument("--dir", default=None,
                    help="directory holding the run output; default is results/, "
                         "falling back to reference/ when you have not run the case")
    ap.add_argument("--step", type=int, default=None,
                    help="which time step the error figure takes apart; "
                         "default is the last one FDS did not have to retake")
    ap.add_argument("--variants", default=None,
                    help="comma separated variant names to plot, e.g. "
                         "FFT,FFT_TP for the error figure's two panel version; "
                         "default is every variant that has been run")
    ap.add_argument("--svg", action="store_true",
                    help="also write SVG copies; this is how the figures in the "
                         "slides' Section_4_assets are made")
    a = ap.parse_args()

    global SVG
    SVG = a.svg

    here = os.path.dirname(os.path.abspath(__file__))
    where = pick_dir(here, a.dir)
    if not os.path.isdir(where):
        sys.exit("no such directory: %s" % where)

    if a.what == "slice":
        slice_pressit(where, a.step)
        return
    only = a.variants.split(",") if a.variants else None
    if a.what in ("iterations", "all"):
        iterations(where, here, only)
    if a.what in ("cost", "all"):
        cost(where, here, only)
    if a.what in ("error", "all"):
        error(where, here, a.step, only)
    if a.what == "all":
        summary(where)


if __name__ == "__main__":
    main()
