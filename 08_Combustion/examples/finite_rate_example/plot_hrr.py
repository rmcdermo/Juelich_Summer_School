#!/usr/bin/python
#McDermott
#2016-02-01 20:52:39

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.seterr(divide='ignore', invalid='ignore')

# Read global heat release and fuel mass flow (kg/s).
base = Path(__file__).resolve().parent
M = pd.read_csv(base / 'westbrook_dryer_hrr.csv', header=1)
t = M['Time']
HRR      = M['HRR']
MLR_FUEL = M['MLR_PROPANE']
HOC  = 46334 # kJ/kg

# combustion efficiency
ETA = np.divide(HRR,(MLR_FUEL*HOC))

# plot fds results
plt.figure()

marker_style_1 = dict(color='black', linestyle=':', marker='o', fillstyle='none', markersize=5)
plt.plot(t,ETA, label='', **marker_style_1)

plt.axis([min(t), max(t), 0, 2])
plt.xlabel('time (s)')
plt.ylabel('$\\eta$ = Q / (MLR $\\times$ HOC)')
#plt.show()
plt.savefig(base / 'comb_efficiency.pdf', format='pdf')
plt.close()

