import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_grid_parameters import Grid_Parameters
from simulation_grid import Simulation_Grid
from simulation_parameters import *

  
sim_ids = None
SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
grid_params = SG.parameters

output_dir = SG.root_dir

param_names = ['scale_He', 'scale_H', 'deltaZ_He', 'deltaZ_H']
default_params = { 'scale_He':1.0, 'scale_H':1.0, 'deltaZ_He':0.2, 'deltaZ_H':0.0 }


selected_sims = {}
selected_sims['default_params'] = default_params 

for param_id in grid_params:

  param_change_name = SG.parameters[param_id]['name']
  param_change_vals = SG.parameters[param_id]['values']
  selected_sims[param_id] = {}
  selected_sims[param_id]['param_name'] = param_change_name
  selected_sims[param_id]['param_vals'] = param_change_vals

  selected_sims_param = {}
  for val_id, p_change_val in enumerate(param_change_vals):
    selected_parameters = {}
    # Fill wit the default values
    for p_name in param_names: selected_parameters[p_name] = default_params[p_name]
    # Change the parameter to vary
    selected_parameters[param_change_name] = p_change_val
    selected_sim_id = SG.Select_Simulations( selected_parameters )[0]
    sim_key = SG.Grid[selected_sim_id]['key']
    sim_params = SG.Grid[selected_sim_id]['parameters']
    selected_sims_param[val_id] = { 'sim_id':selected_sim_id, 'sim_key':sim_key, 'sim_params':sim_params }
  selected_sims[param_id]['selected_sims'] = selected_sims_param


file_name = output_dir + 'selected_sims.pkl'
Write_Pickle_Directory( selected_sims, file_name )

