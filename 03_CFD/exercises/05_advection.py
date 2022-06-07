import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

############################
##### change parameters here

# computational domain extension: x in [-L, L]
# default: 2
L = 2.0

# end time of computation
# default: 4
T = 4.0

# advection velocity
# default: 1
v = 1.0

# time step
# default: 0.01
dt = 0.01

# mesh spacing
# default: 0.05
dx = 0.05

# initial function: gauss or step
# default: gauss
core = "gauss"

# spatial discretization scheme: central or upwind
# default: central
scheme = "central"

##### stop changing, unless on purpose
######################################

skip_frame = 1

def solution_core_step(x):
    y = x*0
    d = 0.5
    y[(x>-d) & (x<d)] = 1.0
    return y

def solution_core_gauss(x):
    d = 0.2
    return np.exp(-x ** 2 / d ** 2)

core_fnk = globals()["solution_core_{}".format(core)]

def solution(x, t, core):
    vt = -v*t
    while vt >  L: vt -= 2*L
    while vt < -L: vt += 2*L
    xp = x + vt
    return core(xp-2*L) + core(xp) + core(xp+2*L)


nt = int(T / dt)
T = nt*dt
nx = int(2*L / dx) + 2

x = np.linspace(-dx-L, L, nx)
x_an = np.linspace(-dx-L, L, 1000)

phi = np.zeros_like(x)

phip = np.zeros_like(x)

phi = solution(x, 0, core_fnk)

fig, ax = plt.subplots()

l1, = ax.plot(x, phi, '-o', linewidth=1, label="numerical")
l2, = ax.plot(x_an, solution(x_an, 0, core_fnk), linewidth=2, alpha=0.5, color='red', label="analytical")

an_amplitude = np.max(solution(x_an, 0, core_fnk))
ax.plot([-L,L], [ an_amplitude,  an_amplitude], color='gray')
ax.plot([-L,L], [0, 0], color='gray')

plt.legend(loc='best')
plt.xlabel("x")
plt.ylabel("phi")

it = 0

def update_central(*args):
    global dt, x, phi, it, L, c

    it += 1
    t = it * dt

    phip[1:-1] = - dt * v * (phi[2:] - phi[:-2])/(2*dx)

    phi[:] += phip[:]
    phi[0] = phi[-2]
    phi[-1] = phi[1]

    if it % skip_frame == 0:
        l1.set_ydata(phi)
        l2.set_ydata(solution(x_an, t, core_fnk))

    return l1, l2

def update_upwind(*args):
    global dt, x, phi, it, L, c

    it += 1
    t = it * dt

    if v > 0:
        phip[1:-1] = - dt * v * (phi[1:-1] - phi[:-2]) / (dx)
    else:
        ##### OPTIONAL: implement the upwind scheme for negative velocity
        #phip[1:-1] = - dt * v * (phi[2:] - phi[1:-1]) / (dx)
        phip[1:-1] = 0

    phi[:] += phip[:]
    phi[0] = phi[-2]
    phi[-1] = phi[1]

    if it % skip_frame == 0:
        l1.set_ydata(phi)
        l2.set_ydata(solution(x_an, t, core_fnk))

    return l1, l2

ani = animation.FuncAnimation(fig, globals()["update_{}".format(scheme)], range(nt),
                              interval=25, blit=False, repeat=False)

plt.show()

# for i in range(nt):
#     globals()["update_{}".format(scheme)]()
#
# plt.title("t={:.2f}, dx={:8.2e}, dt={:8.2e}".format(nt*dt, dx, dt))
# plt.savefig("05_advection.pdf")
