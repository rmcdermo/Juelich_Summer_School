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

# read in create analytical solution
time = np.arange(0,16,1)
Tinf = 500
rho = 300
cp = 1400
d = 0.0006
h = 20
T0 = 20
T = Tinf - (Tinf-T0)*np.exp((-2*h*time)/(d*rho*cp))

# create figure
f, ax = plt.subplots()

# plot experimental data
ax.plot(time,T,'b-',label='Exact')

# read and plot fds data
fds_file = 'curtain_devc.csv'
exists = os.path.isfile(fds_file)
if exists:
        FDS_data = np.loadtxt(fds_file, delimiter=',', skiprows=2)
        ax.plot(FDS_data[:,0],FDS_data[:,1],'k--',label='FDS')

plt.ylabel("T (C)")
plt.xlabel("Time (s)")
ax.grid()
ax.legend()
plt.show()
