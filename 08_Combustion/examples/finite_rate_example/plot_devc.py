#!/usr/bin/python
#McDermott
#2016-02-01 20:52:39

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# read data from _devc file
base = Path(__file__).resolve().parent
M = pd.read_csv(base / 'westbrook_dryer_devc.csv', header=1)
t = M['Time']
Y_O2   = M['O2']
Y_C3H8 = M['C3H8']
Y_CO2  = M['CO2']
Y_H2O  = M['H2O']

# Plot species mass fractions at (0, 0, 0.2) m.
plt.figure()
marker_style_1 = dict(color='blue', linestyle='-', marker='', fillstyle='none', markersize=5)
marker_style_2 = dict(color='black',linestyle='-', marker='', fillstyle='none', markersize=5)
marker_style_3 = dict(color='red',  linestyle='-', marker='', fillstyle='none', markersize=5)
marker_style_4 = dict(color='green',linestyle='-', marker='', fillstyle='none', markersize=5)

plt.plot(t,Y_O2,  label='O2',  **marker_style_1)
plt.plot(t,Y_C3H8,label='C3H8',**marker_style_2)
plt.plot(t,Y_CO2, label='CO2', **marker_style_3)
plt.plot(t,Y_H2O, label='H2O', **marker_style_4)

plt.xlim(min(t), max(t))
plt.ylim(bottom=0)
plt.xlabel('Time (s)')
plt.ylabel('Mass Fraction')
plt.legend(loc='upper right', numpoints=1)
#plt.show()
plt.savefig(base / 'reaction_species.pdf', format='pdf')
plt.close()

