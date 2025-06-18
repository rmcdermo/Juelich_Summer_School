import matplotlib.pyplot as plt
import glob
import re

import fdsreader

rdirs = sorted(glob.glob('mesh_*'), reverse=True)
dx = []

pattern = re.compile(r"mesh_(\d+)-(\d+)mm")
for d in rdirs:
    match = pattern.match(d)
    if match:
        major, minor = match.groups()
        # Convert to float in mm
        length_mm = float(f"{int(major)}.{int(minor)}")
        dx.append(length_mm)
    else:
        print(f"Warning: '{d}' does not match the expected pattern.")

plt.figure(figsize=(7,4))

for i,d in enumerate(rdirs):
    sim = fdsreader.Simulation(d)
    t = sim.devices["Time"].data
    chf = sim.devices["CHF"].data
    plt.plot(t, chf, label=f"$\\Delta$x = {dx[i]:.2f} mm")

plt.xlabel("Time / s")
plt.ylabel("Convective Heat Flux / kW")
plt.grid()
plt.legend()
plt.ylim(top=2.5)
plt.savefig('q_conv.png', dpi=300, bbox_inches='tight')

plt.clf()

for i,d in enumerate(rdirs):
    sim = fdsreader.Simulation(d)
    t = sim.devices["Time"].data
    thf = sim.devices["THF"].data
    plt.plot(t, thf, label=f"$\\Delta$x = {dx[i]:.2f} mm")

plt.xlabel("Time / s")
plt.ylabel("Total Heat Flux / kW")
plt.grid()
plt.legend()
plt.ylim(top=2.5)
plt.savefig('q_tot.png', dpi=300, bbox_inches='tight')