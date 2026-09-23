"""Generate the normalized exponential-decay plot; axis labels live in QMD."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 501)
fig, ax = plt.subplots(figsize=(5.4, 3.2))
fig.subplots_adjust(left=0.12, right=0.97, bottom=0.14, top=0.97)
ax.plot(x, np.exp(-x), color="blue", linewidth=2)
ax.set(xlim=(0, 10), ylim=(0, 1), xticks=[0, 5, 10], yticks=[0, 0.5, 1])
ax.set_yticklabels(["0", "0.5", "1"])
ax.tick_params(direction="in", top=True, right=True, labelsize=14)
for spine in ax.spines.values():
    spine.set_color("0.55")
fig.savefig(Path(__file__).with_name("unmixed-fraction-decay.svg"))
plt.close(fig)
