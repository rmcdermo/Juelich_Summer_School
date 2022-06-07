import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

############################
##### change parameters here

# computational domain extension: x in [-L, L]
# default: 2
L = 2.0

# end time of computation
# default: 5
T = 5.0

# wave velocity
# default: 1
c = 1.0

# time step size
# default: 0.01
dt = 0.01

# mesh spacing
# default: 0.1
dx = 0.1

# time integration scheme: euler_backward, euler_forward, theta, leap
# default: euler_forward
scheme = "euler_forward"

# set theta value for theta scheme: 0 - explicit, 1 - implicit, 0.5 - semi-implicit
# default: 0.5
theta = 0.5

# initial value function: wave, gauss
# default: wave
initial = "wave"

# set mode for wave initial value
# default: 1
wave_mode = 1

# set width for gauss peak
# default: 0.5
gauss_width = 0.5

##### stop changing, unless on purpose
######################################

##########################
########## INIT ##########

## definition of single mode wave solutions
def wave(x, t):
    k = (2*np.pi / (2*L)) * wave_mode
    return np.sin(k * (x - c * t))

## setup variables
def setup(cdx, cdt):
    global nx, nt, x_an, x, rho, v, rhop, vp, T, theta, b, A, dt, dx

    dx = cdx
    dt = cdt

    ## compute dt and dx, correct T
    nt = int(T / dt)
    T = nt*dt
    nx = int(2*L / dx) + 2

    ## create discretisation
    x = np.linspace(-dx-L, L, nx)

    ## x-values for analytical solution
    x_an = np.linspace(-dx-L, L, 1000)

    ## buffers for rho and v
    rho = np.zeros_like(x)
    v   = np.zeros_like(x)

    ## buffers for intermediate solutions
    rhop = np.zeros_like(x)
    vp   = np.zeros_like(x)

    ## initialisation
    if initial=='wave':
        rho = wave(x+dx/2, 0,)
        v   = -wave(x, 0)

    if initial=='gauss':
        rho = np.exp(-x**2/gauss_width**2)
        v   = 0*x

    if initial=='step':
        step_width=1.5
        step_slope=20
        rho = (np.arctan(step_slope*(x-step_width/2.)) - np.arctan(step_slope*(x+step_width/2.)) + np.pi) / np.pi
        v   = 0*x
        # rho[(x>-step_width) & (x<step_width)] = 1

    ## for implicit schemes: system matrix A, rhs b
    A = np.zeros((2*nx,2*nx))
    if scheme == 'euler_backward': theta = 1.0
    f = - theta * dt * c / (dx)
    for i in range(1, nx - 1):
        A[i, i] = 1
        A[i, nx + i - 1] = -f
        A[i, nx + i    ] = f

        A[nx + i, nx + i] = 1
        A[nx + i, i    ] = -f
        A[nx + i, i + 1] = f


    A[0,0] = 1
#     A[0,1] = f
#     A[0,] = f
    A[nx-1, nx-1] = 1
    A[nx, nx] = 1
    A[-1,-1] = 1

    # rhs
    b = np.zeros(2*nx)


## time step index
it = 0

############################
########## SOLVER ##########

################
## forward Euler
def update_euler_forward():

    vp[1:-1] = dt * c * (rho[1:-1] - rho[:-2])/(dx)

    rhop[1:-1] = dt * c * (v[2:] - v[1:-1])/(dx)

    v[:] += vp[:]
    v[0] = v[-2]
    v[-1] = v[1]

    rho[:] += rhop[:]
    rho[0] = rho[-2]
    rho[-1] = rho[1]

#################
## backward Euler
def update_euler_backward():

    # update rhs
    b[:nx] = v[:]
    b[nx:] = rho[:]

    # solve linear system
    sol = np.linalg.solve(A, b)

    # redistribute solution
    v[:] = sol[:nx]
    rho[:] = sol[nx:]

    # set boundary conditions
    v[0] = v[-2]
    v[-1] = v[1]

    rho[0] = rho[-2]
    rho[-1] = rho[1]

############
## leap frog
def update_leap():
    global dt, x, rho, v, it, L, c

    v[1:-1] += dt * c * (rho[1:-1] - rho[:-2]) / (dx)

    v[0] = v[-2]
    v[-1] = v[1]

    rho[1:-1] += dt * c * (v[2:] - v[1:-1]) / (dx)

    rho[0] = rho[-2]
    rho[-1] = rho[1]

