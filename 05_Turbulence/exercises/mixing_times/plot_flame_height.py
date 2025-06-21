import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

rdirs = sorted(glob.glob('rundir/tau*'))

plt.figure(figsize=(7,4))

for rd in rdirs:
    data = pd.read_csv(os.path.join(rd, 'out_mixing_line.csv'), header=1)
    plt.plot(data['HRRPUL'], data['Height'], "o-", label=os.path.split(rd)[-1])
    # plt.semilogx(data['HRRPUL'], data['Height'], "o-", label=os.path.split(rd)[-1])

plt.xlabel("HRRPUL / kW/m")
plt.ylabel("Height / m")

# plt.xlim(left=1)
plt.xlim([0,1000])
plt.legend()
plt.grid()

plt.axhline(3.04,color='black',linestyle='-.')
plt.text(800,3.25,'Flame Height')

plt.savefig("flame_height.png", dpi=300, bbox_inches='tight')

