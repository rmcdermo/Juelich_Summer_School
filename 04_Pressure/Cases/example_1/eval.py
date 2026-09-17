#!/usr/bin/env python3
"""Plot volume flow in and out of the domain for Example 1.

Usage:
    python eval.py [VARIANT] [--dir DIR]

VARIANT is one of FFT, FFT_tight, ULMAT_PARDISO, ULMAT_HYPRE (default FFT); it
selects
which Example_1_<VARIANT>_devc.csv to read.

DIR defaults to 'results', where FDS writes when you run the case yourself, and
falls back to 'reference' when you have not. Pass --dir explicitly to force one.

VDOT_IN is negative because the inlet normal points into the domain, so it is
negated here to compare the two flows directly. The steady-state difference
between them is the velocity error the pressure solver leaves behind, which is
the whole point of the exercise.
"""
import argparse
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator

def pick_dir(here, explicit, filename):
    """Where to read device output from.

    Defaults to the student's own run in 'results/', and falls back to the
    reference run shipped with the class when that is empty. Some cases are too
    large to run in a classroom -- the Sandia plume wants 16 MPI processes --
    so for those 'reference/' is the only data there will ever be, and the
    script should still just work without anyone having to pass a flag.
    """
    if explicit:
        return os.path.join(here, explicit), explicit
    results = os.path.join(here, "results", filename)
    if os.path.exists(results):
        return os.path.join(here, "results"), "results"
    reference = os.path.join(here, "reference", filename)
    if os.path.exists(reference):
        print("no %s in results/, using the reference run" % filename)
        return os.path.join(here, "reference"), "reference"
    return os.path.join(here, "results"), "results"


VARIANTS = ("FFT", "FFT_tight", "ULMAT_PARDISO", "ULMAT_HYPRE")
STEADY_FROM = 4.0          # seconds; flow is developed past this point

# The y axis is fixed, not autoscaled, and these are the bounds the figures on
# the slides use. Two reasons. Autoscaling over the whole run would include the
# startup ramp from zero and squash both curves onto one line, hiding the very
# difference the plot exists to show. Autoscaling over just the steady window
# would instead give each variant its own scale -- FFT spans 0.05 m3/s, ULMAT
# PARDISO 0.004 -- so its machine-precision agreement would be stretched to fill
# the plot and read as noise. A common window lets the four be compared.
YLIM = (6.3, 6.5)
YTICK = 0.02


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("variant", nargs="?", default="FFT", choices=VARIANTS)
    ap.add_argument("--dir", default=None,
                    help="directory holding the _devc.csv; default is results/, "
                         "falling back to reference/ when you have not run the case")
    a = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    name = "Example_1_%s_devc.csv" % a.variant
    where, _ = pick_dir(here, a.dir, name)
    csv = os.path.join(where, name)
    if not os.path.exists(csv):
        sys.exit("no such file: %s\nRun the case first, or check the variant "
                 "name." % csv)

    devc = pd.read_csv(csv, skiprows=1)

    fig, ax = plt.subplots()
    ax.plot(devc["Time"], -devc["VDOT_IN"], "--r", label="VDOT IN")
    ax.plot(devc["Time"], devc["VDOT_OUT"], "b", label="VDOT OUT")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel(r"Volume Flow [m$^3$/s]")
    ax.set_xlim(STEADY_FROM, devc["Time"].iloc[-1])
    ax.set_ylim(*YLIM)
    ax.yaxis.set_major_locator(MultipleLocator(YTICK))
    ax.grid(True)
    ax.legend()
    ax.set_box_aspect(1)

    steady = devc[devc["Time"] >= STEADY_FROM]

    # A fixed window can hide the curve if a run lands outside it -- a different
    # FDS build, or an edited input -- so say so rather than drawing an empty plot.
    lo = min((-steady["VDOT_IN"]).min(), steady["VDOT_OUT"].min())
    hi = max((-steady["VDOT_IN"]).max(), steady["VDOT_OUT"].max())
    if lo < YLIM[0] or hi > YLIM[1]:
        print("warning: steady data spans %.3f..%.3f, outside the plotted "
              "%.2f..%.2f; edit YLIM in this script" % (lo, hi, YLIM[0], YLIM[1]))
    # VDOT_IN is negative, so in + out is the imbalance. Report it at the instant
    # where it is largest in magnitude, and keep its sign: negative means more
    # volume entering than leaving there. The slides tabulate the signed number,
    # so printing the magnitude alone made the two look like different results.
    diff = steady["VDOT_IN"] + steady["VDOT_OUT"]
    imbalance = diff[diff.abs().idxmax()]
    inflow = steady["VDOT_IN"].abs().max()
    print("%s: max in-out volume flow difference %.3g %%"
          % (a.variant, 100.0 * imbalance / inflow))

    plots = os.path.join(here, "plots")
    os.makedirs(plots, exist_ok=True)
    out = os.path.join(plots, "Example_1_%s_VDOT_IN_OUT.pdf" % a.variant)
    fig.savefig(out, bbox_inches="tight")
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
