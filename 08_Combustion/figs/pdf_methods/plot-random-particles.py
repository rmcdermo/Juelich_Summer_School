"""Draw a reproducible random cell following examples/particle_example/particles.py."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Fix the seed so the slide remains identical when regenerated.
rng = np.random.default_rng(74)
fig, ax = plt.subplots(figsize=(4, 4))
fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98)
for color in ("blue", "red"):
    positions = rng.uniform(0, 1, (50, 2))
    ax.scatter(positions[:, 0], positions[:, 1], color=color, s=24)
ax.set(xlim=(0, 1), ylim=(0, 1), xticks=[], yticks=[], aspect="equal")
for spine in ax.spines.values():
    spine.set_linewidth(2)
fig.savefig(Path(__file__).with_name("random-particles.svg"))
plt.close(fig)
