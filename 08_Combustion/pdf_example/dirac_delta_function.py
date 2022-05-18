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


V1 = np.linspace(-1,.5,1000)
V2 = np.linspace(.5, 2,1000)

def normal(V,mu,sigma):
    f = np.zeros((len(V)))
    C = 1./(sigma*np.sqrt(2.*math.pi))
    for i in range(len(V)):
        f[i] = C * np.exp(-0.5*(V[i]-mu)**2 / sigma**2)
    return f

std_dev = 0.0001
f1 = normal(V1,0,std_dev)
f2 = normal(V2,1,std_dev)

# plot fds results
plt.figure

marker_style_1 = dict(color='blue', linestyle='-', linewidth=3, marker='', fillstyle='none', markersize=5)
marker_style_2 = dict(color='red',  linestyle='-', linewidth=3, marker='', fillstyle='none', markersize=5)

plt.plot(V1,f1, label='$V=0$', **marker_style_1)
plt.plot(V2,f2, label='$V=1$', **marker_style_2)

plt.axis([-.1, 1.1, -.1, 1.5])
plt.xlabel('$V$',size=30)
plt.ylabel('$f(V)$',size=30)
plt.legend(loc='upper center', numpoints=1, frameon=False)

plt.gcf().subplots_adjust(bottom=0.15, top=0.95, left=0.15, right=0.95)
#plt.tight_layout() # another possible solution

#plt.show()
plt.savefig('two_deltas.pdf', format='pdf')
plt.close()


