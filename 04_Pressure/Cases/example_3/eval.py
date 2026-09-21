#!/usr/bin/env python3
"""Compare the five pressure solvers on Example 3.

Usage:
    python eval.py [WHAT] [--dir DIR]

WHAT is one of:
    flow        volume flow in and out of the duct, one figure for the local
                solvers and one for the global ones (default)
    iterations  pressure iterations per step, and the velocity error they leave
    cost        wall clock time against simulation time
    all         all of the above

Unlike Example 1, which plots one run at a time, every figure here overlays the
variants side by side -- the point of the exercise is the comparison, not any
single run. Whichever variants are present get plotted and the rest are named
as missing, so the figures are worth looking at after the first run and not
only after all five.

DIR defaults to 'results', where FDS writes when you run the case yourself, and
falls back to 'reference' when you have not. Pass --dir explicitly to force one.

Almost everything comes out of <run>_devc.csv, which the &DEVC lines in the
input fill: in_net and out_net across the two ends of the duct, error for the
largest velocity error left in the domain, and iter for the pressure iterations
the step took. Only the wall clock figure needs a second file, <run>_steps.csv,
which FDS timestamps each reported step in.
"""
import argparse
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

CHID = "Example_3"

# The five &PRES lines in Example_3.fds, in the order the slide lists them, with
# the label and colour each keeps across all three figures.
VARIANTS = [
    ("FFT",       "FFT",       "#1f77b4"),
    ("ULMAT",     "ULMAT",     "#2ca02c"),
    ("FFT_tight", "FFT Tight", "#d62728"),
    ("GLMAT",     "GLMAT",     "#9467bd"),
    ("UGLMAT",    "UGLMAT",    "#ff7f0e"),
]
# The deck splits the volume flow figure in two: solvers that work mesh by mesh,
# and solvers that build one matrix for the whole domain. Keeping that split
# matters because the two groups differ by orders of magnitude -- on one axis
# the global solvers' curves would lie on top of each other.
LOCAL = ("FFT", "ULMAT", "FFT_tight")
GLOBAL = ("GLMAT", "UGLMAT")

STEADY_FROM = 30.0      # seconds; half the run, well past the starting transient

# The inflow both flow figures are drawn against, taken from this run.
#
# It has to come from one run rather than from the &HVAC fan's nominal 1 m3/s,
# because FDS ramps the fan up over the first couple of seconds and the curves
# have to be comparable there too. It has to be UGLMAT's, because the inlet
# measurement is not solver-independent: GLMAT reads 0.9871 to 1.0067 at the fan
# face and FFT 0.9910 to 1.0054, since they leave velocity error there as well
# as at the duct walls. UGLMAT holds 0.999902 to 1.000000, ramp included, so its
# inlet device is the fan's prescribed flow to within a rounding error -- the
# theoretical inflow, not one solver's opinion of it.
REFERENCE = "UGLMAT"
FAN_FLOW = 1.0      # &HVAC VOLUME_FLOW, the fallback when UGLMAT has not been run

# The iteration axis is fixed, not autoscaled, and this is the window the slide
# uses. FFT Tight hits its MAX_PRESSURE_ITERATIONS cap of 1000 in the first
# couple of seconds; letting those spikes set the scale squashes the 50-300 band
# they settle into -- and every other solver's 1-2 iterations -- onto the axis.
# The clipped spikes are the point being made either way, so they can run off
# the top. Raise it if you run with a larger cap.
ITER_YLIM = (0, 500)



def pick_dir(here, explicit):
    """Where to read run output from.

    Defaults to the student's own runs in 'results/', and falls back to the
    reference runs shipped with the class when there are none. The fallback is
    per directory, not per file: mixing a fresh FFT run with a reference GLMAT
    would compare two different machines and quietly misstate the cost figure.
    """
    if explicit:
        return os.path.join(here, explicit), explicit
    results = os.path.join(here, "results")
    ran = os.path.isdir(results) and any(
        f.endswith("_devc.csv") for f in os.listdir(results))
    if ran:
        return results, "results"
    reference = os.path.join(here, "reference")
    if os.path.isdir(reference):
        print("no runs in results/, using the reference runs")
        return reference, "reference"
    return results, "results"


