#----------------
# Summer School in Fire Dynamics Modelling
# Simo Hostikka, Aalto University
#
# Plot gas emissivity, assuming RADIANCE ouput quantity
#-------------------------

# load module for plotting
import matplotlib.pyplot as plt
# load module for numerics, here used for data read-in
import numpy as np


#Read data
devc_file = 'hottel_array_devc.csv'
data = np.loadtxt(devc_file, delimiter=',', skiprows=2)
R = data[2,1:11];

T = [200,300,400,500,600,800,1000,1200,1600,2000]
emissivity = np.zeros(len(T))
for i in range(0,10):
    sT4 = 5.67E-11*T[i]**4
#    sT4_in = (1-np.exp(-1))*sT4
    emissivity[i] = R[i]/(sT4/np.pi)

# create a plot of x and y data
fig, ax = plt.subplots()

ax.plot(T,emissivity,'o-',label='E',color='blue')
	
plt.axis([100, 5000, 0.001, 1.0])
plt.xscale("log")
plt.xticks([100, 200, 500, 1000, 2000, 5000])
plt.yscale("log")
plt.yticks([0.001, 0.01, 0.1, 1])
plt.xlabel("T [K]")
plt.ylabel("Emissivity ")
#plt.legend()
plt.grid(True)
plt.show()
fig.clf()
