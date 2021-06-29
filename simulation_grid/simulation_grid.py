import os, sys
from pathlib import Path
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools')
from tools import *
import subprocess
#Append analysis directories to path
extend_path()
from submit_job_scripts import Create_Submit_Job_Script_Lux, Create_Submit_Job_Script_Summit
from generate_grackle_uvb_file import Generate_Modified_Rates_File
from load_data import load_analysis_data
from phase_diagram_functions import fit_thermal_parameters_mcmc, get_density_temperature_values_to_fit
from simulation_parameters import system, load_reduced_files


def Combine_List_Pair( a, b ):
  output = []
  for a_i in a:
    for b_i in b:
      if type(b_i) == list:
        add_in = [a_i] + b_i
      else:
        add_in = [ a_i, b_i]
      output.append( add_in )
  return output
  

 
class Simulation_Grid:
  n_paramters   = 0
  n_simulations = 0
  parameter_names = []
  root_dir = ''
  sim_param_indx_grid = None
  parameters = None
  Grid = None
  job_parameters = None
  simulation_parameters = None
  sim_ids = None
  
  def __init__( self, job_params=None, sim_params=None, parameters=None, dir=None ):
    print("Initializing Simulation Grid:")
    root_dir = dir
    n_param = len(parameters.keys())
    param_names = [ parameters[i]['name'] for i in range(n_param) ]
    n_sims = np.prod( [ len(parameters[i]['values']) for i in range(n_param) ] )  
    self.parameter_names = param_names
    self.n_paramters = n_param
    self.n_simulations = n_sims
    self.parameters = parameters
    self.root_dir = dir
    self.snapshots_dir = dir + 'snapshot_files/'
    self.job_parameters = job_params
    self.simulation_parameters = sim_params
    print( f" n_paramters: {self.n_paramters}")
    print( f" Paramters: {self.parameter_names}")
    print( f" n_simulations: {self.n_simulations}")
    print( f" Root Dir: {self.root_dir}")
    
    create_directory( self.root_dir )
    create_directory( self.snapshots_dir )
    
    param_keys = []
    indices_list = []
    for i in range(n_param):
      param_id = n_param - 1 - i
      param_keys.append( parameters[param_id]['key'] )
      n_vals = len( parameters[param_id]['values'] )
      indices_list.append( [ x for x in range(n_vals)] )
    
    sim_param_indx_grid = indices_list[0]
    for i in range( n_param-1 ):
      sim_param_indx_grid = Combine_List_Pair( indices_list[i+1], sim_param_indx_grid )
    assert( len(sim_param_indx_grid) == n_sims ), "N_simulations doesn't match Simulation Grid"
        
    sim_grid  = {}
    for sim_id in range( n_sims ):
      sim_grid[sim_id] = {}
      sim_grid[sim_id]['param_indices'] = sim_param_indx_grid[sim_id]
      name = 'S{0:03}'.format( sim_id )
      coords = ''
      for param_id in range(n_param):
        param = parameters[param_id]
        param_key = param['key']
        name += f'_{param_key}{sim_param_indx_grid[sim_id][param_id]}'
        coords += f'_{param_key}{sim_param_indx_grid[sim_id][param_id]}'
      sim_grid[sim_id]['key'] = name
      sim_grid[sim_id]['coords'] = coords[1:] 

    
    for sim_id in range( n_sims ):
      sim_parameters = {}
      param_indices = sim_grid[sim_id]['param_indices']
      for param_id in range(n_param):
        param = parameters[param_id]
        param_name = param['name']
        param_indx = param_indices[param_id]
        param_val = parameters[param_id]['values'][param_indx]
        sim_parameters[param_name] = param_val
      sim_grid[sim_id]['parameters'] = sim_parameters
    
    coords = {}  
    for sim_id in range( n_sims ):
      coords[sim_grid[sim_id]['coords']] = sim_id
      
    
    for sim_id in range( n_sims ):
      parameter_values = []
      for p_id in range(n_param):
        p_name = parameters[p_id]['name']
        p_val = sim_grid[sim_id]['parameters'][p_name]
        parameter_values.append( p_val )
      sim_grid[sim_id]['parameter_values'] = np.array( parameter_values )
      
        
    self.Grid = sim_grid
    self.sim_ids = self.Grid.keys()
    self.coords = coords
    
