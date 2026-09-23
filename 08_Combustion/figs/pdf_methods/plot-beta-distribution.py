"""Plot the four Beta PDF examples; symbolic labels are authored in QMD."""
from math import lgamma
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Use the exact mean and gamma values displayed in the lecture legend.
# Avoid the endpoints, where some of these densities are singular.
z = np.linspace(1e-6, 1 - 1e-6, 5000)
fig, ax = plt.subplots(figsize=(8, 6))
fig.subplots_adjust(left=0.14, right=0.97, bottom=0.13, top=0.97)
for mean, gamma, color in [(0.6, 4, "blue"), (0.6, 10, "red"),
                           (0.6, 0.5, "green"), (0.8, 2, "black")]:
    a, b = mean * gamma, (1 - mean) * gamma
    log_beta = lgamma(a) + lgamma(b) - lgamma(a + b)
    density = np.exp((a - 1) * np.log(z) + (b - 1) * np.log1p(-z) - log_beta)
    ax.plot(z, density, color=color, linewidth=2.5)
ax.set(xlim=(0, 1), ylim=(0, 8), xticks=np.linspace(0, 1, 6))
ax.tick_params(direction="in", top=True, right=True, labelsize=15)
fig.savefig(Path(__file__).with_name("beta-distribution.svg"))
plt.close(fig)
