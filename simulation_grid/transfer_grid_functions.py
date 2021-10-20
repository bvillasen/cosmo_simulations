import os, sys
from os import listdir
from os.path import isfile, join, isdir
import numpy as np



def Link_Simulation_dirctories( src_params, dst_params ):
  param_names = dst_params[0]['parameters'].keys()
  n_params = len( param_names )
  n_src_sims = len( src_params )
  n_dst_sims = len( dst_params )
  dst_array = np.zeros([ n_dst_sims, n_params ])
  src_array = np.zeros([ n_src_sims, n_params ]) 

  for sim_id in range( n_src_sims ):
    sim_params = src_params[sim_id]['parameters']
    for param_id, param_name in enumerate(param_names):
      src_array[sim_id, param_id] = sim_params[param_name]
      
  for sim_id in range( n_dst_sims ):
    sim_params = dst_params[sim_id]['parameters']
    for param_id, param_name in enumerate(param_names):
      dst_array[sim_id, param_id] = sim_params[param_name]
      
  for sim_id in range( n_dst_sims ):
    dst_param_vals = dst_array[sim_id]
    diff = np.abs( src_array - dst_param_vals ).sum(axis=1)
    indx_src = np.where(diff == 0)[0]
    if len( indx_src ) == 0: src_dir = None
    if len( indx_src ) == 1: 
      src_sim_sir, src_id, src_name = src_params[indx_src[0]]['root_dir'], indx_src[0], src_params[indx_src[0]]['name']
      src_dir = {}
      src_dir['root_dir'] = src_sim_sir
      src_dir['id'] = src_id
      src_dir['name'] = src_name
    if len( indx_src ) > 1:
      print( 'Error More that one sims match')
      exit(-1)
    dst_params[sim_id]['src'] = src_dir
    



def Get_Grid_Parameter_Values( grid_dir, constant_params=None, base_dir='simulation_files/', params_file_name='grid_params.txt' ):
  root_dir = grid_dir
  grid_dir += base_dir
  sim_dirs = [f for f in listdir(grid_dir) if (isdir(join(grid_dir, f)) and (f[0] == 'S' ) ) ]
  sim_dirs.sort()
  grid_params = {}  
  for sim_id, sim_dir in enumerate(sim_dirs):
    grid_params[sim_id] = {}
    grid_params[sim_id]['name'] = sim_dir
    grid_params[sim_id]['root_dir'] = root_dir 
    sim_dir = grid_dir + sim_dir
    params_file = sim_dir + '/' + params_file_name
    file = open( params_file, 'r' )
    lines = file.readlines()
    params = {}
    for line in lines:
      if line[0] == '#': continue
      param_name, param_val = line.split('=') 
      params[param_name] = float( param_val )
    if constant_params is not None:
      for p_name in constant_params:
        params[p_name] = constant_params[p_name]
    grid_params[sim_id]['parameters'] = params
    file.close()
    
  return grid_params

