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
geometry = 'hpc'
solvers = ['4mesh_4mpi_1omp',
           '4mesh_4mpi_2omp',
           '4mesh_4mpi_4omp',
           '4mesh_2mpi_1omp',
           '4mesh_2mpi_2omp',
           '4mesh_2mpi_4omp']

xlabel = 'Simulated Time [s]'
tend = 2.0
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
# Plots for 4 MPI processes with different number of OpenMP threads
# ---------------------------------------------------------------------------
widths = [1.25, 1.25, 1.25]
colors = ['r', 'g', 'b']
styles = ['-', '-', '-']
styles = ['-', '--', '-.']
selection = ['4mesh_4mpi_1omp',
             '4mesh_4mpi_2omp',
             '4mesh_4mpi_4omp']
labels = ['1 thread',
          '2 thread',
          '4 thread']
nleg = 3


#
# For each solver print CPU time
#
cols = [1]
title = '4 MPI processes'
ylabel = 'CPU [s]'
ylim = [0.0, 300.0]
name = 'cpu_4mpi'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)


# ---------------------------------------------------------------------------
# Plots for 2 MPI processes with different number of OpenMP threads
# ---------------------------------------------------------------------------
widths = [1.25, 1.25, 1.25]
colors = ['r', 'g', 'b']
styles = ['-', '--', '-.']
selection = ['4mesh_2mpi_1omp',
             '4mesh_2mpi_2omp',
             '4mesh_2mpi_4omp']
labels = ['1 thread',
          '2 thread',
          '4 thread']
nleg = 3


#
# For each solver print CPU time
#
cols = [1]
title = '2 MPI processes'
ylabel = 'CPU [s]'
ylim = [0.0, 300.0]
name = 'cpu_2mpi'
plot_selection(selection, cols, title, ylabel, ylim, labels, name, nleg, False)
