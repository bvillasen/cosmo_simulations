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

simulation_dir = data_dir + f'cosmo_sims/1024_25Mpc_fragmentation/cdm/'
input_dir = simulation_dir + f'snapshot_files/'
output_dir = simulation_dir + 'power_spectrum_files/'
create_directory( output_dir )

args = sys.argv[1:]
data_type = args[0]
# data_type = 'hydro'
# data_type = 'particles'

snap_ids = np.array([ 6, 7, 8 ])
snap_ids_local = split_array_mpi( snap_ids, rank, n_procs )

print( snap_ids_local )
Lbox = 25000.0    #kpc/h
n_cells = 1024
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
precision = np.float64
fields = [ 'density' ]

n_bins = 25
Lbox = Lbox/1e3    #Mpc/h
nx, ny, nz = grid_size
dx, dy, dz = Lbox/nx, Lbox/ny, Lbox/nz


for snap_id in snap_ids_local:
  snap_data = load_snapshot_data_distributed( data_type, fields,  snap_id, input_dir,  box_size, grid_size, precision  )
  z = snap_data['Current_z']
  density = snap_data['density']
  print( f'Computing Power Spectrum  snap_id: {snap_id}  z:{z}' )
  power_spectrum, k_vals, n_in_bin = get_power_spectrum( density, Lbox, nx, ny, nz, dx, dy, dz,  n_kSamples=n_bins )
  sim_data = { 'z':z, 'k_vals':k_vals, 'power_spectrum':power_spectrum, 'n_in_bin':n_in_bin }
  
  file_name = output_dir + f'power_spectrum_{data_type}_{snap_id}.pkl'
  Write_Pickle_Directory( sim_data, file_name )

