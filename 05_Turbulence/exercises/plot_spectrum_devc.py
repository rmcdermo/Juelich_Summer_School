# load module for plotting
import matplotlib.pyplot as plt
# load module for numerics, here used for data read-in
import numpy as np

############################
##### change parameters here

# define file containing DEVC data
# devc_files = ['rc01_coarse_fft_devc.csv', 'rc01_medium_fft_devc.csv', 'rc01_fine_fft_devc.csv' ] 
devc_file = './rc01_coarse_fft_devc.csv'

# define which device is shown
device_id = 11

# time interval used for fourier analysis
t_start = 80
t_end   = 110

##### stop changing, unless on purpose
######################################

# open file, read in the first two lines containing the quantities and units, finally close the file again
fin = open(devc_file, 'r')
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
data = np.loadtxt(devc_file, delimiter=',', skiprows=2)


# create a plot of the first device data
fig, ax = plt.subplots()
ax.plot(data[:,0], data[:,device_id])
ax.axvline(t_start, color='red')
ax.axvline(t_end, color='red')
plt.xlabel("time [s]")
plt.ylabel("{} [{}]".format(quantities[device_id], units[device_id]))
plt.show()
plt.close(fig)

istart = np.where(data[:,0] > t_start)[0][0]
iend = np.where(data[:,0] > t_end)[0][0]
time_series_x = data[istart:iend, 0]
time_series_y = data[istart:iend, device_id]

n = len(time_series_x)
spec = np.fft.fft(time_series_y)
dt = float(t_end - t_start)/n

freq = np.fft.fftfreq(n, dt)

plt.loglog(freq[1:n//2], (np.abs(spec)**2)[1:n//2],linewidth=1)
plt.title(devc_file[2:-4])
plt.ylabel('power [-]')
plt.xlabel('frequency [Hz]')
plt.show()



