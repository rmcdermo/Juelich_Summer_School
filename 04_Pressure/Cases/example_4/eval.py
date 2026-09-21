#!/usr/bin/env python3
"""Compare the five pressure solvers on Example 4.

Usage:
    python eval.py [WHAT] [--dir DIR] [--height Z] [--svg]

WHAT is one of:
    solvers     pressure iterations, the velocity error they leave, and the
                cost of each -- the three panels on the slide (default)
    profiles    vertical and radial velocity across the plume, against the
                Sandia Test 14 measurements
    all         both

Every figure overlays the five runs; whichever are present get plotted and the
rest are named as missing. DIR defaults to 'results', where FDS writes when you
run the case yourself, and falls back to 'reference' when you have not.

Two files per run carry everything:

    <run>_devc.csv   iter, error and cputime, one row per output interval --
                     the three &DEVC lines at the end of each input. This is
                     the whole of the solvers figure.
    <run>_line.csv   the radial profiles: Wp3/Wp5/Wp9 and Up3/Up5/Up9, each a
                     32 point line across the plume, time averaged from 10 s.
                     This is the whole of the profiles figure.

Nothing else from a run is needed to redraw the slides, which matters because
these are 16 process runs that belong on a cluster: bring those two files back
per variant and the figures can be made anywhere.

The measurements in experimental/ are Sandia's, not ours, and are read from
there whichever run directory is in use.
"""
import argparse
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator

CHID = "Example_4"

# The five inputs, with the label and colour each keeps across both figures.
# The colours are the deck's, so a figure made here drops into the slide it
# replaces without the legend changing under the reader.
VARIANTS = [
    ("FFT",             "FFT",             "#ff0000", "--"),
    ("FFT_tight",       "FFT tight",       "#0000ff", "-"),
    ("ULMAT",           "ULMAT",           "#000000", "-"),
    ("UGLMAT_PARDISO",  "UGLMAT PARDISO",  "#00c000", "-"),
    ("UGLMAT_HYPRE",    "UGLMAT HYPRE",    "#ff00ff", "-"),
]

# The line devices are named for the height they sit at: Wp5 is vertical
# velocity at z = 0.5 m, Up3 radial velocity at z = 0.3 m, and so on.
HEIGHTS = {0.3: "p3", 0.5: "p5", 0.9: "p9"}

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
    # A run still in flight has written the header and nothing else.
    return frame if not frame.empty else None


def present(where, kind):
    have, missing = [], []
    for row in VARIANTS:
        (have if read(where, row[0], kind) is not None else missing).append(row)
    if missing:
        print("not plotted (no %s file yet): %s"
              % (kind, ", ".join(r[1] for r in missing)))
    return have


def save(fig, here, name):
    plots = os.path.join(here, "plots")
    os.makedirs(plots, exist_ok=True)
    for ext in ("pdf", "svg") if SVG else ("pdf",):
        out = os.path.join(plots, "%s_%s.%s" % (CHID, name, ext))
        fig.savefig(out, bbox_inches="tight")
        print("wrote %s" % out)


