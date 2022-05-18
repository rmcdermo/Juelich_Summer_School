#!/usr/bin/python
#McDermott
#2016-02-01 20:52:39

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Bitstream Vera Sans'],'size':16})

# read data from _line file
M = np.genfromtxt('Qs=1_RI=05_line.csv', delimiter=',', skip_header=1, names=True)
z1 = M['Height']
hrrpul1 = M['HRRPUL']

M = np.genfromtxt('zeta_0_line.csv', delimiter=',', skip_header=1, names=True)
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

