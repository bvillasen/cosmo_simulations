import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import load_snapshot_data_distributed
from power_spectrum_functions import get_power_spectrum

use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

n_cells = 1024
L_Mpc = 25

sim_name = f'{n_cells}_{L_Mpc}Mpc_cdm'
density_type = 'cic'

base_dir = data_dir + f'cosmo_sims/wdm_sims/tsc/'
sim_dir  = base_dir + f'{sim_name}/{density_type}/'
input_dir = sim_dir + 'density_files/'
output_dir = sim_dir + 'density_slices/'
if rank == 0: create_directory( output_dir )

n_vals = 50
cut_ids = np.arange( n_vals )
ids_local = split_array_mpi( cut_ids, rank, n_procs, adjacent=False )
print( f'rank: {rank}   ids_local: {ids_local}' ) 

snap_id = 5  
slice_depth = 256

for cut_id in ids_local:
  file_name = input_dir + f'filtered_density_{snap_id}_{cut_id}.h5'
  print( f'Loading File: {file_name}' )
  file = h5.File( file_name, 'r' )
  z = file.attrs['z']
  k_cut = file.attrs['k_cut']
  dm_density  = file['dm'][...]
  gas_density = file['gas'][...]
  file.close()
  
  dm_slice  = dm_density[:slice_depth,:,:]
  gas_slice = gas_density[:slice_depth,:,:]
  
  file_name = output_dir + f'filtered_density_{snap_id}_{cut_id}_{slice_depth}.h5'
  file = h5.File( file_name, 'w' )
  file.attrs['z'] = z
  file.attrs['k_cut'] = k_cut
  file.create_dataset( 'dm',  data=dm_slice )
  file.create_dataset( 'gas', data=gas_slice )
  file.close()

  print( f'Saved File: {file_name}' )

