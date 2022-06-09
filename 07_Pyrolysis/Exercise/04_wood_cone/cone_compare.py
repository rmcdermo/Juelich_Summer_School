#----------------
# Summer School in Fire Dynamics Modelling
# Simo Hostikka, Aalto University
#-------------------------

# load module for plotting
import matplotlib.pyplot as plt
# load module for numerics, here used for data read-in
import numpy as np
import os.path

# read in Cone test data;
cone_file = 'Wood_Cone_35kW.csv'
cone_data = np.loadtxt(cone_file, delimiter=',', skiprows=2)
time   = cone_data[:,0];
HRRPUA = cone_data[:,1];
MLRPUA = cone_data[:,2];

# create figure
f, axarr = plt.subplots(2,sharex=True)

# plot experimental data
axarr[0].plot(time,HRRPUA,'-',label='Exp',color='blue')
axarr[1].plot(time,MLRPUA,'-',label='Exp',color='blue')
f.subplots_adjust(hspace=0)

# read and plot fds data
fds_file = 'wood_cone_35_hrr.csv'
exists = os.path.isfile(fds_file)
if exists:
        FDS_data = np.loadtxt(fds_file, delimiter=',', skiprows=2)
        lfds1=axarr[0].plot(FDS_data[:,0],10*FDS_data[:,1],'k--',label='FDS')
        lfds2=axarr[1].plot(FDS_data[:,0],10*FDS_data[:,11],'k--',label='FDS')

axarr[0].set_ylabel("HRRPUA (kW/m^2)")
axarr[0].grid()
axarr[1].set_xlabel("Time (s)")
axarr[1].set_ylabel("MLRPUA (kg/m^2s)")
axarr[1].legend()
axarr[1].grid()
plt.show()
