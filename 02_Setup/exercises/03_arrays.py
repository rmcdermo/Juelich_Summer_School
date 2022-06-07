import numpy as np

n = 10
L = 3.0

x = np.linspace(-L, L, n)
y = x**2

print("x: {}".format(x))
print("y: {}\n".format(y))

print("x[2:4]: {}".format(x[2:4]))
print("x[-2:]: {}\n".format(x[-2:]))

d = y[1:] - y[:-1]
print("d: {}".format(d))
print("len(y): {}, len(d): {}\n".format(len(y), len(d)))

print("|d| > 1: {}".format(d[np.abs(d) > 1]))
print("|d| > 1: {}\n".format(np.where(np.abs(d) > 1)[0]))

z = np.zeros((3,3))
z[1, 2] = 2.0
print("z: \n{}".format(z))
