import matplotlib.pyplot as plt
import numpy as np

############################
##### change parameters here

# define initial number of discretization points
# default: 10
n = 10

# define the number of refinements, i.e. how often n is
# increased by a factor of 2
# default: 5
n_refinements = 5

# define the computational domain: x in [-L, L]
# default: 2
L = 2

##### stop changing, unless on purpose
######################################

# define analytical function
def func(x): return np.exp(-x**2)

# define analytical derivation
def deri(x): return -2. * x * np.exp(-x**2)

def solve(n):

    x = np.linspace(-L,L,n)
    dx = x[1] - x[0]
    y = func(x)

    yp = np.zeros_like(y)

    # handling of bulk grid points
    for i in range(1, len(yp) - 1):
        # yp[i] = (y[i+1] - y[i]) / dx
        yp[i] = (y[i+1] - y[i-1]) / (2*dx)

    # left boundary
    yp[0] = (y[1] - y[0]) / dx
    # yp[0] = (-y[2] + 4*y[1] -3*y[0]) / (2*dx)

    # right boundary
    yp[-1] = (y[-1] - y[-2]) / dx
    # yp[-1] = (y[-3] - 4*y[-2] + 3*y[-1]) / (2*dx)

    ##### COMPUTE ERROR

    an_yp = deri(x)

    RMSE = np.sqrt(np.sum((yp-an_yp)**2) / n)

    return dx, RMSE

##### REFINEMENT LOOP

list_dx = []
list_rmse = []

for i in range(n_refinements):
    current_n = n * 2**i
    dx, rmse = solve(current_n)
    list_dx.append(dx)
    list_rmse.append(rmse)

print("dx       error     factor   order")
print("=================================")
for i in range(n_refinements):
    if i == 0:
        print("{:6.2e} {:6.2e}".format(list_dx[i], list_rmse[i]))
    else:
        factor = list_rmse[i-1] / list_rmse[i]
        order = np.log(factor) / np.log(2)
        print("{:6.2e} {:6.2e}  {:.2f}     {:.2f}".format(list_dx[i], list_rmse[i], factor, order))


##### PLOTTING

plt.plot(list_dx, list_rmse, marker='o', label='approximation', linewidth=2)

x1 = list_dx[-1]
x2 = list_dx[ 0]

plt.xlabel("dx")
plt.ylabel("RMSE")

plt.legend()

plt.savefig("03_convergence.pdf")
plt.show()
