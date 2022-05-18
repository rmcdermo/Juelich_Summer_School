#!/usr/bin/python
#McDermott
#2016-02-01 20:52:39

from __future__ import division # make floating point division default as in Matlab, e.g., 1/2=0.5
import math
import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],'size':16})

np.seterr(divide='ignore', invalid='ignore')

# read data from _devc file
M = np.genfromtxt('wd_propane_hrr.csv', delimiter=',', skip_header=1, names=True)
t = M['Time']
HRR      = M['HRR']
MLR_FUEL = M['MLR_FUEL']
HOC  = 46334 # kJ/kg
AREA = 1     # m^2

# combustion efficiency
ETA = np.divide(HRR,(MLR_FUEL*HOC*AREA))

# plot fds results
plt.figure

marker_style_1 = dict(color='black', linestyle=':', marker='o', fillstyle='none', markersize=5)
plt.plot(t,ETA, label='', **marker_style_1)

plt.axis([min(t), max(t), 0, 2])
plt.xlabel('time (s)')
plt.ylabel('$\eta$ = Q / (MLR $\\times$ HOC $\\times$ A)')
plt.legend(loc='lower right', numpoints=1, frameon=False)
#plt.show()
plt.savefig('comb_efficiency.pdf', format='pdf')
plt.close()

