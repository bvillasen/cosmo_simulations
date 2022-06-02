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

use_mpi = False
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
file_name = input_dir + f'fft_density_{data_type}_{snap_id}.pkl'
print( f'Loading File: {file_name}' )
file = h5.File( file_name, 'r')
z = file.attrs['z']
FT_density = file['FT'][...]


k_cut = 300
print( f'k_cut: {k_cut}' )
FT = FT_density.copy()
k_indices =  K_mag >= k_cut
print(' Filtering')
FT[k_indices] = 0
print( ' Computing inverse fft')
filtered_density = np.fft.ifftn(FT).real   


