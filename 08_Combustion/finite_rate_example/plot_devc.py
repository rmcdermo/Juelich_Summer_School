#!/usr/bin/python
#McDermott
#2016-02-01 20:52:39

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read data from _devc file
M = pd.read_csv('reactionrate_arrhenius_2order_1step_devc.csv', header=1)
t = M['Time']
Y_O2   = M['O2']
Y_C3H8 = M['C3H8']
Y_CO2  = M['CO2']
Y_H2O  = M['H2O']

# plot upper and lower layer temperature
plt.figure
marker_style_1 = dict(color='blue', linestyle='-', marker='', fillstyle='none', markersize=5)
marker_style_2 = dict(color='black',linestyle='-', marker='', fillstyle='none', markersize=5)
marker_style_3 = dict(color='red',  linestyle='-', marker='', fillstyle='none', markersize=5)
marker_style_4 = dict(color='green',linestyle='-', marker='', fillstyle='none', markersize=5)

plt.plot(t,Y_O2,  label='O2',  **marker_style_1)
plt.plot(t,Y_C3H8,label='C3H8',**marker_style_2)
plt.plot(t,Y_CO2, label='CO2', **marker_style_3)
plt.plot(t,Y_H2O, label='H2O', **marker_style_4)

plt.axis([min(t), max(t), 0, 0.3])
plt.xlabel('Time (s)')
plt.ylabel('Mass Fraction')
plt.legend(loc='upper right', numpoints=1)
#plt.show()
plt.savefig('reaction_species.pdf', format='pdf')
plt.close()

