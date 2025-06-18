import matplotlib.pyplot as plt
import numpy as np
import glob
import re
import os

import fdsreader

outdir = 'plots'
if not os.path.exists(outdir):
    os.mkdir(outdir)

ts = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]

rdirs = sorted(glob.glob('rundir/mesh_*'), reverse=True)
dx = []

pattern = re.compile(r"mesh_(\d+)-(\d+)mm")
for d in rdirs:
    match = pattern.match(os.path.split(d)[-1])
    if match:
        major, minor = match.groups()
        # Convert to float in mm
        length_mm = float(f"{int(major)}.{int(minor)}")
        dx.append(length_mm)
    else:
        print(f"Warning: '{d}' does not match the expected pattern.")

vbounds = {}
sims = []

for d in rdirs:
    print(d)
    sim = fdsreader.Simulation(d)

    sims.append(sim)

# print(vbounds)

ob = sims[0].obstructions.get_by_id("OBST-2")
qs = ob.quantities
extent = [ob.bounding_box.x_start, ob.bounding_box.x_end, 
            ob.bounding_box.y_start, ob.bounding_box.y_end]

for q in qs:

    fig = plt.figure(figsize=(7,4))
    for isim, sim in enumerate(sims):
        ob = sim.obstructions.get_by_id("OBST-2")
        mesh = ob.meshes[0].id
        data = ob.get_boundary_data(q)[mesh].data[-3].data

        mins = np.min(data, axis=(1,2))
        maxs = np.max(data, axis=(1,2))
        mean = np.mean(data, axis=(1,2))

        plt.plot(ob.times, mins, lw=0.5, alpha=0.3, color=f"C{isim}")
        plt.plot(ob.times, maxs, lw=0.5, alpha=0.3, color=f"C{isim}")
        plt.plot(ob.times, mean, lw=2, color=f"C{isim}", 
                 label=f"$\\Delta$x = {dx[isim]} mm")
        plt.fill_between(ob.times, mins, maxs, alpha=0.1, color=f"C{isim}")

    plt.xlabel("Time / s")
    plt.ylabel(f"{q.quantity} / {q.unit}")
    plt.legend()
    plt.savefig(os.path.join(outdir, f"bnd_stat_{q.short_name}.png"), 
                dpi=300, bbox_inches='tight')
    plt.close()


    for ct in ts:
        bdata = []
        ldata = []
        for sim in sims:
            ob = sim.obstructions.get_by_id("OBST-2")
            mesh = ob.meshes[0].id
            data = ob.get_boundary_data(q)[mesh].data[-3].data
            it = ob.get_nearest_timestep(ct)
            bdata.append(data[it])

            nx = data[it].shape[0]
            it_min = ob.get_nearest_timestep(ct-50)
            ldata.append(data[it_min:it+1, nx // 2, :])

        vmin = min([np.min(d) for d in bdata])
        vmax = max([np.max(d) for d in bdata])

        n = len(sims)

        fig, axs = plt.subplots(1,n, sharex=True, sharey=True, figsize=(17,5))

        for i in range(len(sims)):
            im = axs[i].imshow(bdata[i].T, extent=extent, 
                       origin='lower',
                       vmin=vmin, vmax=vmax)
            axs[i].set_title(f"$\\Delta$x = {dx[i]} mm")

        fig.colorbar(im, ax=axs.ravel().tolist(), label=f"{q.quantity} / {q.unit}")
        
        plt.savefig(os.path.join(outdir, f"bnd_{q.short_name}_t{ct}.png"), 
                    dpi=300, bbox_inches='tight')
        plt.close()

        fig = plt.figure(figsize=(7,4))
        for isim in range(len(sims)):
            nx = bdata[isim].shape[0]
            x = np.linspace(extent[0], extent[1], nx)
            for i in range(len(ldata[isim])):
                plt.plot(x, ldata[isim][i], color=f"C{isim}", alpha=0.02)
            plt.plot(x, np.mean(ldata[isim], axis=0), label=f"$\\Delta$x = {dx[isim]}")
        plt.xlabel("x / m")
        plt.ylabel(f"{q.quantity} / {q.unit}")
        plt.legend()
        plt.savefig(os.path.join(outdir, f"bnd_line_{q.short_name}_t{ct}.png"), 
                    dpi=300, bbox_inches='tight')
        plt.close()
