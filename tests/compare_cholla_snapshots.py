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

input_dir_0 = data_dir + 'cosmo_sims/chemistry_test/output_files_grackle/'
input_dir_1 = data_dir + 'cosmo_sims/chemistry_test/output_files/'
output_dir  = data_dir + 'cosmo_sims/chemistry_test/figures/'
create_directory( output_dir ) 

precision = np.float64
Lbox = 50000.0    #kpc/h
n_cells = 64
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid


n_snaps = 46

fields = [ 'density', 'momentum_x', 'momentum_y', 'momentum_z', 'GasEnergy', 'Energy'  ]
z, diff_gas, diff_dm = [], [], []

dens_min = 1e-10
for n_snapshot in range(n_snaps):

  data_0 = load_snapshot_data_distributed( 'hydro', fields, n_snapshot, input_dir_0, box_size, grid_size,  precision, show_progess=False )
  data_1 = load_snapshot_data_distributed( 'hydro', fields, n_snapshot, input_dir_1, box_size, grid_size,  precision, show_progess=False )
  z.append(data_0['Current_z'])          
  
  for field in fields:
    dens_0 = data_0[field]
    dens_1 = data_1[field]
    
    print( f'Field: {field}  min: {dens_0.min()}  max: {dens_0.max()}')    

    diff = np.abs( dens_0 - dens_1 ) / dens_0
    diff_gas.append( diff.max())
    # print( f'\nDiff Hydro {field} min: {diff.min()}   max: {diff.max()}   Mean: {diff.mean()}')

  # 
  # 
  # data = load_snapshot_data_distributed( 'particles', fields, n_snapshot, input_dir_0, box_size, grid_size,  precision )
  # dens_0 = data['density']
  # dens_0[dens_0<dens_min] = dens_min          
  # 
  # data = load_snapshot_data_distributed( 'particles', fields, n_snapshot, input_dir_1, box_size, grid_size,  precision, show_progess=True, print_fields=True )
  # dens_1 = data['density']    
  # dens_1[dens_1<dens_min] = dens_min
  # 
  # diff = np.abs( dens_0 - dens_1 ) / dens_0
  # print( f'\nDiff DM min: {diff.min()}   max: {diff.max()}   Mean: {diff.mean()}')
  # diff_dm.append( diff.max())
