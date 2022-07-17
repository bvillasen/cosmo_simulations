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


data_type = 'particles'

n_cells = 1024
L_Mpc = 25

# sim_name = f'{n_cells}_{L_Mpc}Mpc_cdm'
sim_name = f'{n_cells}_{L_Mpc}Mpc_m4.0kev'

base_dir = data_dir + f'cosmo_sims/wdm_sims/new/'
sim_dir  = base_dir + f'{sim_name}/'
input_dir = sim_dir + 'snapshot_files/'
output_dir = sim_dir + 'power_spectrum_files/'
if rank == 0: create_directory( output_dir )


Lbox = L_Mpc * 1e3    #kpc/h
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
precision = np.float64
fields = [ 'density' ]

n_bins = 25
Lbox = Lbox/1000    #Mpc/h
nx, ny, nz = grid_size
dx, dy, dz = Lbox/nx, Lbox/ny, Lbox/nz

snap_id = 6

snap_ids = np.array([ 6, 7, 8])
snap_id = snap_ids[rank]

snap_data = load_snapshot_data_distributed( data_type, fields,  snap_id, input_dir,  box_size, grid_size, precision  )
z = snap_data['Current_z']
density = snap_data['density']
nx, ny, nz = density.shape
n_total = nx * ny * nz

print( f'Computing Power Spectrum  snap_id: {snap_id}  z:{z}' )
power_spectrum, k_vals, n_in_bin = get_power_spectrum( density, Lbox, nx, ny, nz, dx, dy, dz,  n_kSamples=n_bins, fft_shift=False )
sim_data = { 'z':z, 'k_vals':k_vals, 'power_spectrum':power_spectrum, 'n_in_bin':n_in_bin }

file_name = output_dir + f'ps_dm_density_{snap_id}'
Write_Pickle_Directory( sim_data, file_name )

