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

# read data from _devc file
M = np.genfromtxt('hrrpuv_reac_simple_devc.csv', delimiter=',', skip_header=1, names=True)
t = M['Time']
q1 = M['q1']

# plot fds results
plt.figure

marker_style = dict(color='red', linestyle=':', marker='o', fillstyle='none', markersize=5)
plt.plot(t,q1,label='q1',**marker_style)

plt.axis([min(t), max(t), min(q1), 1.1*max(q1)])
plt.xlabel('time (s)')
plt.ylabel('q1 (kW/m$^3$)')
plt.legend(loc='upper right', numpoints=1, frameon=True)
#plt.show()
plt.savefig('q1.pdf', format='pdf')
plt.close()