def solvers(where, here):
    """Iterations, velocity error and cost, side by side.

    The three together are the trade the slide is about: FFT stops at its
    iteration cap and lives with the error, the same FFT with a tolerance of
    1e-4 spends a hundred-odd iterations a step buying that error down, and the
    global solvers reach it in two or three -- for which UGLMAT with the direct
    PARDISO backend pays eight times FFT's wall clock.

    cputime is FDS's CPU TIME device: seconds of processor time for the rank
    that wrote it, which is the run's wall clock when every rank owns a core,
    as it does on a cluster. Seconds, despite the axis on the slide this
    replaces being labelled minutes.
    """
    have = present(where, "devc")
    if not have:
        return
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))
    # Fixed windows, the slide's own. The error axis stops at 1e-15 because the
    # two global solvers leave exactly zero, which a log axis cannot place: they
    # drop off the bottom rather than being scaled to.
    # The floors sit a little below the lowest curve rather than on it: both
    # UGLMAT runs are capped at one iteration and leave error at 1.7e-15, so an
    # axis starting at exactly 1 and 1e-15 draws them half outside the frame.
    panels = (("iter", "Iterations", True, (0.8, 1e3)),
              ("error", "Max Velocity Error [m/s]", True, (1e-16, 1e0)),
              ("cputime", "CPU Time [s]", False, None))
    for ax, (column, ylabel, log, ylim) in zip(axes, panels):
        for name, label, colour, style in have:
            devc = read(where, name, "devc")
            ax.plot(devc["Time"], devc[column], color=colour, linestyle=style,
                    linewidth=1.2, label=label)
        ax.set_xlabel("Time [s]")
        ax.set_ylabel(ylabel)
        ax.set_xlim(0, devc["Time"].iloc[-1])
        ax.xaxis.set_major_locator(MultipleLocator(5))
        if log:
            ax.set_yscale("log")
        if ylim:
            ax.set_ylim(*ylim)
        ax.grid(True)
    axes[0].legend(loc="upper right", fontsize=8)
    for name, label, colour, style in have:
        devc = read(where, name, "devc")
        steady = devc[devc["Time"] >= 10.0]
        print("%-15s %6.1f iterations on average past 10s, velocity error "
              "%.1e m/s, %8.0f s of CPU time (%.1f h)"
              % (label, steady["iter"].mean(), steady["error"].mean(),
                 devc["cputime"].iloc[-1], devc["cputime"].iloc[-1] / 3600))
    fig.tight_layout()
    save(fig, here, "solvers")
    plt.close(fig)


def profiles(where, here, z):
    """Vertical and radial velocity across the plume, against the measurements.

    Time averaged from 10 s on, which is what the &DEVC lines ask FDS for, so
    these are mean profiles rather than an instant. The point of the figure is
    that the five curves sit on top of each other: the solvers disagree by
    orders of magnitude on the error they leave behind and by a factor of eight
    on cost, and predict the same flow.
    """
    have = present(where, "line")
    if not have:
        return
    tag = HEIGHTS[z]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    panels = (("W", "Vertical Velocity [m/s]"),
              ("U", "Radial Velocity [m/s]"))
    for ax, (q, ylabel) in zip(axes, panels):
        for name, label, colour, style in have:
            line = read(where, name, "line")
            ax.plot(line["x"], line["%s%s" % (q, tag)], color=colour,
                    linestyle=style, linewidth=1.4, label=label)
        exp = os.path.join(here, "experimental",
                           "Sandia_CH4_1m_Test14_%s_z%s.csv" % (q, tag))
        if os.path.exists(exp):
            e = pd.read_csv(exp)
            ax.plot(e["x"], e["vel"], "--", color="#808080", linewidth=1.8,
                    label="Sandia Test 14")
        ax.set_xlabel("Radial Position [m]")
        ax.set_ylabel(ylabel)
        ax.grid(True)
    axes[1].legend(loc="upper right", fontsize=8)
    # No title: the height is in the file name, the axes say what the curves
    # are, and on the slide it would repeat the line of text above the figure.
    fig.tight_layout()
    save(fig, here, "profiles_z%s" % tag)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", nargs="?", default="solvers",
                    choices=("solvers", "profiles", "all"))
    ap.add_argument("--dir", default=None,
                    help="directory holding the run output; default is results/, "
                         "falling back to reference/ when you have not run the case")
    ap.add_argument("--height", type=float, default=0.5, choices=sorted(HEIGHTS),
                    help="height of the profile line, in metres (default 0.5)")
    ap.add_argument("--svg", action="store_true",
                    help="also write SVG copies; this is how the figures in the "
                         "slides' Section_3_assets are made")
    a = ap.parse_args()

    global SVG
    SVG = a.svg

    here = os.path.dirname(os.path.abspath(__file__))
    where = pick_dir(here, a.dir)
    if not os.path.isdir(where):
        sys.exit("no such directory: %s" % where)

    if a.what in ("solvers", "all"):
        solvers(where, here)
    if a.what in ("profiles", "all"):
        profiles(where, here, a.height)


if __name__ == "__main__":
    main()
