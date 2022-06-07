# load module for plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as fnt
# load module for numerics, here used for data read-in
import numpy as np


# ----------------------------------------------------------------------------
# Plot selected data from chid_devc.csv
# ----------------------------------------------------------------------------
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

    legsize = fnt.FontProperties(size=11)
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


# ----------------------------------------------------------------------------
# Basic definitions, specify solvers to compare
# ----------------------------------------------------------------------------
result_dir = 'results/'
geometry = 'dancing_eddies'
solvers = ['fft_default',
           'fft_default_tp',
           'fft_tol-5',
           'fft_tol-5_tp',
           'ulmat_default',
           'ulmat_tol-5',
           'uglmat',
           'uscarc_insep']

xlabel = 'Simulated Time [s]'
tend = 2.0
xlim = [0.0, tend]

units = {}
quantities = {}
data = {}


# ----------------------------------------------------------------------------
# Read in selected chid_devc.csv files
# ----------------------------------------------------------------------------
#
# Read in data from chid_devc.csv for each solver
#
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


# ----------------------------------------------------------------------------
# print Statistics about number of pressure iterations
# ----------------------------------------------------------------------------
for solver in solvers:
    pres_ite_max = max(data[solver][20:, 3])
    pres_ite_mean = np.mean(data[solver][20:, 3])
    print("Max  number of pressure iterations for solver {:<13}: {:5.0f}  ".
          format(solver, pres_ite_max))
    print("Mean number of pressure iterations for solver {:<13}: {:5.0f}\n".
          format(solver, pres_ite_mean))


# ----------------------------------------------------------------------------
# Plots for fft_default
# ----------------------------------------------------------------------------
widths = [1.5, 1.5]
colors = ['r', 'k']
styles = ['-', '--']
selection = ['fft_default', 'fft_default_tp']
labels = ['FFT default no TP',
          'FFT default with TP']
nleg = 1

#
# plot PRESSURE trace
#
cols = [1]
title = 'Pressure'
ylabel = 'Pressure [Pa]'
ylim = [-0.35, 0.15]
name = 'pressure_trace_fft_default'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)

#
# plot VELOCITY ERROR
#
cols = [2]
title = 'Velocity Error'
ylabel = 'Error [m/s]'
ylim = [1e-18, 1e-0]
name = 'velocity_error_fft_default'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, True)

#
# plot pressure iterations
#
cols = [3]
title = 'Pressure Iterations'
ylabel = 'Number of Iterations'
ylim = [0.0, 100.0]
name = 'pressure_iterations_fft_default'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)


# ----------------------------------------------------------------------------
# Plots for fft_tol-5
# ----------------------------------------------------------------------------
widths = [1.5, 1.5]
colors = ['r', 'k']
styles = ['-', '--']
selection = ['fft_tol-5', 'fft_tol-5_tp']
labels = ['FFT tol=1E-5 no TP',
          'FFT tol=1E-5 with TP']
nleg = 1

#
# Print course of pressure
#
cols = [1]
title = 'Pressure'
ylabel = 'Pressure [Pa]'
ylim = [-0.35, 0.15]
name = 'pressure_trace_fft_tol-5'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)

#
# For each solver print MAXIMUM VELOCITY ERROR
#
cols = [2]
title = 'Velocity Error'
ylabel = 'Error [m/s]'
ylim = [1e-18, 1e-0]
name = 'velocity_error_fft_tol-5'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, True)

#
# For each solver print PRESSURE ITERATIONS
#
cols = [3]
title = 'Pressure Iterations'
ylabel = 'Number of Iterations'
ylim = [0.0, 100.0]
name = 'pressure_iterations_fft_tol-5'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)


# ----------------------------------------------------------------------------
# Plots for ulmat
# ----------------------------------------------------------------------------
widths = [1.5, 1.5]
colors = ['r', 'k']
styles = ['-', '--']
selection = ['ulmat_default', 'ulmat_tol-5']
labels = ['ULMAT default', 'ULMAT tol=1E-5']
nleg = 1

