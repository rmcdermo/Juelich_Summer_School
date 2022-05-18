#!/usr/bin/python
#McDermott
#2017-07-31 20:52:39

from __future__ import division # for Python 2.7 make floating point division default as in Matlab, e.g., 1/2=0.5
import math
import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],'size':16})

W_C3H8 = 44.
W_O2   = 32.
W_N2   = 28.
W_CO2  = 44.
W_H2O  = 18.

# consider the reaction
# C3H8 + 5 [ O2 + (0.79/0.21) N2 ] => 3 CO2 + 4 H2O + 5 (0.79/0.21) N2
N_A = 5. + 5.*0.79/0.21
N_P = 3. + 4. + 5.*0.79/0.21

X_O2_A = 5./N_A
X_N2_A = 5.*0.79/0.21/N_A

X_CO2_P = 3./N_P
X_H2O_P = 4./N_P
X_N2_P = 5.*0.79/0.21/N_P

W_F = W_C3H8
W_A = X_O2_A*W_O2 + X_N2_A*W_N2
W_P = X_CO2_P*W_CO2 + X_H2O_P*W_H2O + X_N2_P*W_N2

# vector of lumped species mass fractions
Z = np.array([0.3, 0.2, 0.5])
print(Z)
print(np.sum(Z))

A = np.array([[W_C3H8/W_F,                0,                 0], \
              [0,           X_O2_A*W_O2/W_A,                 0], \
              [0,           X_N2_A*W_N2/W_A,   X_N2_P*W_N2/W_P], \
              [0,                         0, X_CO2_P*W_CO2/W_P], \
              [0,                         0, X_H2O_P*W_H2O/W_P]])
print(A)
print(np.sum(A,axis=0))

# convert lumped vector Z to primitive vector Y
Y = np.dot(A,Z)
print(Y)
print(np.sum(Y))













