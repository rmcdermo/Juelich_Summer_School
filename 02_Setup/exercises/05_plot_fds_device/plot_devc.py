# load module for plotting
import matplotlib.pyplot as plt
# load module for numerics, here used for data read-in
import numpy as np

# define file containing DEVC data
devc_file = './data_fds_couch/couch_devc.csv'

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
    print(" - quantity {} with units {}".format(quantities[i], units[i]))

# read DEVC data
data = np.loadtxt(devc_file, delimiter=',', skiprows=2)

# structure of data array: data[row, column], i.e. data[output step index, devc index]

# create a plot of the first devcice data
fig, ax = plt.subplots()
ax.plot(data[:,0], data[:,1])
plt.xlabel("time [s]")
plt.ylabel("{} [{}]".format(quantities[1], units[1]))
plt.show()
fig.clf()

# compute the integral of HRRPUV (8th device with id 7)
sum = 0
partialsum = np.zeros(len(data[:,7]))
for i in range(len(data[:,7]) - 1):
    dq = data[i,7]
    dt = data[i+1,0] - data[i,0]
    sum += dq * dt
    partialsum[i] = sum
# note last element of partialsum is a copy of the previous one
partialsum[-1] = partialsum[-2]

# plot HRRPUV and partialsum
fig, ax1 = plt.subplots()
ln1 = ax1.plot(data[:,0], data[:,7], label='hrrpuv', color='red')
ax1.set_ylabel("{} [{}]".format(quantities[7], units[7]))

ax2 = ax1.twinx()
ln2 = ax2.plot(data[:,0], partialsum, label='energy', color='blue')
ax2.set_ylabel("energy [kJ/m3]")

lns = ln1 + ln2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs)

ax1.set_xlabel("time [s]")

plt.tight_layout()
plt.show()
ax1.cla()
ax2.cla()

# create plots for each device and save to file
for i in range(1, len(quantities)):
    plt.plot(data[:, 0], data[:, i])
    plt.xlabel("time [s]")
    plt.ylabel("{} [{}]".format(quantities[i], units[i]))
    plt.savefig("devc_{:02}_{}.png".format(i, quantities[i]))
    plt.clf()
