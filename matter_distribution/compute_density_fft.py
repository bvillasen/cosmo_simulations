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

args = sys.argv[1:]
data_type = args[0]
# data_type = 'hydro'
# data_type = 'particles'

n_cells = 1024
L_Mpc = 25

sim_name = f'{n_cells}_{L_Mpc}Mpc_cdm'
density_type = 'cic'

base_dir = data_dir + f'cosmo_sims/wdm_sims/tsc/'
sim_dir  = base_dir + f'{sim_name}/{density_type}/'
input_dir = sim_dir + 'snapshot_files/'
output_dir = sim_dir + 'fft_files/'
if rank == 0: create_directory( output_dir )

snap_ids = np.arange(9)
snaps_local = split_array_mpi( snap_ids, rank, n_procs, adjacent=False )
print(f'rank: {rank}  snaps_local: {snaps_local}' )

Lbox = L_Mpc * 1e3    #kpc/h
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
precision = np.float64
fields = [ 'density' ]

nx, ny, nz = grid_size
dx, dy, dz = L_Mpc/nx, L_Mpc/ny, L_Mpc/nz

k_file_name = output_dir + 'k_grid.h5'
if not os.path.isfile( k_file_name ) and rank==0:
  print( 'Computing K ')
  fft_kx = 2*np.pi*np.fft.fftfreq( nx, d=dx )
  fft_ky = 2*np.pi*np.fft.fftfreq( ny, d=dy )
  fft_kz = 2*np.pi*np.fft.fftfreq( nz, d=dz )
  Kz, Ky, Kx = np.meshgrid( fft_kz, fft_ky, fft_kx )
  k_file = h5.File( k_file_name, 'w' )
  k_file.create_dataset( 'fft_kx', data=fft_kx )
  k_file.create_dataset( 'fft_ky', data=fft_ky )
  k_file.create_dataset( 'fft_kz', data=fft_ky )
  k_file.create_dataset( 'Kx', data=Kx )
  k_file.create_dataset( 'Ky', data=Ky )
  k_file.create_dataset( 'Kz', data=Kz )
  k_file.close()

comm.Barrier()

for snap_id in snaps_local:
  file_name = output_dir + f'fft_density_{data_type}_{snap_id}.pkl'
  if os.path.isfile( file_name ): 
    print( f'Skipping: {file_name}')
    continue

  snap_data = load_snapshot_data_distributed( data_type, fields,  snap_id, input_dir,  box_size, grid_size, precision  )
  z = snap_data['Current_z']
  density = snap_data['density'] 
  density /= density.mean()

  print( 'Computing density FFT')
  FT = np.fft.fftn( density )

  file = h5.File( file_name, 'w' )
  file.attrs['z'] = z
  file.attrs['dens_mean'] = density.mean()
  file.create_dataset( 'FT', data=FT )
  file.close()
  print( f'Saved File: {file_name}' )
   
