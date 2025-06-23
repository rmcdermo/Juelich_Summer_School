import numpy as np
import matplotlib.pyplot as plt
import glob
import os

import fdsreader

rdirs = sorted(glob.glob("rundir/nu*"))

for d in rdirs:
    nu = os.path.split(d)[-1]

    sim = fdsreader.Simulation(d)
    slc = sim.slices.filter_by_quantity("VORTICITY Y")[0]
    slc_data = slc.to_global(masked=True, fill=np.nan)

    it = slc.get_nearest_timestep(2)
    # visualise the data
    plt.imshow(slc_data[it,:,:].T, 
               vmax=500,
               vmin=-500,
               cmap='seismic',
               origin='lower', 
               extent=slc.extent.as_list())

    # add labels
    plt.title(f'nu = {nu}; y-vorticity at t={slc.times[it]:.2f}s')
    plt.xlabel('x / m')
    plt.ylabel('z / m')
    plt.colorbar(orientation='horizontal', label=f'{slc.quantity.name} / {slc.quantity.unit}' )

    # save output to file
    plt.savefig(f'result_{nu}.png', bbox_inches='tight', dpi=200)
    plt.clf()

