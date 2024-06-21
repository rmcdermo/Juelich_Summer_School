#!/usr/bin/python
#McDermott
#2016-02-01 20:52:39

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read data from _devc file
M = pd.read_csv("hrrpuv_reac_simple_devc.csv", header=1)
t = M['Time']
hrrpuv = M['hrrpuv']
q1 = M['q1']

# plot fds results
plt.figure

marker_style = dict(color='blue', linestyle=':', marker='*', fillstyle='none', markersize=5)
plt.plot(t,hrrpuv,label='hrrpuv',**marker_style)

marker_style = dict(color='red', linestyle=':', marker='o', fillstyle='none', markersize=5)
plt.plot(t,q1,label='q1',**marker_style)

plt.axis([min(t), max(t), min(q1), 1.1*max(q1)])
plt.xlabel('time (s)')
plt.ylabel('$\dot{q}^{\prime\prime\prime}$ (kW/m$^3$)')
plt.legend(loc='upper right', numpoints=1, frameon=True)
#plt.show()
plt.savefig('hrrpuv_reac_simple.pdf', format='pdf')
plt.close()

