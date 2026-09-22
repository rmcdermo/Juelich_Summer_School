#!/usr/bin/python
# McDermott
# 8-6-2017
# subgrid_variance_2.py

import sys
import numpy as np
import matplotlib.pyplot as plt

data = plt.imread('transport_vs_mixing_0461_a.png')
# data = plt.imread('transport_vs_mixing_0461_b.png')
# normalize data
data = data/np.max(data)
data = data - np.min(data)
data = data*1./np.max(data)
#sys.exit()

#data = np.random.randint(2,size=(10,10))

# data = np.ones([10,10]) * 0.5
# data[:,5:10] = np.ones([10,5]) * 0.5

print(np.var(data))

fig=plt.figure(figsize=(12,6))

#https://matplotlib.org/users/colormaps.html
ax1 = plt.subplot(1, 2, 1)
cax = ax1.imshow(data, interpolation='nearest', cmap=plt.cm.get_cmap('inferno'), vmin=0, vmax=1)
cbar = fig.colorbar(cax, ticks=[0, 0.5, 1], fraction=0.045, pad=.05)

#plt.axis('off') # remove ticks and labels
ax1.set_xticks([])
ax1.set_yticks([])

ax2=plt.subplot(1, 2, 2)
binBoundaries = np.linspace(0,1,100)
plt.hist(data.reshape(np.size(data)), bins=binBoundaries)
plt.xlim(0,1)
ax2.set_xlabel('Z')

plt.tight_layout()

#plt.show()

fig.savefig('mix_hist.pdf', format='pdf', bbox_inches='tight')
fig.clf()