###############
## theta method
def update_theta():

    # compute explicit contribution
    vp[1:-1]   = dt * c * (rho[1:-1] - rho[:-2])/(dx)
    rhop[1:-1] = dt * c * (v[2:] - v[1:-1])/(dx)

    vp[0] = 0
    vp[-1] = 0
    rhop[0] = 0
    rhop[-1] = 0

    # set rhs
    b[:nx] = v   + (1-theta) * vp
    b[nx:] = rho + (1-theta) * rhop

    # solve linear system
    sol = np.linalg.solve(A, b)

    # redistribute solution
    v[:] = sol[:nx]
    rho[:] = sol[nx:]

    # set boundary conditions
    v[0] = v[-2]
    v[-1] = v[1]

    rho[0] = rho[-2]
    rho[-1] = rho[1]


######################################
########## UPDATE ANIMATION ##########

update_fnk = globals()["update_{}".format(scheme)]

def update_animation(*args):
    global it

    it += 1

    update_fnk()

    t = it * dt

    l1.set_ydata(rho)
    l2.set_ydata(v)
    if initial == 'wave':
        l3.set_ydata(wave(x_an, t))
        return l1, l2, l3
    else:
        return l1, l2

########################################
########## CONVERGENCE HELPER ##########

def solve():
    for i in range(nt-1):
        update_fnk()

def rmse():
    return np.sqrt(np.sum((rho - wave(x+dx/2,T)) ** 2) / nx)

###############################
########## MAIN LOOP ##########

convergence_mode = False

if convergence_mode:

    refinement_dt = 7
    refinement_dx = 7

    if initial != 'wave':
        print(" !!! convergence mode only with wave initial conditions !!!")

    T0 = 0.1
    T = T0
    dt0 = dt
    dx0 = dx

    errors_dx = []
    dxs = []

    # compute one level finer than required, this will be the reference error
    setup(dx0 / 2.**refinement_dx, dt0 / 2. ** refinement_dx)
    print(dx, dt)
    solve()
    error0 = rmse()

    print("-- scheme: {} {}".format(scheme, "= {}".format(theta) if scheme == 'theta' else ''))
    print("-- convergence in space")
    print("dx           error")
    for idx in range(refinement_dx):
        T = T0
        dt = dt0 / 2 ** refinement_dx
        dx = dx0 / 2 ** idx
        setup(dx, dt)
        solve()
        error = np.abs((rmse() - error0))
        print("{:e} {:e}".format(dx, error))
        dxs.append(dx)
        errors_dx.append(error)


    errors_dt = []
    dts = []

    print("-- convergence in time")
    print("dt           error")

    # compute one level finer than required, this will be the reference error
    setup(dx0, dt0 / 2.**refinement_dt)
    solve()
    error0 = rmse()

    for idt in range(refinement_dt):
        T = T0
        dt = dt0 / 2 ** idt
        dx = dx0
        setup(dx, dt)
        solve()
        error = np.abs(rmse() - error0)
        print("{:e} {:e}".format(dt, error))
        dts.append(dt)
        errors_dt.append(error)

    # plt.plot(dxs, errors_dx)
    plt.loglog(dxs, errors_dx, '-o', label='spatial error')
    plt.loglog(dts, errors_dt, '-o', label='temporal error')

    # plot guides for first and second order
    e_xmin = min(dxs[-1], dts[-1])
    e_xmax = max(dxs[0], dts[0])
    plt.loglog([e_xmin, e_xmax], [1e-1 * e_xmin, 1e-1 * e_xmax], alpha=0.25, label='O(dx^1)')
    plt.loglog([e_xmin, e_xmax], [1e-1 * e_xmin ** 2, 1e-1 * e_xmax ** 2], alpha=0.25, label='O(dx^2)')

    plt.xlabel("discretization")
    plt.ylabel("error")
    plt.legend()

    # plt.savefig("04_wave_convergence.pdf")
    plt.show()

else:
    # setup system
    setup(dx, dt)

    # init plots
    fig, ax = plt.subplots()

    l1, = ax.plot(x + dx / 2., rho, '-o', linewidth=1, label="density")
    l2, = ax.plot(x, v, '-o', linewidth=1, label="velocity")
    if initial == 'wave':
        l3, = ax.plot(x_an, wave(x_an, 0), linewidth=2, alpha=0.5, color='red', label="analytical density")

    amp = max(np.max(rho), np.max(v))
    ax.plot([-L, L], [amp, amp], color='gray')
    ax.plot([-L, L], [-amp, -amp], color='gray')

    plt.legend(loc='lower center')
    plt.xlabel("x")
    plt.ylabel("v and rho fluctuations")
    plt.title("scheme: {} {}".format(scheme, "= {}".format(theta) if scheme == 'theta' else ''))

    # run animation loop
    ani = animation.FuncAnimation(fig, update_animation, range(nt),
                              interval=25, blit=False, repeat=False)

    plt.show()

    # for i in range(nt):
    #     update_animation()
    #
    # plt.savefig("04_wave.pdf")
