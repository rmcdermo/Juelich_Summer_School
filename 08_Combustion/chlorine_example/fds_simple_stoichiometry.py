#!/usr/bin/python
# McDermott
# 08-02-2017
# fds_complex_stoichiometry.py

from __future__ import division # make floating point division default as in Matlab, e.g., 1/2=0.5
import math
import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica'],'size':16})

# define atomic weights

W_C = 12.0107
W_H = 1.0794
W_O = 15.9994
W_N = 14.0067

# define hydrogen atomic fraction in soot

X_H = 0.1

# define CO and soot yields

y_CO = 0
y_Soot = 0.01

# define primitive species

# 'methane','oxygen','nitrogen','water vapor','carbon dioxide','carbon monoxide','soot'

i_methane         = 0
i_oxygen          = 1
i_nitrogen        = 2
i_water_vapor     = 3
i_carbon_dioxide  = 4
i_carbon_monoxide = 5
i_soot            = 6

n_species = 7

# define the element matrix (number of atoms [rows] for each primitive species [columns])

#              0  1  2  3  4  5  6
E = np.array([[1, 0, 0, 0, 1, 1, (1-X_H)], \
              [4, 0, 0, 2, 0, 0, X_H    ], \
              [0, 2, 0, 1, 2, 1, 0      ], \
              [0, 0, 2, 0, 0, 0, 0      ]])

print('Element matrix')
print(E)

# primitive species molecular weights

A = np.array([W_C, W_H, W_O, W_N])
W = np.dot(E.T,A)

print('Primitive species molecular weights')
print(W)

# define the mass fractions of the background air (grab from FDS .out file)

v_1 = np.zeros((n_species))
v_1[i_oxygen]         = 0.231181
v_1[i_nitrogen]       = 0.763077
v_1[i_water_vapor]    = 0.005149
v_1[i_carbon_dioxide] = 0.000592
print('Mass fractions of AIR')
print(v_1)

# convert to volume fractions

W_1 = 1./np.sum(v_1/W)
print('Molecular weight of AIR')
print(W_1)

v_1 = v_1*W_1/W
v_1 = v_1/np.sum(v_1)
print('Volume fractions of AIR')
print(v_1)

# define volume fractions of fuel mixture (assumed known)

v_2 = np.zeros((n_species))
v_2[i_methane] = 1.
v_2 = v_2/np.sum(v_2)
print('Volume fractions of FUEL')
print(v_2)

W_2 = np.sum(v_2*W)
print('Molecular weight of FUEL')
print(W_2)

# the reaction coefficients for the product primitive species temporarily stored in v_3

v_3 = np.zeros((n_species))

# compute what we know so far

v_3[i_carbon_monoxide] = W_2/W[i_carbon_monoxide]*y_CO
v_3[i_soot]            = W_2/W[i_soot]*y_Soot

# linear system right hand side

b = np.dot(E,v_2-v_3)
print('b')
print(b)

# matrix

L = np.array([np.dot(E,v_1),E[:,i_carbon_dioxide],E[:,i_water_vapor],E[:,i_nitrogen]]).T
print('L')
print(L)

# % solve the system

x = np.linalg.solve(L,b)
print('x')
print(x)

nu_1                  = x[0] # background stoichiometric coefficient
v_3[i_carbon_dioxide] = x[1]
v_3[i_water_vapor]    = x[2]
v_3[i_nitrogen]       = x[3]

nu_2 = -1       # fuel stoich coeff
nu_3 = sum(v_3) # prod stoich coeff

v_3 = v_3/nu_3  # normalized product volume fractions

# check mass balance (should be 0)

print('Mass balance')
print( nu_1*np.sum(v_1*W) + nu_2*np.sum(v_2*W) + nu_3*np.sum(v_3*W) )

# check primitive reaction coefficients

print('Primitive species stoichiometry')
print( nu_1*v_1 + nu_2*v_2 + nu_3*v_3 )

# display fuel properties

Z2Y = np.array([v_1,v_2,v_3]).T
print('Z2Y (volume fractions)')
print(Z2Y)

# check atom balance

C_1 = np.dot(nu_1*v_1,E[0,:])
H_1 = np.dot(nu_1*v_1,E[1,:])
O_1 = np.dot(nu_1*v_1,E[2,:])
N_1 = np.dot(nu_1*v_1,E[3,:])

C_2 = np.dot(nu_2*v_2,E[0,:])
H_2 = np.dot(nu_2*v_2,E[1,:])
O_2 = np.dot(nu_2*v_2,E[2,:])
N_2 = np.dot(nu_2*v_2,E[3,:])

C_3 = np.dot(nu_3*v_3,E[0,:])
H_3 = np.dot(nu_3*v_3,E[1,:])
O_3 = np.dot(nu_3*v_3,E[2,:])
N_3 = np.dot(nu_3*v_3,E[3,:])

print('')
print('check atom balance')
print('AIR')
print('Element   nu*Atom Count')
print('C         '+str(C_1))
print('H         '+str(H_1))
print('O         '+str(O_1))
print('N         '+str(N_1))

print('')
print('check atom balance')
print('FUEL')
print('Element   nu*Atom Count')
print('C         '+str(C_2))
print('H         '+str(H_2))
print('O         '+str(O_2))
print('N         '+str(N_2))

print('')
print('check atom balance')
print('PRODUCTS')
print('Element   nu*Atom Count')
print('C         '+str(C_3))
print('H         '+str(H_3))
print('O         '+str(O_3))
print('N         '+str(N_3))

print('')
print('Element   Atom Error')
print('C         '+str(C_1+C_2+C_3))
print('H         '+str(H_1+H_2+H_3))
print('O         '+str(O_1+O_2+O_3))
print('N         '+str(N_1+N_2+N_3))



