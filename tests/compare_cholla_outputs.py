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

# data_dir = '/gpfs/alpine/csc434/scratch/bvilasen/'
data_dir = '/data/groups/comp-astro/bruno/'
# data_dir = '/raid/bruno/data/'
input_dir = data_dir + 'cosmo_sims/256_hydro_50Mpc/'
output_dir = data_dir + 'cosmo_sims/256_hydro_50Mpc/figures/'
create_directory( output_dir ) 

precision = np.float64
Lbox = 50000.0    #kpc/h
n_cells = 256
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid


n_snaps = 60

fields = [ 'density'  ]

diff_all = []
z_all = []
# for n_snapshot in range(n_snaps):
# 
#   #Load DM data
#   data = load_snapshot_data_distributed( 'hydro', fields, n_snapshot, input_dir_0+'snapshot_files/', box_size, grid_size,  precision, show_progess=True, print_fields=True )
#   dens_0 = data['density']          
# 
#   data = load_snapshot_data_distributed( 'hydro', fields, n_snapshot, input_dir_1, box_size, grid_size,  precision, show_progess=True, print_fields=True )
#   dens_1 = data['density']    
# 
#   diff = np.abs( dens_0 - dens_1 ) / dens_0
# 
#   print( f'\nDiff Mean: {diff.mean()}')
#   print( f'Diff Max: {diff.max()}')
# 
#   diff_all.append( diff.max() )

f_min = 1e-3 
ps_min = 1e-10 
for n_file in range(56):
  file_name = input_dir + f'analysis_files/{n_file}_analysis.h5'
  file = h5.File( file_name, 'r' )
  pd = file['phase_diagram']['data'][...]
  skewers_keys = [ 'skewers_x', 'skewers_y', 'skewers_z' ]
  skewers_0 = {} 
  for skewers_key in skewers_keys:
    skewers = file['lya_statistics'][skewers_key]
    v_0 = skewers['vel_Hubble'][...]
    F_H_0  = skewers['los_transmitted_flux_HI'][...]
    F_He_0 = skewers['los_transmitted_flux_HeII'][...]
    F_H_0[ F_H_0 < f_min ] = f_min
    F_He_0[ F_He_0 < f_min ] = f_min
    skewers_0[skewers_key] = {'v':v_0, 'F_H':F_H_0, 'F_He':F_He_0 }
    
    
  ps_0 = file['lya_statistics']['power_spectrum']['p(k)'][...]
  k_vals_0 = file['lya_statistics']['power_spectrum']['k_vals'][...]    
    

  file_name = input_dir + f'skewers_files/{n_file}_skewers.h5'
  file = h5.File( file_name, 'r' )
  skewers_1 = {} 
  for skewers_key in skewers_keys:
    skewers = file[skewers_key]
    v_1 = skewers['vel_Hubble'][...]
    F_H_1  = skewers['los_transmitted_flux_HI'][...]
    F_He_1 = skewers['los_transmitted_flux_HeII'][...]
    F_H_1[ F_H_1 < f_min ] = f_min
    F_He_1[ F_He_1 < f_min ] = f_min
    skewers_1[skewers_key] = {'v':v_1, 'F_H':F_H_1, 'F_He':F_He_1 }
  
  for key in ['v', 'F_H', 'F_He' ]:
    print (f'Key: {key}')
    for skewers_key in skewers_keys:
      print( f' Skewers: {skewers_key}' )
      vals_0 = skewers_0[skewers_key][key]
      vals_1 = skewers_1[skewers_key][key]
      diff = ( np.abs( F_H_1 - F_H_0) / F_H_0 ).max() 
      print(f'  diff: {diff} ')
    
  file_name = input_dir + f'analysis_files_1/{n_file}_analysis.h5'
  file = h5.File( file_name, 'r' )
  pd = file['phase_diagram']['data'][...]
  ps_1 = file['lya_statistics']['power_spectrum']['p(k)'][...]
  k_vals_1 = file['lya_statistics']['power_spectrum']['k_vals'][...]    


  ps_0[ ps_0 < ps_min ] = ps_min
  ps_1[ ps_1 < ps_min ] = ps_min
  
  diff_k = ( np.abs( k_vals_1 - k_vals_0) / k_vals_0 ).max()
  diff_ps = ( np.abs( ps_1 - ps_0) / ps_0 ).max()
    
  print( diff_k )
  print( diff_ps )
  