def read(where, variant, kind):
    """One run's CSV, or None when that variant has not been run.

    FDS writes a units line above the header in these files, so the header is
    the second row.
    """
    path = os.path.join(where, "%s_%s_%s.csv" % (CHID, variant, kind))
    if not os.path.exists(path):
        return None
    try:
        frame = pd.read_csv(path, skiprows=1)
    except pd.errors.EmptyDataError:
        return None
    # A run still in flight has written the header and nothing else. Treat that
    # as not run rather than crashing halfway through a figure.
    return frame if not frame.empty else None


def present(where, kind):
    """The variants that have this kind of file, and the ones that do not."""
    have, missing = [], []
    for name, label, colour in VARIANTS:
        (have if read(where, name, kind) is not None else missing).append(
            (name, label, colour))
    return have, missing


def note_missing(missing, kind):
    if missing:
        print("not plotted (no %s file yet): %s"
              % (kind, ", ".join(label for _, label, _ in missing)))


SVG = False     # set by --svg; the slide assets are SVG, the case ships PDF


def save(fig, here, name):
    plots = os.path.join(here, "plots")
    os.makedirs(plots, exist_ok=True)
    for ext in ("pdf", "svg") if SVG else ("pdf",):
        out = os.path.join(plots, "%s_%s.%s" % (CHID, name, ext))
        fig.savefig(out, bbox_inches="tight")
        print("wrote %s" % out)


def flow(where, here):
    """Volume flow in and out, local solvers and global solvers separately.

    The fan puts 1 m3/s into the duct and the far end is the only way out of it,
    so the two should agree. What separates them is volume the solver lets
    through the duct walls, which the open domain boundaries then carry away --
    seal those and the two agree whatever happens at the walls.

    The inflow drawn against them is UGLMAT's, for the reason given at
    REFERENCE above.

    in_net and out_net, not the verification case's flow_in and flow_out: those
    two integrate one sign of the velocity only, so a vortex drawing air back
    into the duct mouth is dropped from the integral and reads as flow leaving.
    On UGLMAT that shows up as a 2 % bump on a solver whose net error is 1e-13.
    """
    have, missing = present(where, "devc")
    note_missing(missing, "devc")
    if not have:
        return
    # One y axis for both halves. They sit side by side on the slide, and the
    # whole point is how much further the local solvers and GLMAT wander from
    # the fan's 1 m3/s than UGLMAT does -- which a reader cannot see if each
    # half is scaled to its own worst excursion.
    top = max(read(where, n, "devc")["out_net"].max() for n, _, _ in have)
    ylim = (0.0, max(1.7, top * 1.05))
    ref = read(where, REFERENCE, "devc")
    if ref is None:
        print("%s has not been run, so the inflow line falls back to the fan's "
              "nominal %g m3/s and will not show its ramp" % (REFERENCE, FAN_FLOW))
    for group, title in ((LOCAL, "local"), (GLOBAL, "global")):
        rows = [(n, l, c) for n, l, c in have if n in group]
        if not rows:
            continue
        fig, ax = plt.subplots()
        for name, label, colour in rows:
            devc = read(where, name, "devc")
            ax.plot(devc["Time"], devc["out_net"], color=colour,
                    label="out %s" % label)
            steady = devc[devc["Time"] >= STEADY_FROM]
            if not steady.empty:
                gap = steady["out_net"] - steady["in_net"]
                worst = gap[gap.abs().idxmax()]
                print("%-10s worst in-out volume flow difference past %gs: "
                      "%+.3g %%" % (label, STEADY_FROM,
                                    100.0 * worst / steady["in_net"].max()))
        # Drawn last and dashed, so a solver that tracks it exactly shows through
        # the gaps instead of hiding under it. Black, not red: FFT Tight is red
        # and hugs this line for the whole run.
        if ref is not None:
            ax.plot(ref["Time"], ref["in_net"], "k--", linewidth=1.6,
                    zorder=10, label="in")
        else:
            ax.axhline(FAN_FLOW, color="black", linestyle="--", linewidth=1.6,
                       zorder=10, label="in (fan, %g m$^3$/s)" % FAN_FLOW)
        ax.set_xlabel("Time [s]")
        ax.set_ylabel(r"Volume Flow [m$^3$/s]")
        ax.set_xlim(0, devc["Time"].iloc[-1])
        ax.set_ylim(*ylim)
        ax.grid(True)
        ax.legend(loc="lower right")
        save(fig, here, "flow_%s" % title)
        plt.close(fig)


