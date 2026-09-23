"""Reproduce the variance examples; symbolic axis labels live in QMD."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

cases = {"unmixed": (0, 1), "partially-mixed": (0.2, 0.8),
         "nearly-mixed": (0.4, 0.6), "fully-mixed": (0.5, 0.5)}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--cases", nargs="+", choices=cases, default=list(cases))
args = parser.parse_args()

for name in args.cases:
    values = cases[name]
    data = np.full((10, 10), values[0], dtype=float)
    data[:, 5:] = values[1]
    fig = plt.figure(figsize=(8, 3.5))
    cell = fig.add_axes([0.02, 0.15, 0.35, 0.8])
    image = cell.imshow(data, cmap="inferno", vmin=0, vmax=1,
                        interpolation="nearest", aspect="equal")
    cell.set(xticks=[], yticks=[])
    scale = fig.add_axes([0.39, 0.15, 0.018, 0.8])
    fig.colorbar(image, cax=scale, ticks=[0, 0.5, 1])
    scale.tick_params(labelsize=10)
    histogram = fig.add_axes([0.51, 0.15, 0.47, 0.8])
    histogram.hist(data.ravel(), bins=np.linspace(0, 1, 100), color="blue")
    histogram.set(xlim=(0, 1), ylim=(0, 100 if values[0] == values[1] else 50),
                  xticks=np.linspace(0, 1, 6))
    histogram.tick_params(direction="in", labelsize=11)
    for ax in (cell, histogram, scale):
        for spine in ax.spines.values():
            spine.set_color("0.5")
    fig.savefig(Path(__file__).with_name(f"variance-{name}.svg"))
    plt.close(fig)
