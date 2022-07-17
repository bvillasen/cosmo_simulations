import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
from scipy import interpolate
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from get_RT_correction import get_RT_1Dpk_correction

use_mpi = False
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1


# grid_name = '1024_wdmgrid_extended_beta'
grid_name = '1024_wdmgrid_cdm_extended_beta'
grid_dir = data_dir + f'cosmo_sims/sim_grid/{grid_name}/' 
root_dir = grid_dir + f'simulation_files/'
ps_dir = grid_dir + 'flux_power_spectrum/'
thermal_dir = grid_dir + 'thermal/'
output_dir = grid_dir + 'flux_power_spectrum_RT_corrected/'
if rank == 0: create_directory( output_dir )

sim_dirs = [ dir for dir in os.listdir(root_dir) if dir[0]=='S' ]
sim_dirs.sort()

# 
# n_simulations = len( sim_dirs )
# sim_ids = range(n_simulations)
# sim_ids_local = split_indices( sim_ids, rank, n_procs )
# print( f'proc_id: {rank}  sim_ids_local:{sim_ids_local}')



for sim_dir in sim_dirs:
  
  create_directory( output_dir + f'{sim_dir}' )

  file_name = thermal_dir + f'{sim_dir}/global_properties.pkl'
  data_global = Load_Pickle_Directory( file_name )
  z_ion_H = data_global['z_ion_H']

  snap_ids = [ 25, 29, 33 ]

  for snap_id in snap_ids:
    file_name = ps_dir + f'{sim_dir}/flux_ps_sampled_boera_extended_{snap_id:03}.h5'
    print( f'Loading File: {file_name}' )
    file = h5.File( file_name, 'r' )
    current_z = file.attrs['current_z']
    print( f'current_z: {current_z}' )
    k_vals  = file['k_vals'][...]
    ps_mean = file['ps_mean'][...]
    file.close()

    log_k = np.log10( k_vals )
    correction_log_k, correction = get_RT_1Dpk_correction( current_z, z_ion_H ) 
    f = interpolate.interp1d( correction_log_k, correction, fill_value='extrapolate')

    ps_correction = f( log_k )
    ps_corrected = ps_mean * ps_correction


    file_name = output_dir + f'{sim_dir}/flux_ps_sampled_boera_extended_{snap_id:03}.h5'
    file = h5.File( file_name, 'w' )
    file.attrs['current_z'] = current_z 
    file.create_dataset( 'k_vals', data = k_vals )
    file.create_dataset( 'ps_mean', data= ps_corrected )
    file.close()
    print( f'Saved File: {file_name}' )





