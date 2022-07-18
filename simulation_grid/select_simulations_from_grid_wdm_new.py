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
SG.Load_Grid_Analysis_Data( sim_ids=sim_ids,  load_pd_fit=True, mcmc_fit_dir='fit_mcmc_delta_0_1.0', FPS_correction=None, load_thermal=False )

# 
# param_names = [ 'wdm_mass', 'scale_H_ion', 'scale_H_Eheat', 'deltaZ_H' ]
# default_params = { 'wdm_mass':10000, 'scale_H_ion':1.0, 'scale_H_Eheat':0.9, 'deltaZ_H':0.0 }
# 
# param_id = 0
# param_change_name = SG.parameters[param_id]['name']
# param_change_vals = SG.parameters[param_id]['values']
# for p_change_val in param_change_vals:
#   selected_parameters = {}
#   # Fill wit the default values
#   for p_name in param_names: selected_parameters[p_name] = default_params[p_name]
#   selected_parameters
#   # Change the parameter to vary
#   selected_parameters[param_change_name] = p_change_val
#   selected_sim_id = SG.Select_Simulations( selected_parameters )[0]
#   print( selected_sim_id, selected_parameters )
  
# 
# selected_combination = selected_combinations[rank]
# selected_sim_ids = []
# for selected_combination in selected_combinations:
#   selected_parameters = {'wdm_mass':selected_combination[0], 'scale_H_ion':selected_combination[1], 'scale_H_Eheat':selected_combination[2], 'deltaZ_H':selected_combination[3] }
#   selected_sim_ids.append( selected_sim_id )
