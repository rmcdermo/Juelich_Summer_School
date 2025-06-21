import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

rdirs = sorted(glob.glob('rundir/tau*'))

plt.figure(figsize=(7,4))

for rd in rdirs:
    data = pd.read_csv(os.path.join(rd, 'out_mixing_hrr.csv'), header=1)
    plt.plot(data['Time'], data['HRR'], "o-", label=os.path.split(rd)[-1])

plt.xlabel("Time / s")
plt.ylabel("HRR / kW")

plt.legend()
plt.grid()

plt.axhline(y = 1512,color='black',linestyle='-.')
plt.text(0,1420,'Theoretical HRR')

plt.savefig("HRR.png", dpi=300, bbox_inches='tight')

