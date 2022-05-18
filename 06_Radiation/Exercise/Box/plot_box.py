#----------------
# Summer School in Fire Dynamics Modelling
# Simo Hostikka, Aalto University
#
# Define which case you want to do by setting these logical variables 0 or 1
PlotExact = 1
PlotX = 1
PlotY = 0
PlotZ = 0
#
#-------------------------

# load module for plotting
import matplotlib.pyplot as plt
# load module for numerics, here used for data read-in
import numpy as np

# create a plot of x and y data
fig, ax = plt.subplots()

# read in exact solutionExact_Phi = csvread('exact_f.csv',1,0);
exact_file = 'Exact_F.csv'
Exact_F = np.loadtxt(exact_file, delimiter=',', skiprows=1)
xyz = Exact_F[:,0];

if(PlotExact):
	ax.plot(xyz,Exact_F[:,1],'o',label='Exact', color='black',linewidth=1)

if(PlotX):
	devc_file_x = 'radiation_box__50__100_devc.csv'
	data = np.loadtxt(devc_file_x, delimiter=',', skiprows=2)
	M_x = data[1,1:21];
	ax.plot(xyz,M_x,'x--',label='X',color='blue')

if(PlotY):
	devc_file_y = 'radiation_box__50__100_y_devc.csv'
	data = np.loadtxt(devc_file_y, delimiter=',', skiprows=2)
	M_y = data[1,21:41];
	ax.plot(xyz,M_y,'-.',label='Y',color='red')

if(PlotZ):
	devc_file_z = 'radiation_box__50__100_z_devc.csv'
	data = np.loadtxt(devc_file_z, delimiter=',', skiprows=2)
	M_z = data[1,41:61];
	ax.plot(xyz,M_z,label='Z',color='green')
	
plt.xlabel("Position [m]")
plt.ylabel("Heat flux [kW/m2]")
plt.legend()
plt.show()
fig.clf()
