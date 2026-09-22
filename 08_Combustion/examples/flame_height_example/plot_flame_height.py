#!/usr/bin/python
#McDermott
#2016-02-01 20:52:39

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read data from _line file
M = pd.read_csv('Qs=1_RI=05_line.csv', header=1)
z1 = M['Height']
hrrpul1 = M['HRRPUL']

M = pd.read_csv('zeta_0_line.csv', header=1)
z2 = M['Height']
hrrpul2 = M['HRRPUL']

# plot fds results
plt.figure

marker_style = dict(color='blue', linestyle='-', linewidth=2, marker='*', fillstyle='none', markersize=5)
plt.semilogx(hrrpul1,z1,label='$\zeta_0=1$',**marker_style)

marker_style = dict(color='red', linestyle='-', linewidth=2, marker='o', fillstyle='none', markersize=5)
plt.semilogx(hrrpul2,z2,label='$\zeta_0=0$',**marker_style)

plt.axis([1e-1, 1e4, 0, 9])
plt.ylabel('height-z (m)')
plt.xlabel('HRRPUL (kW/m)')
plt.legend(loc='upper right', numpoints=1, frameon=True)
#plt.show()
plt.savefig('hrrpul.pdf', format='pdf')
plt.close()

