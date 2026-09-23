"""Plot the fully unmixed, equal-volume case and its scalar variance."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np


def main():
    output = Path(__file__).resolve().parent
    values = np.array([1.0, 0.0])
    weights = np.array([0.5, 0.5])
    mean = np.sum(weights * values)
    variance = np.sum(weights * (values - mean) ** 2)
    zeta = 1.0
    assert np.isclose(variance, zeta * mean * (1 - mean))

    for kind in ("cell", "variance"):
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.subplots_adjust(left=0.18, right=0.97, bottom=0.18, top=0.96)
        ax.set(xlim=(0, 1), xticks=[0, 0.5, 1])
        if kind == "cell":
            # Separate horizontal segments preserve the discontinuous field.
            ax.plot([0, 0.5], [values[0]] * 2, color="blue", linewidth=2.5)
            ax.plot([0.5, 1], [values[1]] * 2, color="blue", linewidth=2.5)
            ax.set(ylim=(-0.1, 1.1), yticks=np.linspace(0, 1, 6))
            ax.set_xlabel("normalized cell volume", fontsize=19)
            ax.set_ylabel("sample space", fontsize=19)
        else:
            ax.plot(mean, variance, marker="s", color="blue", markersize=10)
            ax.set(ylim=(0, 0.3), yticks=[0, 0.1, 0.2, 0.3])
            ax.set_xlabel("mean cell composition", fontsize=19)
            ax.set_ylabel("SGS scalar variance", fontsize=19)
        ax.xaxis.set_major_formatter(FormatStrFormatter("%g"))
        ax.yaxis.set_major_formatter(FormatStrFormatter("%g"))
        ax.tick_params(direction="in", top=True, right=True, labelsize=17)
        fig.savefig(output / f"unmixed-sgs-{kind}.svg", metadata={"Date": None})
        plt.close(fig)
    print(f"zeta={zeta:g}, mean={mean:g}, variance={variance:g}")


if __name__ == "__main__":
    main()
