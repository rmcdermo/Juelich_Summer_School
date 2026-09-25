"""Generate the wall-law plot used on the Scaling slide.

Run from any directory:
    python3 05_Turbulence/figs/plot_log_law.py

Requires NumPy and Matplotlib. The default output is log_law.svg beside this script.
The two asymptotes use kappa=0.41 and B=5.2 and meet at their computed
intersection. This illustration is not a resolved buffer-layer profile or
the exact FDS switch (11.81); it retains the corner between the asymptotes.
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).with_name("log_law.svg"),
    )
    args = parser.parse_args()

    kappa, intercept = 0.41, 5.2
    # Find the outer intersection of y+ = ln(y+)/kappa + B.
    lower, upper = 5.0, 20.0
    for _ in range(60):
        midpoint = (lower + upper) / 2
        if midpoint - np.log(midpoint) / kappa - intercept > 0:
            upper = midpoint
        else:
            lower = midpoint
    transition = (lower + upper) / 2
    assert abs(transition - np.log(transition) / kappa - intercept) < 1e-12
    viscous_y = np.geomspace(1.0, transition, 500)
    log_y = np.geomspace(transition, 1000.0, 350)

    with plt.rc_context({
        "font.family": "DejaVu Sans", "font.size": 16,
        "mathtext.fontset": "stix", "svg.fonttype": "path",
        "axes.labelsize": 24, "axes.spines.top": False,
        "axes.spines.right": False, "svg.hashsalt": "juelich-log-law",
        "axes.linewidth": 1.2,
    }):
        fig, ax = plt.subplots(figsize=(6.4, 5.6), layout="constrained")
        ax.semilogx(viscous_y, viscous_y, color="#2463a6", linewidth=3.2)
        ax.semilogx(log_y, np.log(log_y) / kappa + intercept,
                    color="#b94641", linewidth=3.2)
        ax.axvline(transition, color="#999999", linestyle=(0, (3, 4)), linewidth=1)
        ax.text(1.4, 16, "Viscous law\n" + r"$u^+=y^+$",
                color="#2463a6", fontsize=18, linespacing=1.5)
        ax.text(23, 5, "Log law\n" + r"$u^+=\frac{1}{0.41}\ln(y^+)+5.2$",
                color="#b94641", fontsize=18, linespacing=1.5)
        ax.text(transition * 1.2, 1.0, f"{transition:.2f}", fontsize=14, color="#555555")
        ax.set(xlabel=r"$y^+$", ylabel=r"$u^+$", xlim=(1, 1000), ylim=(0, 25))
        ax.set_yticks([0, 5, 10, 15, 20])
        ax.tick_params(which="major", length=6, width=1.2)
        ax.tick_params(which="minor", length=3, color="#888888")
        fig.savefig(args.output, dpi=300, metadata={"Date": None})
        plt.close(fig)
    if args.output.suffix.lower() == ".svg":
        # A standalone SVG that also works inside a raw HTML include in Quarto.
        svg = args.output.read_text()
        svg = svg[svg.index("<svg"):]
        svg = svg.replace('<svg ', '<svg role="img" aria-label="Viscous and log-law asymptotes, joined continuously at y plus 11.06" ', 1)
        args.output.write_text(svg)
    print(f"Continuous intersection: y+ = {transition:.8f}")
    print(args.output)


if __name__ == "__main__":
    main()
