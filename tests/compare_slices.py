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

sim_dir = data_dir + 'cosmo_sims/1024_50Mpc/'
input_dir_0 = sim_dir + 'snapshot_files_grackle/'
input_dir_1 = sim_dir + 'snapshot_files_cholla/'
output_dir  = sim_dir + 'figures/slices/'
create_directory( output_dir ) 

precision = np.float64
Lbox = 50000.0    #kpc/h
n_cells = 1024
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid


data_type = 'hydro'

# fields = [ 'density', 'momentum_x', 'momentum_y', 'momentum_z', 'GasEnergy', 'Energy'  ]
fields = [ 'density' ]
diff = {}


n_snapshot = 10 
data_0 = load_snapshot_data_distributed( data_type, fields, n_snapshot, input_dir_0, box_size, grid_size,  precision, show_progess=False )
data_1 = load_snapshot_data_distributed( data_type, fields, n_snapshot, input_dir_1, box_size, grid_size,  precision, show_progess=False )
z_0 = data_0['Current_z']
z_1 = data_1['Current_z']
if np.abs( z_0 - z_1 ) > 1e-3:
  print( 'ERROR: Redshift of snapshots does not match')
  exit(-1)  
  
  