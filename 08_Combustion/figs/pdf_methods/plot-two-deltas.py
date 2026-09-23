"""Draw schematic delta locations; MathJax labels and weights live in QMD."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(8, 6))
fig.subplots_adjust(left=0.14, right=0.97, bottom=0.13, top=0.97)
# Vertical lines denote singular locations, not finite delta heights.
ax.plot([-0.1, 0.5], [0, 0], color="blue", linewidth=2.5)
ax.plot([0.5, 1.1], [0, 0], color="red", linewidth=2.5)
ax.axvline(0, ymin=0.0625, color="blue", linewidth=2.5)
ax.axvline(1, ymin=0.0625, color="red", linewidth=2.5)
ax.set(xlim=(-0.1, 1.1), ylim=(-0.1, 1.5),
       xticks=np.linspace(0, 1, 6), yticks=np.arange(0, 1.5, 0.2))
ax.tick_params(direction="in", top=True, right=True, labelsize=15)
fig.savefig(Path(__file__).with_name("two-deltas.svg"))
plt.close(fig)
