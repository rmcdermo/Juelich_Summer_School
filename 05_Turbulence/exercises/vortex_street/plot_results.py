import numpy as np
import matplotlib.pyplot as plt
import glob
import os

import fdsreader

rdirs = sorted(glob.glob("rundir/nu*"))

for d in rdirs:
    nu = os.path.split(d)[-1]

    sim = fdsreader.Simulation(d)

    ### VORTICITY Y
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
    plt.savefig(f'result_vorticity_{nu}.png', bbox_inches='tight', dpi=200)
    plt.clf()

    ### VELOCITY
    slc = sim.slices.filter_by_quantity("VELOCITY")[0]
    slc_data = slc.to_global(masked=True, fill=np.nan)

    it = slc.get_nearest_timestep(2)
    # visualise the data
    plt.imshow(slc_data[it,:,:].T, 
               vmax=1,
               vmin=0,
               cmap='seismic',
               origin='lower', 
               extent=slc.extent.as_list())

    # add labels
    plt.title(f'nu = {nu}; velocity magnitude at t={slc.times[it]:.2f}s')
    plt.xlabel('x / m')
    plt.ylabel('z / m')
    plt.colorbar(orientation='horizontal', label=f'{slc.quantity.name} / {slc.quantity.unit}' )

    # save output to file
    plt.savefig(f'result_vel_{nu}.png', bbox_inches='tight', dpi=200)
    plt.clf()

    ### Z-VELOCITY
    slc = sim.slices.filter_by_quantity("W-VELOCITY")[0]
    slc_data = slc.to_global(masked=True, fill=np.nan)

    it = slc.get_nearest_timestep(2)
    # visualise the data
    plt.imshow(slc_data[it,:,:].T, 
            #    vmax=1,
            #    vmin=0,
               cmap='seismic',
               origin='lower', 
               extent=slc.extent.as_list())

    # add labels
    plt.title(f'nu = {nu}; z-velocity at t={slc.times[it]:.2f}s')
    plt.xlabel('x / m')
    plt.ylabel('z / m')
    plt.colorbar(orientation='horizontal', label=f'{slc.quantity.name} / {slc.quantity.unit}' )

    # save output to file
    plt.savefig(f'result_z-vel_{nu}.png', bbox_inches='tight', dpi=200)
    plt.clf()

    ### AIR1 MASS FRACTION
    slc = sim.slices.filter_by_quantity("AIR1 MASS FRACTION")[0]
    slc_data = slc.to_global(masked=True, fill=np.nan)

    it = slc.get_nearest_timestep(2)
    # visualise the data
    plt.imshow(slc_data[it,:,:].T, 
            #    vmax=500,
            #    vmin=-500,
               cmap='gray_r',
               origin='lower', 
               extent=slc.extent.as_list())

    # add labels
    plt.title(f'nu = {nu}; AIR1 mass fraction at t={slc.times[it]:.2f}s')
    plt.xlabel('x / m')
    plt.ylabel('z / m')
    plt.colorbar(orientation='horizontal', label=f'{slc.quantity.name} / {slc.quantity.unit}' )

    # save output to file
    plt.savefig(f'result_mf1_{nu}.png', bbox_inches='tight', dpi=200)
    plt.clf()

