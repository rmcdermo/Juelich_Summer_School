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


r = np.linspace(-2,2,1000)
def tophat_kernel(r,D):
    K = np.zeros((len(r)))
    for i in range(len(r)):
        if np.abs(r[i])<D/2.:
            K[i]=1.
    return K

G = tophat_kernel(r,1)

# plot fds results
plt.figure

marker_style_1 = dict(color='blue', linestyle='-', linewidth=3, marker='', fillstyle='none', markersize=5)
plt.plot(r,G, label='tophat kernel', **marker_style_1)

plt.axis([-2, 2, -.1, 1.5])
plt.xlabel('$r/\Delta$',size=30)
plt.ylabel('$G(r)$',size=30)
plt.legend(loc='upper right', numpoints=1, frameon=False)

plt.gcf().subplots_adjust(bottom=0.15, top=0.95, left=0.15, right=0.95)
#plt.tight_layout() # another possible solution

#plt.show()
plt.savefig('tophat_kernel.pdf', format='pdf')
plt.close()

