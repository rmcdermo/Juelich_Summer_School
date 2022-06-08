#!/usr/bin/python
#McDermott
#2016-02-01 20:52:39

import numpy as np
import matplotlib.pyplot as plt

# see S.B. Pope (2000) p. 232

C_K=1.5
L=10
eta=0.001
eps=100
TWTH=2./3.
MFTH=-5./3.

keta = np.logspace(-5,0,num=100)
k = keta/eta

def f_L(x):
    c_L=6.78
    p0=2.
    f = (x/np.sqrt(x**2+c_L))**(5./3.+p0)
    return f

def f_eta(x):
    c_eta=0.40
    beta=5.2
    f = np.exp(-beta*((x**4+c_eta**4)**0.25)-c_eta)
    return f

def model_spectrum(x):
    f = np.zeros((len(x)))
    for i in range(len(x)):
        f[i] = C_K * eps**TWTH * x[i]**MFTH * f_L(x[i]*L) * f_eta(x[i]*eta)
    return f

E = model_spectrum(k)

# plot fds results
plt.figure

marker_style_1 = dict(color='blue', linestyle='-', linewidth=3, marker='', fillstyle='none', markersize=5)
plt.loglog(k,E, label='', **marker_style_1)

marker_style_2 = dict(color='black', linestyle='--', linewidth=3, marker='', fillstyle='none', markersize=5)
plt.loglog(np.array([k[60], k[60]]),np.array([np.min(E), np.max(E)]), label='', **marker_style_2)

#plt.axis([-.1, 1.1, -.1, 1.5])
plt.xlabel('$k$',size=16)
plt.ylabel('$E(k)$',size=16)
#plt.legend(loc='upper center', numpoints=1, frameon=False)

plt.gcf().subplots_adjust(bottom=0.15, top=0.95, left=0.15, right=0.95)
#plt.tight_layout() # another possible solution

#plt.show()
plt.savefig('model_spectrum.pdf', format='pdf')
plt.close()


