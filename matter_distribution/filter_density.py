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
input_dir = sim_dir + 'fft_files/'
output_dir = sim_dir + 'density_files/'
if rank == 0: create_directory( output_dir )


k_file_name = input_dir + 'k_grid.h5'
print( f'Loading File: {k_file_name}' )
file = h5.File( k_file_name, 'r' )
Kx = file['Kx'][...]
Ky = file['Ky'][...]
Kz = file['Kz'][...]
file.close()
K_mag = np.sqrt( Kz*Kz + Ky*Ky + Kx*Kx )
  
  
snap_id = 5  

file_name = input_dir + f'fft_density_particles_{snap_id}.pkl'
print( f'Loading File: {file_name}' )
file = h5.File( file_name, 'r')
z = file.attrs['z']
FT_dm_density = file['FT'][...]
file.close()

file_name = input_dir + f'fft_density_hydro_{snap_id}.pkl'
print( f'Loading File: {file_name}' )
file = h5.File( file_name, 'r')
z = file.attrs['z']
FT_gas_density = file['FT'][...]
file.close()

n_vals = 50
k_cut_vals = np.logspace( -0.5, 2.36, n_vals ) 
cut_ids = np.arange( n_vals )
ids_local = split_array_mpi( cut_ids, rank, n_procs, adjacent=False )
print( f'rank: {rank}   ids_local: {ids_local}' ) 

for cut_id in ids_local:
  k_cut = k_cut_vals[cut_id]
  print( f'k_cut: {k_cut}' )
  FT_dm  = FT_dm_density.copy()
  FT_gas = FT_gas_density.copy()
  k_indices =  K_mag >= k_cut
  print(' Filtering')
  FT_dm[k_indices]  = 0
  FT_gas[k_indices] = 0
  print( ' Computing inverse fft')
  filtered_dm_density  = np.fft.ifftn(FT_dm).real
  filtered_gas_density = np.fft.ifftn(FT_gas).real   
  file_name = output_dir + f'filtered_density_{snap_id}_{cut_id}.h5'
  file = h5.File( file_name, 'w' )
  file.attrs['z'] = z
  file.attrs['k_cut'] = k_cut
  file.create_dataset( 'dm',  data=filtered_dm_density )
  file.create_dataset( 'gas', data=filtered_gas_density )
  file.close()
  print( f'Saved File: {file_name}' )
  
  
