import os, sys
import numpy as np
import pickle
import pymc
import matplotlib.pyplot as plt
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *

grid_dir = data_dir + 'cosmo_sims/sim_grid/grid_thermal/1024_P19m_np4_nsim400/'
flux_dir = grid_dir + 'transmitted_flux/'
create_directory( flux_dir )

sim_dirs = [ dir for dir in os.listdir(grid_dir) if os.path.isdir(grid_dir+dir) and dir[0]=='S' ]
sim_dirs.sort()

file_indices = range( 15, 56 )

for sim_dir in sim_dirs:
  
  print(f'\nDir: {sim_dir}')
  output_dir = flux_dir + f'{sim_dir}/'
  create_directory( output_dir )

  for file_indx in file_indices:

    file_name = grid_dir + sim_dir + f'/analysis_files/{file_indx}_analysis.h5'
    file = h5.File( file_name, 'r' )
    current_z = file.attrs['current_z'][0]
    print( f' z: {current_z}')
    F_mean = file['lya_statistics'].attrs['Flux_mean_HI'][0]
    k_vals = file['lya_statistics']['power_spectrum']['k_vals'][...]
    ps_mean = file['lya_statistics']['power_spectrum']['p(k)'][...]
    vel_Hubble = None
    flux_all = []
    for axis in [ 'x', 'y', 'z' ]:
      key = f'skewers_{axis}'
      print ( f' Loading {key}' )
      skewers_data = file['lya_statistics'][key]
      vel_Hubble_axis = skewers_data['vel_Hubble'][...]
      if vel_Hubble is None: vel_Hubble = vel_Hubble_axis
      v_diff = np.abs( vel_Hubble - vel_Hubble_axis).sum()
      if v_diff > 1e-6: 
        print( 'ERROR: Mismatch in vel_Hubble')
        exit(-1)
      los_flux_axis = skewers_data['los_transmitted_flux_HI'][...]
      flux_all.append( los_flux_axis )
    flux_all = np.concatenate( flux_all, axis=0 )
    f_diff = np.abs( F_mean - flux_all.mean()) / F_mean
    if f_diff > 1e-6:
      print( f'ERROR: Mismatch in F_mean ')
      exit(-1)

    file.close()

    out_file_name = output_dir + f'lya_flux_{file_indx:03}.h5'
    out_file = h5.File( out_file_name, 'w' )
    out_file.attrs['current_z'] = current_z
    out_file.attrs['Flux_mean'] = F_mean
    out_file.create_dataset( 'vel_Hubble', data=vel_Hubble )
    out_file.create_dataset( 'skewers_fflux', data=flux_all )
    ps_group = out_file.create_group( 'power_spectrum' )
    ps_group.create_dataset( 'k_vals', data=k_vals )
    ps_group.create_dataset( 'ps_mean', data=ps_mean )
    out_file.close()
    print( f'Saved File: {out_file_name}' )

# file_name = '/data/groups/comp-astro/bruno/cosmo_sims/sim_grid/1024_wdmgrid_nsim600/transmitted_flux/S000_A0_B0_C0_D0/lya_flux_033.h5'
# file_0 = h5.File( file_name, 'r' )