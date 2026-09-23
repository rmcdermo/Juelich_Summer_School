"""Reproduce the four unmixed-fraction cases and the SGS variance summary.

Run without arguments for all plots, or select e.g. --cases 2 3 4 summary.
Cell segment widths are the three environment weights; variance is computed
from these weighted scalar values and checked against zeta * mean * (1-mean).
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

CASES = [(1.0, 0.5, "blue"), (1.0, 0.25, "blue"),
         (0.5, 0.5, "magenta"), (0.5, 0.25, "magenta")]


def cell_statistics(zeta, mean):
    values = np.array([1.0, mean, 0.0])
    weights = np.array([zeta * mean, 1 - zeta, zeta * (1 - mean)])
    actual_mean = np.sum(weights * values)
    variance = np.sum(weights * (values - actual_mean) ** 2)
    assert np.isclose(weights.sum(), 1)
    assert np.isclose(actual_mean, mean)
    assert np.isclose(variance, zeta * mean * (1 - mean))
    return values, weights, variance


def axes(figsize=(8, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(left=0.18, right=0.97, bottom=0.18, top=0.96)
    ax.set(xlim=(0, 1), xticks=[0, 0.5, 1])
    ax.xaxis.set_major_formatter(FormatStrFormatter("%g"))
    ax.yaxis.set_major_formatter(FormatStrFormatter("%g"))
    ax.tick_params(direction="in", top=True, right=True, labelsize=17)
    return fig, ax


def draw_case(output, number):
    zeta, mean, color = CASES[number - 1]
    values, weights, variance = cell_statistics(zeta, mean)
    edges = np.r_[0, np.cumsum(weights)]
    suffix = "" if number == 1 else f"-case-{number}"
    for kind in ("cell", "variance"):
        fig, ax = axes()
        if kind == "cell":
            # Disconnected segments preserve jumps and omit zero-width regions.
            for i, (value, weight) in enumerate(zip(values, weights)):
                if weight > 0:
                    ax.plot(edges[i:i + 2], [value] * 2,
                            color=color, linewidth=2.5)
            ax.set(ylim=(-0.1, 1.1), yticks=np.linspace(0, 1, 6))
            ax.set_xlabel("normalized cell volume", fontsize=19)
            ax.set_ylabel("sample space", fontsize=19)
        else:
            # Each successive slide retains the earlier cases for comparison.
            for previous_zeta, previous_mean, previous_color in CASES[:number]:
                _, _, previous_variance = cell_statistics(previous_zeta, previous_mean)
                ax.plot(previous_mean, previous_variance, marker="s",
                        color=previous_color, markersize=10)
            ax.set(ylim=(0, 0.3), yticks=[0, 0.1, 0.2, 0.3])
            ax.set_xlabel("mean cell composition", fontsize=19)
            ax.set_ylabel("SGS scalar variance", fontsize=19)
        fig.savefig(output / f"unmixed-sgs-{kind}{suffix}.svg", metadata={"Date": None})
        plt.close(fig)
    print(f"case {number}: zeta={zeta:g}, mean={mean:g}, variance={variance:g}")


def draw_summary(output):
    fig, ax = axes(figsize=(9, 6))
    mean = np.linspace(0, 1, 401)
    for zeta, color in [(1, "blue"), (0.75, "cyan"), (0.5, "magenta"),
                        (0.25, "red"), (0, "black")]:
        ax.plot(mean, zeta * mean * (1 - mean), color=color, linewidth=2)
        ax.annotate(rf"$\zeta={zeta:g}$", (0.5, zeta * 0.25),
                    xytext=(0, 5), textcoords="offset points",
                    ha="center", va="bottom", fontsize=17)
    ax.set(ylim=(0, 0.3), xticks=np.linspace(0, 1, 6),
           yticks=np.arange(0, 0.26, 0.05))
    ax.set_xlabel("mean cell composition", fontsize=19)
    ax.set_ylabel("SGS scalar variance", fontsize=19)
    fig.savefig(output / "unmixed-sgs-summary.svg", metadata={"Date": None})
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", nargs="+", choices=["1", "2", "3", "4", "summary"],
                        default=["1", "2", "3", "4", "summary"])
    args = parser.parse_args()
    output = Path(__file__).resolve().parent
    for case in args.cases:
        if case == "summary":
            draw_summary(output)
        else:
            draw_case(output, int(case))


if __name__ == "__main__":
    main()
