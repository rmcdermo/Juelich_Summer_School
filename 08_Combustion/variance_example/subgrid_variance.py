#!/usr/bin/python
# McDermott
# 8-4-2017

import math
import numpy as np
import matplotlib.pyplot as plt

#data = np.random.randint(2,size=(10,10))

data = np.ones([10,10]) * 0.5
data[:,5:10] = np.ones([10,5]) * 0.5

print(np.var(data))

fig=plt.figure(figsize=(12,6))

#https://matplotlib.org/users/colormaps.html
ax1 = plt.subplot(1, 2, 1)
cax = ax1.imshow(data, interpolation='nearest', \
    cmap=plt.cm.get_cmap('inferno'), vmin=0, vmax=1)
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

fig.savefig('histogram.pdf', format='pdf', bbox_inches='tight')
fig.clf()
