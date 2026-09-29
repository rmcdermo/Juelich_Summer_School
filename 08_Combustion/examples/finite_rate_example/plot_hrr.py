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
plt.figure(figsize=(5, 3.8))
plt.rcParams.update({'font.size': 13, 'svg.fonttype': 'none'})

marker_style_1 = dict(color='black', linestyle=':', linewidth=0.6, marker='o',
                      fillstyle='none', markersize=2.5, markeredgewidth=0.5)
plt.plot(t,ETA, label='', **marker_style_1)

plt.axis([min(t), max(t), 0, 2])
plt.xlabel('time (s)')
plt.ylabel(r'$\eta = \dot{Q}/(\dot{m}_f\,\Delta H_c)$')
#plt.show()
plt.tight_layout()
plt.savefig(base / 'comb_efficiency.pdf')
plt.savefig(base / 'comb_efficiency.png', dpi=300)
plt.close()

