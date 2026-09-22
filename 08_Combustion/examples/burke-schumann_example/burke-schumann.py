#!/usr/bin/python
#McDermott
#2017-07-31 20:52:39

import numpy as np
import matplotlib.pyplot as plt

# mass stoichiometric coefficient
s = 17.55
Cp = 1320
Hc = 50010.e3
T0 = 293

# mixture fraction space
f = np.linspace(0,1,1000)

def Fuel_Composition(f,s):
    f_st = 1./(1.+s)
    Y_Fuel = np.zeros(np.size(f))
    for i in range(len(f)):
        if f[i]<=f_st:
            Y_Fuel[i] = 0.
        else:
            Y_Fuel[i] = ((1.+s)*f[i]-1.)/s
    return Y_Fuel

def Product_Composition(f,s):
    f_st = 1./(1.+s)
    Y_Prod = np.zeros(np.size(f))
    for i in range(len(f)):
        if f[i]<=f_st:
            Y_Prod[i] = (1.+s)*f[i]
        else:
            Y_Prod[i] = (1.+s)/s * (1.-f[i])
    return Y_Prod

def Flame_Temperature(f,s,T0,Cp,Hc):
    f_st = 1./(1.+s)
    T = np.zeros(np.size(f))
    Y_Fuel = Fuel_Composition(f,s)
    for i in range(len(f)):
        if f[i]<=f_st:
            T[i] = T0 + f[i]*Hc/Cp
        else:

            T[i] = T0 + (f[i]-Y_Fuel[i])*Hc/Cp
    return T

Y_F = Fuel_Composition(f,s)
Y_P = Product_Composition(f,s)
Y_A = 1. - Y_F - Y_P
T   = Flame_Temperature(f,s,T0,Cp,Hc)

# plot species
plt.figure

marker_style = dict(color='black', linestyle='-', marker='', fillstyle='none', markersize=5)
plt.plot(f,Y_F,label='Fuel',**marker_style)

marker_style = dict(color='blue', linestyle='-', marker='', fillstyle='none', markersize=5)
plt.plot(f,Y_A,label='Air',**marker_style)

marker_style = dict(color='red', linestyle='-', marker='', fillstyle='none', markersize=5)
plt.plot(f,Y_P,label='Products',**marker_style)

plt.axis([0, 1, -0.1, 1.1])
plt.xlabel('mixture fraction')
plt.ylabel('species')
plt.legend(loc='upper center', numpoints=1, frameon=True)
#plt.show()
plt.savefig('species.pdf', format='pdf')
plt.close()

# plot temperature
plt.figure

marker_style = dict(color='red', linestyle='-', marker='', fillstyle='none', markersize=5)
plt.plot(f,T-T0,**marker_style)

plt.axis([0, 1, 20, 2200])
plt.xlabel('mixture fraction')
plt.ylabel('temperature ($^\\circ$C)')
#plt.show()
plt.savefig('temperature.pdf', format='pdf')
plt.close()













