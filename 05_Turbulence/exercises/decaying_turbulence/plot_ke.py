import matplotlib.pyplot as plt
import glob
import os

import fdsreader

rdirs = sorted(glob.glob('rundir/*'))

plt.figure(figsize=(7,4))

for d in rdirs:
    sim = fdsreader.Simulation(d)

    t = sim.devices["Time"]
    ke = sim.devices["KE"]

    plt.plot(t.data, ke.data, label=os.path.split(d)[-1])

plt.ylim(bottom=0)
plt.xlabel("Time / $s$")
plt.ylabel("Mean Kinetic Energy / $m^2/s^2$")

ref_x = [0.00, 0.28, 0.67]
ref_y = [0.048, 0.0175, 0.0093]

plt.scatter(ref_x, ref_y, color='black', s=25, label="reference data")

plt.grid()
plt.legend()
plt.savefig("KE.png", dpi=300, bbox_inches='tight')