import matplotlib.pyplot as plt
import matplotlib.font_manager as fnt
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
        plt.axhline(y=1.0e-16, color='m', linestyle='-', linewidth=1.25)
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
geometry = 'tunnel_demo'
solvers = ['fft_tol-3',
           'fft_tol-6',
           'glmat',
           'scarc_insep']

xlabel = 'Simulated Time [s]'
xlim = [0.0, 30.0]

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
    pres_ite_max = max(data[solver][20:, 2])
    pres_ite_mean = np.mean(data[solver][20:, 2])
    print("Max  number of pressure iterations for solver {:<13}: {:5.0f}  ".
          format(solver, pres_ite_max))
    print("Mean number of pressure iterations for solver {:<13}: {:5.0f}\n".
          format(solver, pres_ite_mean))


# ---------------------------------------------------------------------------
# Plots for all solvers
# ---------------------------------------------------------------------------
widths = [1.25, 1.25, 1.25, 1.25]
colors = ['r', 'g', 'c', 'b']
styles = ['-', '-', '-', '-']
selection = solvers
labels = ['FFT tol=1E-3 with TP', 'FFT tol=1E-6 with TP', 'GLMAT default', 'Inseparable SCARC']
nleg = 2

#
# For each solver print MAXIMUM VELOCITY ERROR
#
cols = [1]
title = 'Velocity Error'
ylabel = 'Error [m/s]'
ylim = [1e-18, 1e-0]
name = 'velocity_error_all'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, True)

#
# For each solver print PRESSURE ITERATIONS
#
cols = [2]
title = 'Pressure Iterations'
ylabel = 'Number of Iterations'
ylim = [0.0, 200.0]
name = 'pressure_iterations'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)

#
# For each solver print course of PRESSURE
#
cols = [3]
title = 'CPU'
ylabel = 'CPU [s]'
ylim = [0.0, 6000.0]
name = 'cpu_all'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)
