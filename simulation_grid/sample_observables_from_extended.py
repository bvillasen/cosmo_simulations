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
from simulation_grid_data_functions import Get_Data_Grid_Composite
from mcmc_sampling_functions import Get_Highest_Likelihood_Params, Sample_Fields_from_Trace, Sample_Power_Spectrum_from_Trace


output_dir = root_dir + 'extended_samples/'
create_directory( output_dir )


load_global_properties = True

# sim_ids = range(10)
sim_ids = None
SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
SG.Load_Grid_Analysis_Data( sim_ids=sim_ids, load_pd_fit=True, mcmc_fit_dir='fit_mcmc_delta_0_1.0', load_thermal=load_global_properties)
params = SG.parameters

n_val_per_param = 25
params_extended = {}
param_vals = {}
for p_id in params:
  p_name = params[p_id]['name']
  p_vals = params[p_id]['values']
  p_min, p_max = min( p_vals ), max( p_vals )
  vals_extended = np.linspace( p_min, p_max, n_val_per_param )
  params_extended[p_id] = { 'name':p_name, 'values':vals_extended }
  param_vals[p_id] = vals_extended
  
param_combinations = Get_Parameters_Combination( param_vals )  
param_combinations = np.array( param_combinations ).T
for p_id in params:
  params_extended[p_id]['trace'] = param_combinations[p_id]


kmax = 0.1
ps_range = SG.Get_Power_Spectrum_Range( kmax=kmax )
sim_ids = SG.sim_ids

z_vals = [ 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4,  4.6, 5.0   ]
fields_to_sample = ['P(k)', 'T0', 'gamma', 'tau', 'tau_HeII', ]
if load_global_properties: fields_to_sample.append( 'z_ion_H' )
data_grid, data_grid_power_spectrum = Get_Data_Grid_Composite(  fields_to_sample, SG, z_vals=z_vals, sim_ids=sim_ids, load_uvb_rates=False )

hpi_sum = 0.95

# Obtain distribution of the power spectrum
file_name = output_dir + 'samples_power_spectrum.pkl'
samples_ps = Sample_Power_Spectrum_from_Trace( params_extended, data_grid_power_spectrum, SG, hpi_sum=hpi_sum, output_trace=True )
Write_Pickle_Directory( samples_ps, file_name )

# # Obtain distribution of the other fields
# file_name = output_dir + 'samples_fields.pkl' 
# field_list = ['T0', 'gamma', 'tau', 'tau_HeII']
# if load_global_properties: field_list.append( 'z_ion_H' )
# samples_fields = Sample_Fields_from_Trace( field_list, params_extended, data_grid, SG, hpi_sum=hpi_sum, output_trace=True)
# Write_Pickle_Directory( samples_fields, file_name )



