import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
import pylab
import palettable
root_dir =  os.path.dirname(os.getcwd())  + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from colors import *


base_dir = data_dir + 'cosmo_sims/rescaled_P19/'

files_to_load = [ 25, 35, 45, 55 ][::-1]
files_to_load = range(15, 56 )[::-1]


sim_names = [ '2048_50Mpc',  '1024_50Mpc',  ]
n_sims = len( sim_names )



data_all = {}
for sim_id, sim_name in enumerate(sim_names): 
  name_vals, extra = sim_name.split('Mpc')
  n_cells, Lbox_Mpc = name_vals.split('_')
  n_cells = int( n_cells )
  Lbox_Mpc = int( Lbox_Mpc )
  
  data_all[sim_id] = { 'n_cells': n_cells, 'Lbox_Mpc': Lbox_Mpc }
  input_dir = base_dir + f'{sim_name}/analysis_files/'
  data_sim = {}
  for z_id, n_file in enumerate( files_to_load ):
    file_name = input_dir + f'{n_file}_analysis.h5'
    print( f'Loading File: {file_name}' )
    file = h5.File( file_name )
    Lbox = file.attrs['Lbox']
    current_z = file.attrs['current_z'][0]
    ps_mean = file['lya_statistics']['power_spectrum']['p(k)'][...]
    k_vals  = file['lya_statistics']['power_spectrum']['k_vals'][...]
    indices = ps_mean > 0
    ps_mean = ps_mean[indices]
    k_vals  = k_vals[indices]
    ps_mean = ps_mean
    k_vals = k_vals
    data_sim[z_id] = { 'z':current_z, 'k_vals':k_vals, 'ps_mean':ps_mean }
  data_all[sim_id]['data_ps'] = data_sim

id_0 = 0

ps_diff_data = {}

sim_id = 1

for z_id, n_file in enumerate(files_to_load):

  ps_data_0 = data_all[id_0]['data_ps'][z_id]
  z_0 = ps_data_0['z']
  ps_mean_0 = ps_data_0['ps_mean']
  k_vals_0 = ps_data_0['k_vals']

  sim_data = data_all[sim_id]
  data_ps = sim_data['data_ps'][z_id]
  z = data_ps['z']
  k_vals  = data_ps['k_vals']
  ps_mean = data_ps['ps_mean']
  n_kvals = len( k_vals )
  
  if z != z_0:
    print( 'ERROR: Redshift miusmatch')
    exit(-1)
  
  k_vals_reference = k_vals_0[:n_kvals]
  ps_reference = ps_mean_0[:n_kvals]
  k_diff = np.abs(  k_vals - k_vals_reference )
  ps_diff = ( ps_mean  ) / ps_reference 
  print( f'\nz: {z}' )
  print( f'Diff k_vals: {k_diff.sum()}' )
  print( f'Diff ps: {ps_diff}' )
  ps_diff_data[z_id] = { 'z':z, 'k_vals':k_vals, 'delta_factor':ps_diff  }
     
ps_diff_data['z_vals'] = np.array([ ps_diff_data[i]['z'] for i in ps_diff_data])     
     
file_name = base_dir + 'FPS_resolution_correction_1024_50Mpc.pkl'
Write_Pickle_Directory( ps_diff_data, file_name )




