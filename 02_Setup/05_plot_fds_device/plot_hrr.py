# load module for plotting
import matplotlib.pyplot as plt
# load module for numerics, here used for data read-in
import numpy as np

# define file containing HRR data
devc_file = './data_fds_couch/couch_hrr.csv'

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

# read data
data = np.loadtxt(devc_file, delimiter=',', skiprows=2)

# create plots for each quantity and save to file
for i in range(1, len(quantities)):
    fig, ax = plt.subplots()
    ax.plot(data[:, 0], data[:, i])
    plt.xlabel("time [s]")
    plt.ylabel("{} [{}]".format(quantities[i], units[i]))
    fig.savefig("hrr_{:02}_{}.png".format(i, quantities[i]))
    plt.close(fig)

# compute the integral of HRR
sum = 0
partialsum_hrr = np.zeros(len(data[:,1]))
for i in range(len(data[:,1]) - 1):
    dq = data[i,1]
    dt = data[i+1,0] - data[i,0]
    sum += dq * dt
    partialsum_hrr[i] = sum
# note last element of partialsum is a copy of the previous one
partialsum_hrr[-1] = partialsum_hrr[-2]

# plot HRR and partialsum
fig, ax1 = plt.subplots()
ln1 = ax1.plot(data[:,0], data[:,1], label='HRR', color='red')
ax1.set_ylabel("{} [{}]".format(quantities[1], units[1]))

ax2 = ax1.twinx()
ln2 = ax2.plot(data[:,0], partialsum_hrr, label='energy', color='blue')
ax2.set_ylabel("energy [kJ]")

lns = ln1 + ln2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs)

ax1.set_xlabel("time [s]")

plt.tight_layout()
plt.savefig("05_hrr_sum_hrr.pdf")
plt.show()
plt.close(fig)

# HRR and Qs
fig, ax = plt.subplots()
ax.plot(data[:,0], data[:,1], label="{}".format(quantities[1]))

for iq in range(2,5):
    ax.plot(data[:, 0], data[:, iq], label="{}".format(quantities[iq]))

ax.plot(data[:,0], - (data[:,2] + data[:,3] + data[:,4]), label="- sum Qs")

plt.xlabel("time [s]")

plt.legend()
plt.tight_layout()
plt.savefig("05_HRR_Qs.pdf")
plt.show()
plt.close(fig)

# compute the integral of Qs
sum = 0
partialsum_qs = np.zeros(len(data[:,1]))
for i in range(len(data[:,1]) - 1):
    dq = - (data[i,2] + data[i,3] + data[i,4])
    dt = data[i+1,0] - data[i,0]
    sum += dq * dt
    partialsum_qs[i] = sum
# note last element of partialsum is a copy of the previous one
partialsum_qs[-1] = partialsum_qs[-2]

fig, ax1 = plt.subplots()
ln1 = ax1.plot(data[:,0], partialsum_hrr, label='energy by HRR', color='red')
ln2 = ax1.plot(data[:,0], partialsum_qs, label='energy by Qs', color='green')

ax2 = ax1.twinx()
ln3 = ax2.plot(data[:,0], partialsum_hrr - partialsum_qs, label='energy difference', color='blue')

ax1.set_xlabel("time [s]")
ax1.set_ylabel("energy [kJ]")
ax2.set_ylabel("energy difference [kJ]")

lns = ln1 + ln2 + ln3
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs)

plt.savefig("05_hrr_qs_diff.pdf")
plt.show()
plt.close(fig)