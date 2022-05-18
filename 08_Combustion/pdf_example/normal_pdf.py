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


V = np.linspace(-1,1,1000)

def normal(V,mu,sigma):
    f = np.zeros((len(V)))
    C = 1./(sigma*np.sqrt(2.*math.pi))
    for i in range(len(V)):
        f[i] = C * np.exp(-0.5*(V[i]-mu)**2 / sigma**2)
    return f

f1 = normal(V,0,.1)
f2 = normal(V,0,.2)
f3 = normal(V,0,.5)

# plot fds results
plt.figure

marker_style_1 = dict(color='blue',  linestyle='-', linewidth=3, marker='', fillstyle='none', markersize=5)
marker_style_2 = dict(color='red',   linestyle='-', linewidth=3, marker='', fillstyle='none', markersize=5)
marker_style_3 = dict(color='green', linestyle='-', linewidth=3, marker='', fillstyle='none', markersize=5)

plt.plot(V,f1, label='$\mu=0, \sigma=0.1$', **marker_style_1)
plt.plot(V,f2, label='$\mu=0, \sigma=0.2$', **marker_style_2)
plt.plot(V,f3, label='$\mu=0, \sigma=0.5$', **marker_style_3)

#plt.axis([-2, 2, -.1, 1.5])
plt.xlabel('$V$',size=30)
plt.ylabel('$f(V)$',size=30)
plt.legend(loc='upper right', numpoints=1, frameon=False)

plt.gcf().subplots_adjust(bottom=0.15, top=0.95, left=0.15, right=0.95)
#plt.tight_layout() # another possible solution

#plt.show()
plt.savefig('normal_distribution.pdf', format='pdf')
plt.close()


