#----------------
# Summer School in Fire Dynamics Modelling
# Simo Hostikka, Aalto University
#
# Plot gas emissivity, assuming RADIANCE ouput quantity
#-------------------------

# File names
LBL_file = 'H2O_emissivity_LBL.csv'
FDS_RadCal_basic_file = 'H2O_array_devc.csv'
FDS_RadCal_PATH_file = 'H2O_array_path_devc.csv'
FDS_RadCal_PATH_RADTMP_file = 'H2O_array_path_radtmp_devc.csv'
FDS_WSGG_file = 'H2O_array_wsgg_devc.csv'

# load module for plotting
import matplotlib.pyplot as plt
# load module for numerics, here used for data read-in
import numpy as np
import os.path

T = np.array([300.,400.,500.,600.,800.,1000.,1200.,1600.,2000.,2273.15])
TC = np.zeros(len(T))
TC = T-273.15
# create a plot of x and y data
fig, ax = plt.subplots()

#Read and plot LBL data
data = np.loadtxt(LBL_file, delimiter=',', skiprows=2)
E_LBL = np.zeros(len(T))
for i in range(0,10):
    E_LBL[i] = data[i,1];
ax.plot(TC,E_LBL,'o',label='LBL',color='black')

#Read and plot FDS basic data
exists = os.path.isfile(FDS_RadCal_basic_file)
if exists:
    data = np.loadtxt(FDS_RadCal_basic_file, delimiter=',', skiprows=2)
    E_FDS = np.zeros(len(T))
    for i in range(0,10):
        sT4 = 5.67E-11*T[i]**4
        E_FDS[i] = data[2,i+1]/(sT4/np.pi)
    ax.plot(TC,E_FDS,'-',label='FDS',color='blue')        

#Read FDS with PATH lenght
exists = os.path.isfile(FDS_RadCal_PATH_file)
if exists:
    data = np.loadtxt(FDS_RadCal_PATH_file, delimiter=',', skiprows=2)
    E_FDS = np.zeros(len(T))
    for i in range(0,10):
        sT4 = 5.67E-11*T[i]**4
        E_FDS[i] = data[2,i+1]/(sT4/np.pi)
    ax.plot(TC,E_FDS,'--',label='FDS, PATH',color='green')


#Read FDS with PATH lenght and RADTMP
exists = os.path.isfile(FDS_RadCal_PATH_RADTMP_file)
if exists:
    data = np.loadtxt(FDS_RadCal_PATH_RADTMP_file, delimiter=',', skiprows=2)
    E_FDS = np.zeros(len(T))
    for i in range(0,10):
        sT4 = 5.67E-11*T[i]**4
        E_FDS[i] = data[2,i+1]/(sT4/np.pi)
    ax.plot(TC,E_FDS,'--',label='FDS, PATH+RADTMP',color='red')


#Read FDS with WSGG
exists = os.path.isfile(FDS_WSGG_file)
if exists:
    data_wsgg = np.loadtxt(FDS_WSGG_file, delimiter=',', skiprows=2)
    E_FDS = np.zeros(len(T))
    for i in range(0,10):
        sT4 = 5.67E-11*T[i]**4
        E_FDS[i] = data_wsgg[2,i+1]/(sT4/np.pi)
    ax.plot(TC,E_FDS,'-.',label='FDS, WSGG',color='black')

#plt.axis([100, 2500, 0.01, 1.0])
#plt.xscale("log")
#plt.setp(ax, xticks = [100, 200, 500, 1000, 2000])
#plt.yscale("log")
#plt.yticks([0.01, 0.1, 1])
plt.xlabel("T [C]")
plt.ylabel("Emissivity ")
plt.grid(True)
plt.legend()
plt.show()
#fig.clf()
