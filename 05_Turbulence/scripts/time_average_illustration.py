import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(7,4))

x = np.linspace(0, 1, 200)

y1 = 1.25 + np.sin(5*x) - 2*x
y2 = (2*np.random.random(len(x)) - 1) * 0.1

plt.plot(x, y1 + y2, label="$\\phi(t)$", lw=2, color='black')
plt.plot(x, y1, label="$\\langle \\phi(t) \\rangle$", color='C1')
plt.plot(x, y2, label="$\\phi'(t)$", color='C2')

plt.xticks([])
plt.yticks([0],[0])

plt.xlabel("Time")
plt.ylabel("$\\phi$")

plt.legend()
plt.grid()

plt.savefig("time_average_illustration.png", dpi=300, bbox_inches='tight')