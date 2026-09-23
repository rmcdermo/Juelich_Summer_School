"""Plot the normal PDFs from normal_pdf.py; symbolic labels live in QMD."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

v = np.linspace(-1, 1, 1000)
fig, ax = plt.subplots(figsize=(8, 6))
fig.subplots_adjust(left=0.14, right=0.97, bottom=0.13, top=0.97)
for sigma, color in [(0.1, "blue"), (0.2, "red"), (0.5, "green")]:
    density = np.exp(-0.5 * (v / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))
    ax.plot(v, density, color=color, linewidth=2.5)
ax.set(xlim=(-1, 1), ylim=(0, 4), xticks=[-1, -0.5, 0, 0.5, 1])
ax.tick_params(direction="in", top=True, right=True, labelsize=15)
fig.savefig(Path(__file__).with_name("normal-distribution.svg"))
plt.close(fig)
