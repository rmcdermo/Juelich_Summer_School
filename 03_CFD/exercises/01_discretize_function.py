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

# define analytical function
def func(x): return np.exp(-x**2)

# discretize the function by evaluation at selected positions
# define x as the positions of grid points, equally spaced n points between -L and L
x = np.linspace(-L,L,n)

# evaluate function at each point in x
y = func(x)

# compute the cell integrals
n_integration = 10
yp = np.zeros_like(x)
dx = x[1] - x[0]
dxx = dx / n_integration
for i in range(n):
    for ii in range(n_integration):
        xeval = x[i] - dx/2 + dxx/2 + dxx * ii
        yp[i] += func(xeval)
    yp[i] /= n_integration

##### PLOTTING

# define 'analytical' function for plotting only
an_x = np.linspace(-L,L,1000)
an_y = func(an_x)

# plot 'analytical' function
plt.plot(an_x, an_y, label='analytical', linewidth=3)

# plot dircretized function
plt.plot(x, y, 'o', label='nodal values, n={}'.format(n))

# plot steps for cell integrals
# compute dx for step width / shift
dx = x[1] - x[0]
step_x = np.zeros(len(x)+1)
step_x[1:] = x + dx/2.
step_x[0] = x[0] - dx/2.
step_y = np.zeros_like(step_x)
step_y[1:] = yp
step_y[0] = step_y[1]
plt.step(step_x, step_y, color='gray', label="cell integral")

plt.xlabel("x")
plt.ylabel("f(x)")

plt.xlim([-L,L])

plt.legend(loc="best")

# plt.savefig("01_discretization.pdf")
plt.show()
