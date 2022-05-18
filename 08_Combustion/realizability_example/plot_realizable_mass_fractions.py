#!/usr/bin/python
#McDermott
#2016-02-01 20:52:39

# from __future__ import division # make floating point division default as in Matlab, e.g., 1/2=0.5
import math
import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],'size':16})

# read data from _devc file
M = np.genfromtxt('realizable_mass_fractions_devc.csv', delimiter=',', skip_header=1, names=True)
t = M['Time']
YF = M['YF']
YA = M['YA']
YP = M['YP']
SUMZ = M['SUMZ']
SUMY = M['SUMY']

# plot fds results
plt.figure()
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.95)
plt.subplots_adjust(bottom=0.175)
plt.subplots_adjust(top=0.95)

marker_style = dict(color='black', linestyle=':', marker='o', fillstyle='none', markersize=5)
plt.plot(t,YF,label='YF',**marker_style)

marker_style = dict(color='red', linestyle=':', marker='o', fillstyle='none', markersize=5)
plt.plot(t,YA,label='YA',**marker_style)

marker_style = dict(color='blue', linestyle=':', marker='o', fillstyle='none', markersize=5)
plt.plot(t,YP,label='YP',**marker_style)

marker_style = dict(color='green', linestyle='-', marker='o', fillstyle='none', markersize=5)
plt.plot(t,SUMZ,label='SUMZ',**marker_style)

marker_style = dict(color='cyan', linestyle='-', marker='o', fillstyle='none', markersize=5)
plt.plot(t,SUMY,label='SUMY',**marker_style)

marker_style = dict(color='magenta', linestyle='-', marker='o', fillstyle='none', markersize=5)
plt.plot(t,YF+YA+YP,label='SUMZ2',**marker_style)


plt.axis([min(t), max(t), 0, 1.1])
plt.xlabel('time (s)')
plt.ylabel('mass fraction')
plt.legend(loc='upper right', numpoints=1, frameon=True)
#plt.show()
plt.savefig('realizability_example.pdf', format='pdf')
plt.close()

