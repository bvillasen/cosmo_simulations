import os, sys
from os import listdir
from os.path import isfile, join
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from load_data import load_snapshot_data_distributed
from tools import *

use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

Lbox = 50000.0    #kpc/h
# n_cells = 1024
n_cells = 256

snapshots = np.arange( 0, 1, 1, dtype=int )
# snapshots = np.arange( 0, 170, 1, dtype=int )
snapshots_local = split_array_mpi( snapshots, rank, n_procs )
print( f'rank: {rank}  snapshots_local:{snapshots_local}' )

sim_dir = data_dir + f'cosmo_sims/{n_cells}_50Mpc/'
input_dir_0 = sim_dir + 'snapshot_files_8/'
input_dir_1 = sim_dir + 'snapshot_files/'

# sim_dir = data_dir + f'cosmo_sims/{n_cells}_50Mpc/'
# input_dir_0 = sim_dir + 'snapshot_files_cosmo/'
# input_dir_1 = sim_dir + 'snapshot_files_merge_grackle/'


# input_dir_0 = data_dir + 'cosmo_sims/1024_50Mpc_adiabatic/snapshot_files_caar/'
# input_dir_1 = data_dir + 'cosmo_sims/1024_50Mpc_adiabatic/sim_cosmo/snapshot_files/'

output_dir  = sim_dir + 'figures/'
if rank ==0: create_directory( output_dir ) 
if rank ==0: print( f'Input 0: {input_dir_0}')
if rank ==0: print( f'Input 1: {input_dir_1}')

data_type = 'hydro'
# data_type = 'particles'
precision = np.float64
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid



# fields = [ 'density', 'momentum_x', 'momentum_y', 'momentum_z', 'GasEnergy', 'Energy'  ]
fields = [ 'density' ]
diff = {}


v_min = 1e-10
for n_snapshot in snapshots_local:

  data_0 = load_snapshot_data_distributed( data_type, fields, n_snapshot, input_dir_0, box_size, grid_size,  precision, show_progess=False )
  data_1 = load_snapshot_data_distributed( data_type, fields, n_snapshot, input_dir_1, box_size, grid_size,  precision, show_progess=False )
  z_0 = data_0['Current_z']
  z_1 = data_1['Current_z']
  if np.abs( z_0 - z_0 ) > 1e-3: print( f'Large redshift difference: {z_0}  {z_1}' )
  z = z_0
  
  if 'z' not in diff: diff['z'] = []
  diff['z'].append(z)          
  
  for field in fields:
    dens_0 = data_0[field]
    dens_1 = data_1[field]
    
    if field in [ 'density' ]:
      dens_0[dens_0<v_min] = v_min
      dens_1[dens_1<v_min] = v_min
    
    if field not in diff: diff[field] = [] 
    diff_vals = np.abs( dens_0 - dens_1 ) / dens_0
    diff_max = diff_vals.max()
    diff[field].append( diff_max )
    
    print( f'n: {n_snapshot:03}  z: {z:.2f}  Diff {data_type} {field} min: {diff_vals.min():.3e}   max: {diff_vals.max():.3e}   Mean: {diff_vals.mean():.3e}')
