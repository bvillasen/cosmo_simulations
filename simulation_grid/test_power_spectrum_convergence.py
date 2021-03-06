import os, sys
import numpy as np
import pickle
import pymc
import matplotlib.pyplot as plt
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_grid_parameters import Grid_Parameters
from simulation_grid import Simulation_Grid
from simulation_parameters import *
from interpolation_functions import Interpolate_multi_dimensional_from_grid
from mcmc_data_functions import Get_Comparable_Composite, Get_Comparable_Composite_from_Grid
from plot_mcmc_functions import Plot_Comparable_Data

# Directories 
ps_data_dir = base_dir + '/lya_statistics/data/'
output_dir = data_dir + 'figures/wdm/pk_convergence/'
create_directory( output_dir )

# Fields to interpolate
fields_to_fit = 'P(k)+'
data_ps_sets = [ 'Boera' ]

use_inv_wdm = True
# Change wdm_mass to inv_wdm_mass
if use_inv_wdm: Grid_Parameters = Invert_wdm_masses( Grid_Parameters )




#Load custom power spectrum measurement
custom_ps_data = { 'root_dir': root_dir + 'flux_power_spectrum', 'file_base_name':'flux_ps_sampled_boera_extended', 'stats_base_name':None }
custom_data = { 'P(k)': custom_ps_data } 

sim_ids = None
SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
SG.Load_Grid_Analysis_Data( sim_ids=sim_ids, load_pd_fit=True, mcmc_fit_dir='fit_mcmc_delta_0_1.0', FPS_correction=None, custom_data=custom_data )
grid_params = SG.parameters
print( grid_params)

kmax = 0.2
ps_range = SG.Get_Power_Spectrum_Range( kmax=kmax )

#Define the redshift range for the fit 
z_min, z_max = 4.2, 5.0

# Use P(k) instead of Delta_P(k)
no_use_delta_p = True 

data_systematic_uncertainties = None
load_covariance_matrix = False
ps_parameters = { 'range':ps_range, 'data_dir':ps_data_dir, 'data_sets':data_ps_sets  }
comparable_data = Get_Comparable_Composite( fields_to_fit, z_min, z_max, ps_parameters=ps_parameters, log_ps=False, systematic_uncertainties=data_systematic_uncertainties, no_use_delta_p=no_use_delta_p, load_covariance_matrix=load_covariance_matrix   )
comparable_grid = Get_Comparable_Composite_from_Grid( fields_to_fit, comparable_data, SG, log_ps=False, no_use_delta_p=no_use_delta_p )


param_names = [ 'inv_wdm_mass', 'scale_H_ion', 'scale_H_Eheat', 'deltaZ_H' ]
default_params = { 'inv_wdm_mass':0.0, 'scale_H_ion':1.0, 'scale_H_Eheat':0.9, 'deltaZ_H':0.0 }

# 
# param_to_change = 0
# param_change_name = SG.parameters[param_to_change]['name']
# param_change_vals = SG.parameters[param_to_change]['values']
# pk_data = { 'param_change_name':param_change_name, 'param_change_vals':param_change_vals, 'default_params':default_params, 'pk_samples':{}}
# 
# for data_id, p_change_val in enumerate(param_change_vals):
#   selected_parameters = {}
#   # Fill wit the default values
#   for p_name in param_names: selected_parameters[p_name] = default_params[p_name]
#   # Change the parameter to vary
#   selected_parameters[param_change_name] = p_change_val
#   selected_sim_id = SG.Select_Simulations( selected_parameters )[0]
#   pk_from_sim = comparable_grid[selected_sim_id][fields_to_fit]['mean']
#   param_vals = [ selected_parameters[p_name] for p_name in param_names ]
#   pk_interpolated = Interpolate_multi_dimensional_from_grid( param_vals, comparable_grid, fields_to_fit, 'mean', SG )  
#   print( pk_from_sim/pk_interpolated)
#   pk_data['pk_samples'][data_id] = {'simulation':pk_from_sim, 'interpolated':pk_interpolated }
# 
# file_name = output_dir + 'pk_from_simulations.pkl'
# Write_Pickle_Directory( pk_data, file_name )




default_params = { 'inv_wdm_mass':0.0, 'scale_H_ion':0.9, 'scale_H_Eheat':1.0, 'deltaZ_H':0.25 }

param_to_change = 0
param_change_name = SG.parameters[param_to_change]['name']
param_change_vals = 1/np.array([ 1.5, 2.5, 3.5, 5.5, 7.0, 10.0, 15.0, 30.0, 50.0, 1000000 ])
pk_data = { 'param_change_name':param_change_name, 'param_change_vals':param_change_vals, 'default_params':default_params, 'pk_samples':{}}
for data_id, p_change_val in enumerate(param_change_vals):
  selected_parameters = {}
  # Fill wit the default values
  for p_name in param_names: selected_parameters[p_name] = default_params[p_name]
  # Change the parameter to vary
  selected_parameters[param_change_name] = p_change_val
  param_vals = [ selected_parameters[p_name] for p_name in param_names ]
  print( f'Interppolate to: {param_vals}')
  pk_interpolated = Interpolate_multi_dimensional_from_grid( param_vals, comparable_grid, fields_to_fit, 'mean', SG )  
  pk_data['pk_samples'][data_id] = {'interpolated':pk_interpolated }

file_name = output_dir + 'pk_interpolated.pkl'
Write_Pickle_Directory( pk_data, file_name )


# 
# param_to_change = 2
# param_change_name = SG.parameters[param_to_change]['name']
# param_change_vals = [0.6, 0.8, 1.0, 1.2, 1.4, 1.6 ]
# pk_data = { 'param_change_name':param_change_name, 'param_change_vals':param_change_vals, 'default_params':default_params, 'pk_samples':{}}
# for data_id, p_change_val in enumerate(param_change_vals):
#   selected_parameters = {}
#   # Fill wit the default values
#   for p_name in param_names: selected_parameters[p_name] = default_params[p_name]
#   # Change the parameter to vary
#   selected_parameters[param_change_name] = p_change_val
#   param_vals = [ selected_parameters[p_name] for p_name in param_names ]
#   pk_interpolated = Interpolate_multi_dimensional_from_grid( param_vals, comparable_grid, fields_to_fit, 'mean', SG )  
#   pk_data['pk_samples'][data_id] = {'interpolated':pk_interpolated }
# 
# file_name = output_dir + f'pk_{param_change_name}_interpolated.pkl'
# Write_Pickle_Directory( pk_data, file_name )
