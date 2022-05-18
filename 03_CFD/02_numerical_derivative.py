import matplotlib.pyplot as plt
import numpy as np

############################
##### change parameters here

# define number of discretization points
# default: 10
n = 10

# define the evaluation interval, x in [-L, L]
# default: 2
L = 2

##### stop changing, unless on purpose
######################################


##### DEFINITIONS
# define analytical function
def func(x): return np.exp(-x**2)

# define analytical derivation
def deri(x): return -2. * x * np.exp(-x**2)

x = np.linspace(-L,L,n)
dx = x[1] - x[0]
y = func(x)

yp = np.zeros_like(y)


##### COMPUTE DERIVATIVE
# handling of bulk grid points
for i in range(1, len(yp) - 1):
    # yp[i] = (y[i+1] - y[i]) / dx
    yp[i] = (y[i+1] - y[i-1]) / (2*dx)

# left boundary
yp[0] = (y[1] - y[0]) / dx

# right boundary
yp[-1] = (y[-1] - y[-2]) / dx


##### COMPUTE ERROR

an_yp = deri(x)

RMSE = np.sqrt(np.sum((yp-an_yp)**2) / n)

print("RMSE: {}".format(RMSE))

##### PLOTTING

# define 'analytical' function and derivation for plotting only
an_x = np.linspace(-L,L,1000)
an_y = func(an_x)
an_yp = deri(an_x)

## plot soluton and analytical functions
plt.plot(an_x, an_y, label='analytical function')
plt.plot(an_x, an_yp, label='analytical derivation')
plt.plot(x, yp, 'o', label='numerical derivation')


## plot difference lines
plt.plot([x[0],x[0]], [yp[0], deri(x[0])], color='red', alpha=1.0, linewidth=1, zorder=1, label="error")
for i in range(n):
    plt.plot([x[i],x[i]], [yp[i], deri(x[i])], color='red', alpha=1.0, linewidth=1, zorder=1)

plt.xlabel("x")
plt.ylabel("f(x) and f'(x)")

plt.legend()

plt.title("n={}, RMSE={:8.2e}".format(n, RMSE))
# plt.savefig("02_derivative.pdf")
plt.show()
