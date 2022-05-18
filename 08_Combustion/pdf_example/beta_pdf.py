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

Z = np.linspace(0,1,100)

def beta(Z,Z_MEAN,Z_VAR):
    f = np.zeros((len(Z)))
    gamma = Z_MEAN*(1.-Z_MEAN)/Z_VAR - 1.
    print(gamma)
    alpha = Z_MEAN*gamma
    beta  = (1.-Z_MEAN)*gamma
    for i in range(len(Z)):
        f[i] = Z[i]**(alpha-1.) * (1.-Z[i])**(beta-1.) / (sp.gamma(alpha)*sp.gamma(beta)) * sp.gamma(alpha+beta)
    return f

f1 = beta(Z,0.6,0.048)
f2 = beta(Z,0.6,0.022)
f3 = beta(Z,0.6,0.160)
f4 = beta(Z,0.8,0.053)

# plot fds results
plt.figure

marker_style_1 = dict(color='blue',  linestyle='-', linewidth=3, marker='', fillstyle='none', markersize=5)
marker_style_2 = dict(color='red',   linestyle='-', linewidth=3, marker='', fillstyle='none', markersize=5)
marker_style_3 = dict(color='green', linestyle='-', linewidth=3, marker='', fillstyle='none', markersize=5)
marker_style_4 = dict(color='black', linestyle='-', linewidth=3, marker='', fillstyle='none', markersize=5)

plt.plot(Z,f1, label='$\\tilde{Z}=0.6, \gamma=4$' ,  **marker_style_1)
plt.plot(Z,f2, label='$\\tilde{Z}=0.6, \gamma=10$',  **marker_style_2)
plt.plot(Z,f3, label='$\\tilde{Z}=0.6, \gamma=0.5$', **marker_style_3)
plt.plot(Z,f4, label='$\\tilde{Z}=0.8, \gamma=2$' ,  **marker_style_4)

#plt.axis([-2, 2, -.1, 1.5])
plt.xlabel('$Z$',size=30)
plt.ylabel('$f(Z)$',size=30)
plt.legend(loc='upper left', numpoints=1, frameon=False)

plt.gcf().subplots_adjust(bottom=0.15, top=0.95, left=0.15, right=0.95)
#plt.tight_layout() # another possible solution

#plt.show()
plt.savefig('beta_distribution.pdf', format='pdf')
plt.close()


