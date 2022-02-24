import os, sys
from pathlib import Path
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools')
from tools import *



def Get_Grid_Params( root_dir, base_key='S'):
  sim_dirs = [ root_dir + dir for dir in os.listdir(root_dir) if dir[0] == base_key ]
  sim_dirs.sort()

  grid_sim_params = {} 
  for sim_id, sim_dir in enumerate( sim_dirs ):
    sim_param_file = sim_dir + '/uvb_params.txt'
    file = open( sim_param_file )
    lines = file.readlines()
    sim_params = {}
    for line in lines:
      line = line[:-2]
      param_name, param_val = line.split('=')
      param_val = float( param_val )
      sim_params[param_name] = param_val
    grid_sim_params[sim_id] = sim_params
  return grid_sim_params, sim_dirs


def Select_Simulations_local( self, params_to_select, tolerance=5e-3, ):
  vals_to_find = { key:params_to_select[key] for key in params_to_select if params_to_select[key] != None }
  selected_sims = []

  print(f'Selecting from grid: {self.root_dir}')
  sim_ids = self.sim_ids
  for sim_id in sim_ids: 
    sim_data = self.Grid[sim_id]
    sim_parameters = sim_data['parameters']
    sim_vals = { key:sim_parameters[key] for key in vals_to_find }
    same_vals = True
    for key in sim_vals:
      if np.abs( sim_vals[key] - vals_to_find[key] ) > tolerance: same_vals = False
    if same_vals: selected_sims.append( sim_id )
  
  return selected_sims
  

def Select_Simulations_From_Grid( params_to_select, grid_params=None, tolerance=5e-3, SG=None ):
  vals_to_find = { key:params_to_select[key] for key in params_to_select if params_to_select[key] != None }
  selected_sims = []

  
  if grid_params is not None:
    for sim_id in grid_params:
      sim_parameters = grid_params[sim_id]
      sim_vals = { key:sim_parameters[key] for key in vals_to_find }
      same_vals = True
      for key in sim_vals:
        if np.abs( sim_vals[key] - vals_to_find[key] ) > tolerance: same_vals = False
      if same_vals: selected_sims.append( sim_id )
  
  if SG is not None:
    print(f'Selecting from grid: {SG.root_dir}')
    sim_ids = SG.sim_ids
    for sim_id in sim_ids: 
      sim_data = SG.Grid[sim_id]
      sim_parameters = sim_data['parameters']
      sim_vals = { key:sim_parameters[key] for key in vals_to_find }
      same_vals = True
      for key in sim_vals:
        if np.abs( sim_vals[key] - vals_to_find[key] ) > tolerance: same_vals = False
      if same_vals: selected_sims.append( sim_id )
  
  return selected_sims

def Fit_Grid_Phase_Diagram_MPI( self, n_mpi=30, n_nodes=1 ):
  print("Fitting Phase Diagram:")
  for sim_id in self.Grid.keys():
    self.Fit_Simulation_Phase_Diagram_MPI( sim_id, n_mpi=n_mpi, n_nodes=n_nodes )

def Fit_Simulation_Phase_Diagram_MPI( self, sim_id, n_mpi=30,  n_nodes=1  ):
  print( f' Fitting Simulation: {sim_id}')
  fit_is_done = False
  sim_key = self.Grid[sim_id]['key']
  input_dir = self.analysis_dir + sim_key + '/'
  analysis_files = [f for f in os.listdir(input_dir) if os.path.isfile(input_dir+f)]
  n_analysis_files = len(analysis_files)
  found_dirs = [d for d in os.listdir(input_dir) if os.path.isdir(input_dir+d)]
  if len(found_dirs) == 1:
    fit_dir = input_dir + found_dirs[0] + '/'
    files = [f for f in os.listdir(fit_dir) if os.path.isfile(fit_dir+f)]
    n_files = len(files)
    print( f'  Skipping {sim_key}:  n_analysis: {n_analysis_files}  n_fit: {n_files}')
  # run_file = root_dir + '/phase_diagram/fit_phase_diagram_mpi.py'
  # parameters = input_dir
  # n_per_node = n_mpi // n_nodes + 1
  # command = f'mpirun -n {n_mpi} --map-by ppr:{n_per_node}:node --oversubscribe python {run_file} {parameters}'
  # print( f' Submitting: {command}' )
  # os.system( command )

def Delete_grid_core_files( self ):
 sim_ids = self.sim_ids
 for sim_id in sim_ids:
   self.Delete_simulation_core_files( sim_id )
 
def Delete_simulation_core_files( self, sim_id ):
 sim_dir = self.Get_Simulation_Directory( sim_id )
 files = os.listdir( sim_dir )
 for file in files:
   if file.find('core') == 0:
     print( f'Removing: {sim_dir + file} ' )
     os.remove( sim_dir + file )
 
def Load_Grid_UVB_Rates( self ):
  print( 'Loading UVB Rates Files')
  sim_ids = self.Grid.keys()
  rates_data = {}
  for sim_id in sim_ids:
    rates = self.Load_Simulation_UVB_Rates( sim_id )
    rates_data[sim_id] = rates
  return rates_data
  
def Load_Simulation_UVB_Rates( self, sim_id ):
  sim_dir = self.Get_Simulation_Directory( sim_id )
  file_name = sim_dir + 'UVB_rates.h5'
  print( f' Loading File: {file_name}')
  file = h5.File( file_name, 'r' )
  rates = file['UVBRates']
  rates_out = {}
  for root_key in rates.keys():
    rates_out[root_key] = {}
    data_group = rates[root_key]
    if root_key in [ 'Chemistry', 'Photoheating']:
      for key in data_group.keys():
        rates_out[root_key][key] = data_group[key][...]
    else:
      rates_out[root_key] = data_group[...]
  self.Grid[sim_id]['UVB_rates'] = rates_out
  return { 'UVBRates': rates_out }