def iterations(where, here):
    """Iterations per step and the velocity error each solver settles for.

    Side by side rather than on two y axes, as on the slide: these are the two
    halves of the same trade. FFT stops at its iteration cap and leaves an
    error behind, the same FFT with a tighter tolerance buys orders of magnitude
    off that error with hundreds of iterations, and UGLMAT reaches machine
    precision in one. Sixteen decades of velocity error need a log axis, which
    a shared axis with a count on it cannot give.
    """
    have, missing = present(where, "devc")
    note_missing(missing, "devc")
    if not have:
        return
    # 9 x 6.5 is the 4:3-ish frame the slide holds, two tall panels side by
    # side rather than two wide ones.
    fig, (left, right) = plt.subplots(1, 2, figsize=(9, 6.5))
    for name, label, colour in have:
        devc = read(where, name, "devc")
        left.plot(devc["Time"], devc["iter"], color=colour, label=label,
                  linewidth=1)
        right.plot(devc["Time"], devc["error"], color=colour, linewidth=1)
        steady = devc[devc["Time"] >= STEADY_FROM]
        print("%-10s %4d iterations at most, %5.1f on average past %gs; "
              "velocity error there %.2g m/s"
              % (label, devc["iter"].max(), steady["iter"].mean(), STEADY_FROM,
                 steady["error"].max()))
    for ax, ylabel in ((left, "Iterations"),
                       (right, "Max Velocity Error [m/s]")):
        ax.set_xlabel("Simulation Time [s]")
        ax.set_ylabel(ylabel)
        ax.set_xlim(0, devc["Time"].iloc[-1])
        ax.grid(True)
    left.set_ylim(*ITER_YLIM)
    right.set_yscale("log")
    left.legend(loc="upper right")
    fig.tight_layout()
    save(fig, here, "iterations")
    plt.close(fig)


def cost(where, here):
    """Wall clock time against simulation time.

    _steps.csv timestamps each reported step, so the elapsed time is measured
    from the first one. FDS reports every step for the first ten and then thins
    out, which is the right way round here: the early steps are where the
    solvers differ most. The reference runs were made one after another on an
    idle machine, because a second job on the same cores would show up in this
    figure as solver cost.
    """
    have, missing = present(where, "steps")
    note_missing(missing, "steps")
    if not have:
        return
    fig, ax = plt.subplots()
    for name, label, colour in have:
        steps = read(where, name, "steps")
        wall = pd.to_datetime(steps["Wall Time"], format="ISO8601")
        elapsed = (wall - wall.iloc[0]).dt.total_seconds()
        ax.plot(steps["Simulation Time"], elapsed, color=colour, label=label)
        print("%-10s %.0f s of wall clock for %g s of simulation"
              % (label, elapsed.iloc[-1], steps["Simulation Time"].iloc[-1]))
    ax.set_xlabel("Simulation Time [s]")
    ax.set_ylabel("Wall Time [s]")
    ax.grid(True)
    ax.legend(loc="upper left")
    save(fig, here, "cost")
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", nargs="?", default="flow",
                    choices=("flow", "iterations", "cost", "all"))
    ap.add_argument("--dir", default=None,
                    help="directory holding the run output; default is results/, "
                         "falling back to reference/ when you have not run the case")
    ap.add_argument("--svg", action="store_true",
                    help="also write SVG copies; this is how the figures in the "
                         "slides' Section_3_assets are made")
    a = ap.parse_args()

    global SVG
    SVG = a.svg

    here = os.path.dirname(os.path.abspath(__file__))
    where, _ = pick_dir(here, a.dir)
    if not os.path.isdir(where):
        sys.exit("no such directory: %s" % where)

    for name, fn in (("flow", flow), ("iterations", iterations), ("cost", cost)):
        if a.what in (name, "all"):
            fn(where, here)


if __name__ == "__main__":
    main()
