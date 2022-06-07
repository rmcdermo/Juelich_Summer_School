# load module for plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as fnt
# load module for numerics, here used for data read-in
import numpy as np


# ---------------------------------------------------------------------------
# Plot selection of data from chid_devc.csv
# ---------------------------------------------------------------------------
def plot_selection(selection, cols, title, ylabel, ylim, labels, name,
                   nleg, semilogy):

    plot_file = 'plots/' + name + '.png'

    ax = plt.subplot(111)

    # Shrink current axis's height by 10% on the bottom
    # Put a legend below current axis

    j = 0
    for s in selection:
        for i in cols:
            if semilogy:
                plt.semilogy(data[s][:, 0],
                             data[s][:, i],
                             linewidth=widths[j],
                             linestyle=styles[j],
                             color=colors[j],
                             label=labels[j])
            else:
                plt.plot(data[s][:, 0],
                         data[s][:, i],
                         linewidth=widths[j],
                         linestyle=styles[j],
                         color=colors[j],
                         label=labels[j])
            j = j+1

    legsize = fnt.FontProperties(size=12)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2,
                     box.width, box.height * 0.8])
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.42), prop=legsize,
              fancybox=True, shadow=False, ncol=nleg)

    if title == 'Velocity Error':
        plt.axhline(y=1.0e-16, color='m', linestyle='-', linewidth=1)
    plt.xlabel(xlabel, fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.title(title, fontsize=18)
    plt.xlim(xlim[0], xlim[1])
    plt.ylim(ylim[0], ylim[1])
    plt.tick_params(labelsize=10)
    plt.savefig(plot_file)
    plt.clf()

    print('Plotting file {}'.format(plot_file))


# ---------------------------------------------------------------------------
# Basic definitions, specify solvers to compare
# ---------------------------------------------------------------------------
result_dir = 'results/'
geometry = 'pipe2d'
solvers = ['fft_default', 'fft_tol-5',
           'ulmat', 'uglmat',
           'uscarc', 'uscarc_insep']

xlabel = 'Simulated Time [s]'
tend = 0.5
xlim = [0.0, tend]

units = {}
quantities = {}
data = {}


# ---------------------------------------------------------------------------
# Read in data from chid_devc.csv for each solver
# ---------------------------------------------------------------------------
for solver in solvers:

    # get name of devices file for selected solver
    devc_solver = result_dir + geometry + '_' + solver + '_devc.csv'

    # first open file
    # then read in the first two lines containing the quantities and units
    # finally close the file again
    fin = open(devc_solver, 'r')
    units_line = fin.readline()
    quantities_line = fin.readline()
    fin.close()

    # separate quantities and units by comma
    units_solver = units_line.strip().split(', ')
    quantities_solver = quantities_line.strip().split(', ')

    # remove quotes and end-of-line characters
    for i in range(len(quantities_solver)):
        units_solver[i] = units_solver[i].strip().strip('\'')
        quantities_solver[i] = quantities_solver[i].strip().strip('\'')

    # read whole DEVC data
    data_solver = np.loadtxt(devc_solver, delimiter=',', skiprows=2)

    units[solver] = units_solver
    quantities[solver] = quantities_solver
    data[solver] = data_solver

# ---------------------------------------------------------------------------
# For all solvers plot number of needed pressure iterations
# ---------------------------------------------------------------------------
for solver in solvers:
    pres_ite_max = max(data[solver][20:, 4])
    pres_ite_mean = np.mean(data[solver][20:, 4])
    print("Max  number of pressure iterations for solver {:<13}: {:5.0f}  ".
          format(solver, pres_ite_max))
    print("Mean number of pressure iterations for solver {:<13}: {:5.0f}\n".
          format(solver, pres_ite_mean))


# ---------------------------------------------------------------------------
# For each solver print u-velocity at inflow versus u-velocity at outflow
# ---------------------------------------------------------------------------
widths = [1.5, 1.5]
colors = ['r', 'k']
styles = ['-', '--']

for solver in solvers:
    selection = [solver]
    cols = [1, 2]
    title = 'Volume Mean U-Velocity'
    ylabel = r'Volume Mean'
    ylim = [0.0, 0.6]
    labels = ['$U_{left}$', '$U_{right}$']
    name = 'u-velocity_' + solver
    plot_selection(selection, cols, title, ylabel, ylim, labels, name, 3,
                   False)


# ---------------------------------------------------------------------------
# Plots for all solvers
# ---------------------------------------------------------------------------
colors = ['r', 'k', 'orange', 'g', 'b', 'c']
styles = ['-', '-', '-', '--', '-', '-.']

selection = solvers
labels = ['FFT default', 'FFT tol=1E-5',
          'ULMAT', 'UGLMAT',
          'USCARC', 'inseparable USCARC']
nleg = 3

#
# plot MAXIMUM VELOCITY ERROR
#
widths = [1.5, 1.5, 1.5, 1.5, 1.5, 1.5]
cols = [3]
title = 'Velocity Error'
ylabel = 'Error [m/s]'
ylim = [1e-18, 1e-0]
name = 'velocity_error_all'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, True)

