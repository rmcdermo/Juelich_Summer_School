#!/usr/bin/python
#McDermott
#2017-07-31 20:52:39

#from __future__ import division # for Python 2.7 make floating point division default as in Matlab, e.g., 1/2=0.5
import math
import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],'size':16})

# consider the reaction
# C3H8 + 5 [ O2 + (0.79/0.21) N2 ] => 3 CO2 + 4 H2O + 5 (0.79/0.21) N2

NU  = np.array([-1, -5, 3, 4])
W   = np.array([44.09562, 31.99880, 44.00950, 18.01528])
H_F = np.array([-2.37E+06, 0, -8.94E+06, -1.34E+07])

HOC = -np.sum(NU*W/W[0]*H_F)
print("HOC Fuel Basis: " + "{:.3e}".format(HOC))

HOC_O2 = HOC*NU[0]/NU[1]*W[0]/W[1]
print("HOC O2 Basis: " + "{:.3e}".format(HOC_O2))













