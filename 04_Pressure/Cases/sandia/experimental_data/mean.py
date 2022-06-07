# load module for plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as fnt
# load module for numerics, here used for data read-in
import numpy as np


def plot_selection(selection, indices, title, ylabel, ylim, label, name,
                   semilogy):

    widths = [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75]
    colors = ['brown', 'r', 'c', 'b', 'y', 'g', 'k']
    styles = ['--', '-', '--', '-', '--', '-', '--']

    ax = plt.subplot(111)

    # Shrink current axis's height by 10% on the bottom
    # Put a legend below current axis

    j = 0
    for s in selection:
        for i in indices:
            if semilogy:
                plt.semilogy(data[s][:, 0],
                             data[s][:, i],
                             linewidth=widths[j],
                             linestyle=styles[j],
                             color=colors[j],
                             label=label[j])
            else:
                plt.plot(data[s][:, 0],
                         data[s][:, i],
                         linewidth=widths[j],
                         linestyle=styles[j],
                         color=colors[j],
                         label=label[j])
            j = j+1

    legsize = fnt.FontProperties(size=10)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2,
                     box.width, box.height * 0.8])
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.42), prop=legsize,
              fancybox=True, shadow=False, ncol=4)

    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=18)
    plt.xlim(xlim[0], xlim[1])
    plt.ylim(ylim[0], ylim[1])
    plt.tick_params(labelsize=10)
    plt.savefig('pictures/' + name + '.png')
    plt.clf()


result_dir = './'
geometry = 'sandia'
solvers = ['fft_tight']
xlabel = 'Simulated Time [s]'
xlim = [-0.5, 0.5]

units = {}
quantities = {}
data = {}

#
# Read in data from chid_devc.csv for each solver
#
for solver in solvers:

    # get name of devices file for selected solver
    devc_solver = result_dir + geometry + '_' + solver + '_line.csv'
    devc_solver = 'Sandia_CH4_1m_Test14_U_zp5.csv'

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
    data_solver = np.loadtxt(devc_solver, delimiter=',', skiprows=1)

    units[solver] = units_solver
    quantities[solver] = quantities_solver
    data[solver] = data_solver

#
# For each solver print MAXIMUM VELOCITY ERROR
#
selection = solvers
indices = [1]
title = 'Wp5'
ylabel = 'Error [m/s]'
ylim = [-0.3, 0.3]
label = solvers
name = 'Wp5'
plot_selection(selection, indices, title, ylabel, ylim, label, name, False)
