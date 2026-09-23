"""Draw the square 100-particle cell from examples/particle_example/particles.py."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(4, 4))
fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98)
x, y = np.meshgrid(np.linspace(0.05, 0.95, 10), np.linspace(0.05, 0.95, 10))
ax.scatter(x.ravel(), y.ravel(), c=np.where(x.ravel() < 0.5, "blue", "red"), s=24)
ax.set(xlim=(0, 1), ylim=(0, 1), xticks=[], yticks=[], aspect="equal")
for spine in ax.spines.values():
    spine.set_linewidth(2)
fig.savefig(Path(__file__).with_name("uniform-particles.svg"))
plt.close(fig)