#
# Print course of pressure
#
cols = [1]
title = 'Pressure'
ylabel = 'Pressure [Pa]'
ylim = [-0.35, 0.15]
name = 'pressure_trace_ulmat'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)

#
# For each solver print MAXIMUM VELOCITY ERROR
#
cols = [2]
title = 'Velocity Error'
ylabel = 'Error [m/s]'
ylim = [1e-18, 1e-0]
name = 'velocity_error_ulmat'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, True)

#
# For each solver print PRESSURE ITERATIONS
#
cols = [3]
title = 'Pressure Iterations'
ylabel = 'Number of Iterations'
ylim = [0.0, 100.0]
name = 'pressure_iterations_ulmat'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)

# ----------------------------------------------------------------------------
# Plots for unstructured solvers
# ----------------------------------------------------------------------------
widths = [1.5, 1.5, 1.5]
colors = ['c', 'b', 'g']
styles = ['-', '--', ':']
selection = ['uglmat', 'uscarc_insep', 'ulmat_tol-5']
labels = ['UGLMAT', 'inseparable USCARC', 'ULMAT tol=1E-5']
nleg = 3

#
# Print course of pressure
#
cols = [1]
title = 'Pressure'
ylabel = 'Pressure [Pa]'
ylim = [-0.35, 0.15]
name = 'pressure_trace_unstructured'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)

#
# For each solver print MAXIMUM VELOCITY ERROR
#
cols = [2]
title = 'Velocity Error'
ylabel = 'Error [m/s]'
ylim = [1e-18, 1e-0]
name = 'velocity_error_unstructured'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, True)

#
# For each solver print PRESSURE ITERATIONS
#
cols = [3]
title = 'Pressure Iterations'
ylabel = 'Number of Iterations'
ylim = [0.0, 100.0]
name = 'pressure_iterations_unstructured'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)


# ----------------------------------------------------------------------------
# Plots for unstructured global solvers
# ----------------------------------------------------------------------------
widths = [1.5, 1.5]
colors = ['c', 'b']
styles = ['-', '--']
selection = ['uglmat', 'uscarc_insep']
labels = ['UGLMAT', 'inseparable USCARC']
nleg = 2

#
# Print course of pressure
#
cols = [1]
title = 'Pressure'
ylabel = 'Pressure [Pa]'
ylim = [-0.35, 0.15]
name = 'pressure_trace_unstructured'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)

#
# For each solver print MAXIMUM VELOCITY ERROR
#
cols = [2]
title = 'Velocity Error'
ylabel = 'Error [m/s]'
ylim = [1e-18, 1e-0]
name = 'velocity_error_unstructured_global'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, True)

#
# For each solver print PRESSURE ITERATIONS
#
cols = [3]
title = 'Pressure Iterations'
ylabel = 'Number of Iterations'
ylim = [0.0, 100.0]
name = 'pressure_iterations_unstructured_global'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)

# ----------------------------------------------------------------------------
# Plots for all solvers
# ----------------------------------------------------------------------------
widths = [1.5, 1.5, 1.5, 1.5, 1.5]
colors = ['r', 'g', 'k', 'c', 'b']
styles = ['-', '-', '-','-', '-']
selection = ['fft_default', 'fft_tol-5', 'fft_tol-5_tp', 'uglmat', 'uscarc_insep']
labels = ['FFT default', 'FFT tol=1E-5', 'FFT tol=1E-5 with TP',
          'UGLMAT', 'inseparable USCARC']
nleg = 2

#
# plot MAXIMUM VELOCITY ERROR
#
cols = [2]
title = 'Velocity Error'
ylabel = 'Error [m/s]'
ylim = [1e-18, 1e-0]
name = 'velocity_error_all'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, True)

#
# plot CPU time
#
cols = [4]
title = 'CPU time'
ylabel = 'CPU time [s]'
ylim = [0.0, 1200.0]
name = 'cpu_all'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)

