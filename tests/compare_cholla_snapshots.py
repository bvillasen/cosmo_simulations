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

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

Lbox = 50000.0    #kpc/h
n_cells = 1024
n_snaps = 60

sim_dir = data_dir + f'cosmo_sims/{n_cells}_50Mpc_adiabatic/'
input_dir_0 = sim_dir + 'snapshot_files_caar_0/'
input_dir_1 = sim_dir + 'snapshot_files_caar/'
output_dir  = sim_dir + 'figures/'

# input_dir_0 = data_dir + 'cosmo_sims/1024_50Mpc_adiabatic/snapshot_files_caar/'
# input_dir_1 = data_dir + 'cosmo_sims/1024_50Mpc_adiabatic/sim_cosmo/snapshot_files/'
# output_dir  = data_dir + 'cosmo_sims/1024_50Mpc_adiabatic/figures/'

create_directory( output_dir ) 

precision = np.float64
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid



# fields = [ 'density', 'momentum_x', 'momentum_y', 'momentum_z', 'GasEnergy', 'Energy'  ]
fields = [ 'density' ]
diff = {}

data_type = 'hydro'

v_min = 1e-10
for n_snapshot in range(n_snaps):

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
    
    if field not in diff: diff[field] = [] 
    diff_vals = np.abs( dens_0 - dens_1 ) / dens_0
    diff_max = diff_vals.max()
    diff[field].append( diff_max )
    
    print( f'n: {n_snapshot}  z: {z}  Diff {data_type} {field} min: {diff_vals.min()}   max: {diff_vals.max()}   Mean: {diff_vals.mean()}')
