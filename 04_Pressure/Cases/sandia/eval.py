import matplotlib.pyplot as plt
import matplotlib.font_manager as fnt
# load module for numerics, here used for data read-in
import numpy as np


# -----------------------------------------------------------------------------------------------
# Read in experimental data
# -----------------------------------------------------------------------------------------------
def read_exp(name):

    data_solver = np.loadtxt(name, delimiter=',', skiprows=1)
    exp_data['exp'] = data_solver


# -----------------------------------------------------------------------------------------------
# Plot selection of data from chid_devc.csv
# -----------------------------------------------------------------------------------------------
def plot_selection(selection, indices, title, ylabel, ylim, label, name,
                   semilogy):

    widths = [1, 1, 1, 1]
    colors = ['r', 'g', 'c', 'b']
    styles = ['-', '-', '-', '-']

    plot_file = 'plots/' + name + '.png'

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
                plt.plot(exp_data['exp'][:, 0],
                         exp_data['exp'][:, 1],
                         linewidth=0.75,
                         linestyle='--',
                         color='grey')
            j = j+1

    legsize = fnt.FontProperties(size=10)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2,
                     box.width, box.height * 0.8])
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.42), prop=legsize,
              fancybox=True, shadow=False, ncol=5)

    plt.xlabel(xlabel, fontsize=11)
    plt.ylabel(ylabel, fontsize=11)
    plt.title(title, fontsize=18)
    plt.xlim(xlim[0], xlim[1])
    plt.ylim(ylim[0], ylim[1])
    plt.tick_params(labelsize=10)
    plt.savefig(plot_file)
    plt.clf()

    print('Plotting file {}'.format(plot_file))


# -----------------------------------------------------------------------------------------------
# Basic definitions, define solvers to compare
# -----------------------------------------------------------------------------------------------
result_dir = 'results/'
geometry = 'sandia'
solvers = ['fft_default', 'ulmat', 'glmat', 'scarc']

xlabel = 'Simulated Time [s]'
xlim = [-0.5, 0.5]

units = {}
quantities = {}
data = {}
exp_data = {}


# -----------------------------------------------------------------------------------------------
# Read in data from chid_devc.csv for each solver
# -----------------------------------------------------------------------------------------------
for solver in solvers:

    # get name of devices file for selected solver
    devc_solver = result_dir + geometry + '_' + solver + '_line.csv'

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


# -----------------------------------------------------------------------------------------------
# For each solver print MAXIMUM VELOCITY ERROR
# -----------------------------------------------------------------------------------------------
selection = solvers
label = ['FFT default', 'ULMAT', 'GLMAT', 'SCARC']
indices = [2]
title = 'Wp5'
ylabel = ' '
ylim = [0, 5]
name = 'Wp5'
read_exp('experimental_data/Sandia_CH4_1m_Test14_W_zp5.csv')
plot_selection(selection, indices, title, ylabel, ylim, label, name, False)

#
# For each solver print PRESSURE ITERATIONS
#
selection = solvers
indices = [5]
title = 'Up5'
ylabel = ' '
ylim = [-0.5, 0.5]
label = solvers
name = 'Up5'
read_exp('experimental_data/Sandia_CH4_1m_Test14_U_zp5.csv')
plot_selection(selection, indices, title, ylabel, ylim, label, name, False)