#
# plot PRESSURE ITERATIONS
#
widths = [1.5, 0.75, 1.5, 1.5, 1.5, 1.5]
cols = [4]
title = 'Pressure Iterations'
ylabel = 'Number of Iterations'
ylim = [0.0, 500.0]
name = 'pressure_iterations_all'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)

#
# plot course of PRESSURE
#
widths = [1.5, 1.5, 1.5, 1.5, 1.5, 1.5]
cols = [5]
title = 'Pressure trace'
ylabel = 'Pressure [Pa]'
ylim = [-2.8, 3.3]
name = 'pressure_trace_all'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)


# ---------------------------------------------------------------------------
# Plots for structured solvers
# ---------------------------------------------------------------------------
colors = ['r', 'k', 'orange']
styles = ['-', '-', '-']
selection = ['fft_default', 'fft_tol-5', 'ulmat']
labels = ['FFT default', 'FFT tol=1E-5', 'ULMAT']
nleg = 3

#
# plot PRESSURE ITERATIONS
#
widths = [1.5, 0.75, 1.5]
cols = [4]
title = 'Pressure Iterations'
ylabel = 'Number of Iterations'
ylim = [0.0, 500.0]
name = 'pressure_iterations_structured'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)

#
# plot PRESSURE trace
#
widths = [1.5, 1.5, 1.5]
cols = [5]
title = 'Pressure Trace'
ylabel = 'Number of Iterations'
ylim = [-2.8, 3.3]
name = 'pressure_trace_structured'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)


# ---------------------------------------------------------------------------
# Plots for unstructured solvers
# ---------------------------------------------------------------------------
widths = [1.5, 1.5, 1.5, 1.5]
colors = ['orange', 'g', 'b', 'c']
styles = ['-', '--', '-', '-.']
selection = ['ulmat', 'uglmat', 'uscarc', 'uscarc_insep']
labels = ['ULMAT', 'UGLMAT', 'USCARC', 'inseparable USCARC']
nleg = 2

#
# plot PRESSURE ITERATIONS
#
cols = [4]
title = 'Pressure Iterations'
ylabel = 'Number of Iterations'
ylim = [0.0, 7.5]
name = 'pressure_iterations_unstructured'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)

#
# plot PRESSURE trace
#
cols = [5]
title = 'Pressure Trace'
ylabel = 'Number of Iterations'
ylim = [-2.8, 3.3]
name = 'pressure_trace_unstructured'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)


# ---------------------------------------------------------------------------
# Plots for unstructured global solvers
# ---------------------------------------------------------------------------
widths = [1.5, 1.5, 1.5]
colors = ['g', 'b', 'c']
styles = ['--', '-', '-.']
selection = ['uglmat', 'uscarc', 'uscarc_insep']
labels = ['UGLMAT', 'USCARC', 'inseparable USCARC']
nleg = 3

#
# plot PRESSURE ITERATIONS
#
cols = [4]
title = 'Pressure Iterations'
ylabel = 'Number of Iterations'
ylim = [0.0, 7.5]
label = selection
name = 'pressure_iterations_unstructured_global'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)

#
# Print course of PRESSURE for selection of solvers
#
cols = [5]
title = 'Pressure Iterations'
ylabel = 'Number of Iterations'
ylim = [-2.8, 3.3]
name = 'pressure_trace_unstructured_global'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)
