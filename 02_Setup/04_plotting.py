import matplotlib.pyplot as plt
import numpy as np

L = 3
n = 30
x0 = 1.0

x = np.linspace(-L, L, n)
y1 = np.exp(-(x-x0)**2)
y2 = np.zeros_like(x)
y2[ np.abs(x-x0) < 1.0] = 1.0

plt.plot(x,y1, label="gauss", marker='o')
plt.plot(x,y2, label="step", marker='d')

plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc='best')
plt.grid()
plt.savefig("04_plotting.pdf")
plt.show()
