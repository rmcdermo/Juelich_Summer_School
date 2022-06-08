#!/usr/bin/python
#McDermott
#2016-02-01 20:52:39

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read data from _hrr file
M = pd.read_csv("hrrpuv_reac_simple_hrr.csv", header=1)
t = M['Time']
Q = M['HRR']

# plot fds results
plt.figure()
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.95)
plt.subplots_adjust(bottom=0.175)
plt.subplots_adjust(top=0.95)

marker_style = dict(color='blue', linestyle=':', marker='*', fillstyle='none', markersize=5)
plt.plot(t,Q,label='HRR',**marker_style)

marker_style = dict(color='red', linestyle='--', marker='', fillstyle='none', markersize=5)
plt.plot(t,50*np.ones_like(t),label='exact',**marker_style)

plt.axis([min(t), max(t), min(Q), 1.1*max(Q)])
plt.xlabel('time (s)')
plt.ylabel('$\dot{Q}$ (kW)')
plt.legend(loc='lower right', numpoints=1, frameon=True)
#plt.show()
plt.savefig('hrr_simple.pdf', format='pdf')
plt.close()

