#----------------
# Summer School in Fire Dynamics Modelling
# Simo Hostikka, Aalto University
#-------------------------

# load module for plotting
import matplotlib.pyplot as plt
# load module for numerics
import numpy as np
import os.path
import math

# create figure
f, ax = plt.subplots()

# read in analytical solution
exact_file = 'heat_conduction_exact.csv'
exists = os.path.isfile(exact_file)
if exists:
        Exact_data = np.loadtxt(exact_file, delimiter=',', skiprows=1)
        ax.plot(Exact_data[:,0],Exact_data[:,[1,5,6]],'o',mfc='w',label=['Back','2 cm','Front'])

#		label=['Back','8 cm','6 cm','4 cm','2 cm','Front'])

# read and plot fds data
fds_file = 'heat_conduction_devc.csv'
exists = os.path.isfile(fds_file)
if exists:
        FDS_data = np.loadtxt(fds_file, delimiter=',', skiprows=2)
        ax.plot(FDS_data[:,0],FDS_data[:,[1,5,6]],'-',label=['FDS Back','FDS 2 cm','FDS Front'])

plt.ylabel("T (C)")
plt.xlabel("Time (s)")
ax.grid()
ax.legend(loc='center right')
plt.show()
