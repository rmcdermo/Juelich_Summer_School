#!/usr/bin/env python3
"""Plot the tracer mass balance for Example 2.

Usage:
    python eval.py [--dir DIR]

DIR defaults to 'results', where FDS writes when you run the case yourself, and
falls back to 'reference' when you have not.

The sphere blows tracer in at a fixed mass flux; some leaves through the OPEN
top and the rest stays in the domain. The three devices integrate those terms,
so the balance to check at the end is

    MASS IN TRACER  ~=  MASS OUT TRACER + MASS VOL TRACER

MASS OUT TRACER comes out negative: both flux devices measure MASS FLUX WALL,
and the wall normal at the OPEN boundary points the opposite way to the one on
the sphere. It is negated here, so the printed numbers and the three curves are
all positive and directly comparable -- and so they match the slide.

Mass in and mass out are time integrals of a flux, which FDS accumulates with a
PID controller (proportional and derivative gains zero, integral gain one), so
the device output is the running total rather than an instantaneous rate.
"""
import argparse
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

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


IN, OUT, VOL = "MASS IN TRACER", "MASS OUT TRACER", "MASS VOL TRACER"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=None,
                    help="directory holding the _devc.csv; default is results/, "
                         "falling back to reference/ when you have not run the case")
    a = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    name = "Example_2_devc.csv"
    where, _ = pick_dir(here, a.dir, name)
    csv = os.path.join(where, name)
    if not os.path.exists(csv):
        sys.exit("no such file: %s\nRun the case first." % csv)

    devc = pd.read_csv(csv, skiprows=1)
    missing = [c for c in (IN, OUT, VOL) if c not in devc.columns]
    if missing:
        sys.exit("columns not found in %s: %s" % (csv, ", ".join(missing)))

    out = -devc[OUT]            # see the note on signs above

    fig, ax = plt.subplots()
    ax.plot(devc["Time"], devc[IN], "-k", label=IN)
    ax.plot(devc["Time"], out, "--b", label=OUT)
    ax.plot(devc["Time"], devc[VOL], "-.r", label=VOL)
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Tracer mass [kg]")
    ax.grid(True)
    ax.legend()
    ax.set_box_aspect(1)

    m_in, m_out, m_vol = devc[IN].iloc[-1], out.iloc[-1], devc[VOL].iloc[-1]
    err = 100.0 * abs(m_in - (m_out + m_vol)) / m_in if m_in else float("nan")
    print("mass in      %.4E kg" % m_in)
    print("mass out     %.4E kg" % m_out)
    print("mass in vol  %.4E kg" % m_vol)
    print("out + vol    %.4E kg   (%.2f %% difference)" % (m_out + m_vol, err))

    plots = os.path.join(here, "plots")
    os.makedirs(plots, exist_ok=True)
    out_pdf = os.path.join(plots, "Example_2_mass_balance.pdf")
    fig.savefig(out_pdf, bbox_inches="tight")
    print("wrote %s" % out_pdf)


if __name__ == "__main__":
    main()
