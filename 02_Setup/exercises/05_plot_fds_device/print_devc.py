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

# print the first 10 time stamp values:
print("-- first 10 time stamp values:")
print(data[:10, 0])

# print the first 10 values of first devc:
print("-- first 10 values of device {} in {}: ".format(quantities[1], units[1]))
print(data[:10, 1])

# print the first 10 values of second devc:
print("-- first 10 values of device {} in {}: ".format(quantities[2], units[2]))
print(data[:10, 2])