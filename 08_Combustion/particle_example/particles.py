#!/usr/bin/python
#McDermott
#2016-02-01 20:52:39

from __future__ import division # make floating point division default as in Matlab, e.g., 1/2=0.5
import math
import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],'size':16})

# draw a box

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
ax.add_patch(
    patches.Rectangle(
        (0., 0.),
        1.,
        1.,
        fill=False,      # remove background
        linewidth=7
    )
)

# draw blue particles
lx, ly = (1, .5)
nx, ny = (10, 5)
dx, dy = (lx/nx, ly/ny)
x = np.linspace(.5*dx, lx-.5*dx, nx)
y = np.linspace(.5*dy, ly-.5*dy, ny)

xv, yv = np.meshgrid(y, x)

marker_style_1 = dict(color='blue',  linestyle='', linewidth=1, marker='.', fillstyle='full', markersize=20)
plt.plot(xv,yv, **marker_style_1)

# draw red particles
lx, ly = (1, .5)
nx, ny = (10, 5)
dx, dy = (lx/nx, ly/ny)
x = np.linspace(.5*dx, lx-.5*dx, nx)
y = np.linspace(ly+.5*dy, lx-.5*dy, ny)
xv, yv = np.meshgrid(y, x)

marker_style_1 = dict(color='red',  linestyle='', linewidth=1, marker='.', fillstyle='full', markersize=20)
plt.plot(xv,yv, **marker_style_1)

plt.axis('off')
fig.savefig('uniform_particles.pdf', format='pdf', bbox_inches='tight')
fig.clf()

# draw a box

fig = plt.figure()
ax = fig.add_subplot(111, aspect='equal')
ax.autoscale(enable=False)
ax.add_patch(
    patches.Rectangle(
        (0., 0.),
        1.,
        1.,
        fill=False,      # remove background
        linewidth=7
    )
)

# draw blue particles
lx, ly = (1, 1)
nx, ny = (50, 50)
x = np.random.uniform(0,lx,nx)
y = np.random.uniform(0,ly,ny)
plt.scatter(x,y, color='blue', s=100)

# draw red particles
lx, ly = (1, 1)
nx, ny = (50, 50)
x = np.random.uniform(0,lx,nx)
y = np.random.uniform(0,ly,ny)
plt.scatter(x,y, color='red', s=100)

plt.axis('off')
fig.savefig('random_particles.pdf', format='pdf', bbox_inches='tight')
fig.clf()
