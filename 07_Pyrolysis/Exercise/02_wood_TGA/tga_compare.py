#----------------
# Summer School in Fire Dynamics Modelling
# Simo Hostikka, Aalto University
#-------------------------

# load module for plotting
import matplotlib.pyplot as plt
# load module for numerics, here used for data read-in
import numpy as np
import os.path

# read in tga data;
tga_file = 'Wood_TGA_10Kmin_N2.csv'
tga_data = np.loadtxt(tga_file, delimiter=',', skiprows=2)
T_tga = tga_data[:,1];
M_tga = tga_data[:,2];
MLR_tga = tga_data[:,3];

# create figure
f, axarr = plt.subplots(2,sharex=True)

# plot experimental data
axarr[0].plot(T_tga,M_tga,'-',label='TGA',color='blue')
axarr[1].plot(T_tga,MLR_tga,'-',label='TGA',color='blue')
f.subplots_adjust(hspace=0)

# read and plot fds data
fds_file = 'wood_tga_tga.csv'
exists = os.path.isfile(fds_file)
if exists:
        FDS_data = np.loadtxt(fds_file, delimiter=',', skiprows=2)
        lfds1=axarr[0].plot(FDS_data[:,1],FDS_data[:,2],'k--',label='FDS')
        lfds2=axarr[1].plot(FDS_data[:,1],FDS_data[:,6],'k--',label='FDS')

axarr[0].set_ylabel("Mass (-)")
axarr[0].grid()
axarr[1].set_xlabel("T (C)")
axarr[1].set_ylabel("MLR (1/s)")
axarr[1].legend()
axarr[1].grid()
plt.show()
