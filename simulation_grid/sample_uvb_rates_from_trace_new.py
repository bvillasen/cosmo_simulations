import os, sys, time
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
from mcmc_sampling_functions import Get_Highest_Likelihood_Params, Get_1D_Likelihood_max, Get_Params_mean,Sample_Fields_from_Trace, Sample_Power_Spectrum_from_Trace
from uvb_functions import Load_Grackle_File, Modify_UVB_Rates, Extend_Rates_Redshift, Copy_Grakle_UVB_Rates
from stats_functions import compute_distribution, get_highest_probability_interval

# data_name = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera_systematic'
data_name = 'fit_results_covariance_systematic'

ps_data_dir = 'lya_statistics/data/'
mcmc_dir = root_dir + 'fit_mcmc/'
input_dir = mcmc_dir + f'{data_name}/' 
output_dir = input_dir + 'observable_samples/'
create_directory( output_dir )


SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
params = SG.parameters

stats_file = input_dir + 'fit_mcmc.pkl'
samples_file = input_dir + 'samples_mcmc.pkl'


print( f'Loading File: {stats_file}')
stats = pickle.load( open( stats_file, 'rb' ) )
for p_id in params.keys():
  p_name = params[p_id]['name']
  p_stats = stats[p_name]
  params[p_id]['mean'] = p_stats['mean']
  params[p_id]['sigma'] = p_stats['standard deviation']
print( f'Loading File: {samples_file}')
param_samples = pickle.load( open( samples_file, 'rb' ) )


# Get the Highest_Likelihood parameter values 
params_HL = Get_Highest_Likelihood_Params( param_samples, n_bins=10 )


hpi_sum = 0.95
n_samples = 400000

load_samples = False


grackle_file_name = base_dir + 'rates_uvb/CloudyData_UVB_Puchwein2019_cloudy.h5'
grackle_data = Load_Grackle_File( grackle_file_name )
max_delta_z = 0.02
rates_data = Extend_Rates_Redshift( max_delta_z, grackle_data )
# rates_data = grackle_data

field_list = ['photoheating_HI', 'photoheating_HeI', 'photoheating_HeII', 'photoionization_HI', 'photoionization_HeI', 'photoionization_HeII' ]
rates_samples = {}
for field in field_list:
  rates_samples[field] = []

start = time.time()
for sample_id in range(n_samples ):
  parameter_values = {}
  for p_id in param_samples:
    p_name = param_samples[p_id]['name']
    p_val = param_samples[p_id]['trace'][sample_id]
    parameter_values[p_name] = p_val
    # p_val = params_HL[p_id][0]
    parameter_values[p_name] = p_val
  # print( parameter_values )
  input_rates = Copy_Grakle_UVB_Rates( rates_data )
  rates_modified = Modify_UVB_Rates( parameter_values, input_rates, extrapolate='spline' )
  for field in field_list:
    rates_samples[field].append(  rates_modified[field] )
  print_progress( sample_id+1, n_samples, start )
print('')

if params_HL is not None:
  parameter_values_HL = {}
  for p_id in param_samples:
    p_name = param_samples[p_id]['name']
    p_val = params_HL[p_id]
    parameter_values_HL[p_name] = p_val
  input_rates = Copy_Grakle_UVB_Rates( rates_data )  
  rates_modified_HL = Modify_UVB_Rates( parameter_values_HL, input_rates, extrapolate='spline' )


samples_uvb_rates = {}
for field in field_list:
  print( f'Obtaining Distribution: {field} ' )
  samples_stats = {}
  samples = rates_samples[field]
  samples = np.array( samples ).T
  mean = np.array([ vals.mean() for vals in samples ])
  sigma = [ ]
  lower, higher = [], []
  for i in range( len( samples ) ):
    sigma.append( np.sqrt(  ( (samples[i] - mean[i])**2).mean()  ) )
    values = samples[i]
    n_bins = 100
    distribution, bin_centers = compute_distribution( values, n_bins, log=False )
    fill_sum = hpi_sum
    log_hpi = True
    v_l, v_r, v_max, sum = get_highest_probability_interval( bin_centers, distribution, fill_sum, log=log_hpi, n_interpolate=1000)
    lower.append( v_l )
    higher.append( v_r )
  sigma  = np.array( sigma )
  lower  = np.array( lower )
  higher = np.array( higher )
  samples_stats = {}
  samples_stats['z'] = rates_modified['z']
  samples_stats['mean']   = mean
  samples_stats['sigma']  = sigma
  samples_stats['lower']  = lower
  samples_stats['higher'] = higher
  samples_stats['Highest_Likelihood'] = rates_modified_HL[field]  
  samples_uvb_rates[field] = samples_stats


file_name = output_dir + 'samples_uvb_rates_notextended.pkl' 
Write_Pickle_Directory( samples_uvb_rates, file_name )



