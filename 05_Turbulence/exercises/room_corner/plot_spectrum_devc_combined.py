# load module for plotting
import matplotlib.pyplot as plt
# load module for numerics, here used for data read-in
import numpy as np

############################
##### change parameters here

# define file containing DEVC data
devc_files = ['rc01_coarse_fft_devc.csv', 'rc01_medium_fft_devc.csv', 'rc01_fine_fft_devc.csv' ]

# define which device is shown
device_id = 11

# time interval used for fourier analysis
t_start = 117
t_end   = 119

# turn on / off plotting parts
plot_data = False
plot_data_zoom = True
plot_spectrum = False
plot_histogram = False

##### stop changing, unless on purpose
######################################

# open file, read in the first two lines containing the quantities and units, finally close the file again
fin = open(devc_files[0], 'r')
units_line = fin.readline()
quantities_line = fin.readline()
fin.close()

# split the two lines by comma to determie the column data, results are now lists
units = units_line.strip().split(',')
quantities = quantities_line.strip().split(',')

# remove quotes and end-of-line characters
for i in range(len(quantities)):
    units[i] = units[i].strip().strip("\"")
    quantities[i] = quantities[i].strip().strip("\"")

# plot both lists:
print("-- found quantities: ")
for i in range(len(quantities)):
    print(" - {:2d}, quantity {} with units {}".format(i, quantities[i], units[i]))

# read DEVC data
# structure of data array: data[row, column], i.e. data[output step index, devc index]
data=[]
for i in range(len(devc_files)):
    data.append(np.loadtxt(devc_files[i], delimiter=',', skiprows=2))

if plot_data:
    fig, ax = plt.subplots()

    for i in range(len(devc_files)):
        ax.plot(data[i][:,0], data[i][:,device_id], label=devc_files[i], alpha=0.5)

    ax.axvline(t_start, color='red')
    ax.axvline(t_end, color='red')
    plt.xlabel("time [s]")
    plt.ylabel("{} [{}]".format(quantities[device_id], units[device_id]))
    plt.legend()
    plt.show()
    plt.close(fig)

if plot_data_zoom:
    fig, ax = plt.subplots()

    for i in range(len(devc_files)):
        istart = np.where(data[i][:, 0] > t_start)[0][0]
        iend = np.where(data[i][:, 0] > t_end)[0][0]

        ax.plot(data[i][istart:iend,0], data[i][istart:iend,device_id], marker='o', label=devc_files[i], alpha=0.5)

    ax.axvline(t_start, color='red')
    ax.axvline(t_end, color='red')
    plt.xlabel("time [s]")
    plt.ylabel("{} [{}]".format(quantities[device_id], units[device_id]))
    plt.legend()
    plt.show()
    plt.close(fig)

if plot_spectrum:
    fig, ax = plt.subplots()
    for i in range(len(devc_files)):

        istart = np.where(data[i][:, 0] > t_start)[0][0]
        iend = np.where(data[i][:, 0] > t_end)[0][0]

        time_series_x = data[i][istart:iend, 0]
        time_series_y = data[i][istart:iend, device_id]

        n = len(time_series_x)
        spec = np.fft.fft(time_series_y)
        dt = float(t_end - t_start)/n
        freq = np.fft.fftfreq(n, dt)

        ax.loglog(freq[1:n/2], (np.abs(spec)**2)[1:n/2], label=devc_files[i], alpha=0.8)

    plt.legend()
    plt.ylabel('power [1]')
    plt.xlabel('frequency [Hz]')
    plt.show()
    plt.close(fig)

if plot_histogram:
    fig, ax = plt.subplots()
    for i in range(len(devc_files)):
        istart = np.where(data[i][:, 0] > t_start)[0][0]
        iend = np.where(data[i][:, 0] > t_end)[0][0]

        time_series_x = data[i][istart:iend, 0]
        time_series_y = data[i][istart:iend, device_id]

        diff = time_series_y[1:] - time_series_y[:-1]

        hist, edges = np.histogram(diff, bins=50)
        ax.plot(edges[:-1], hist, label=devc_files[i])

    ax.set_yscale("log")
    plt.legend()
    plt.ylabel('probability')
    plt.xlabel('fluctuation [m/s]')
    plt.show()
    plt.close(fig)
