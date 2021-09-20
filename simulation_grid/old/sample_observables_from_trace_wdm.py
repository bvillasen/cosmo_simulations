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


use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

z_indx = rank


# data_name = 'fit_results_P(k)+_Boera'
data_name = f'fit_results_P(k)+_Boera/fit_redshift/redshift_{z_indx}'


mcmc_dir = root_dir + 'fit_mcmc/'
input_dir = mcmc_dir + f'{data_name}/' 
output_dir = input_dir + 'observable_samples/'
create_directory( output_dir )


load_global_properties = False

# sim_ids = range(10)
sim_ids = None
SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
SG.Load_Grid_Analysis_Data( sim_ids=sim_ids, load_pd_fit=True, mcmc_fit_dir='fit_mcmc_delta_0_1.0', load_thermal=load_global_properties)
params = SG.parameters

kmax = 0.2
ps_range = SG.Get_Power_Spectrum_Range( kmax=kmax )
sim_ids = SG.sim_ids

z_vals = [ 4.2, 4.6, 5.0   ]
fields_to_sample = ['P(k)', 'T0', 'gamma', 'tau', 'tau_HeII', ]
if load_global_properties: fields_to_sample.append( 'z_ion_H' )
data_grid, data_grid_power_spectrum = Get_Data_Grid_Composite(  fields_to_sample, SG, z_vals=z_vals, sim_ids=sim_ids, load_uvb_rates=False )


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


Write_Pickle_Directory( params, output_dir + 'params.pkl' )
Write_Pickle_Directory( stats, output_dir + 'fit_mcmc.pkl' )
Write_Pickle_Directory( param_samples, output_dir + 'samples_mcmc.pkl' )

# Get the Highest_Likelihood parameter values 
params_HL = Get_Highest_Likelihood_Params( param_samples, n_bins=100 )

hpi_sum = 0.95
n_samples = 400000 

# Obtain distribution of the power spectrum
file_name = output_dir + 'samples_power_spectrum.pkl'
samples_ps = Sample_Power_Spectrum_from_Trace( param_samples, data_grid_power_spectrum, SG, hpi_sum=hpi_sum, n_samples=n_samples, params_HL=params_HL, output_trace=True )
Write_Pickle_Directory( samples_ps, file_name )

# Obtain distribution of the other fields
file_name = output_dir + 'samples_fields.pkl' 
field_list = ['T0', 'gamma', 'tau', 'tau_HeII']
if load_global_properties: fields_list.append( 'z_ion_H' )
samples_fields = Sample_Fields_from_Trace( field_list, param_samples, data_grid, SG, hpi_sum=hpi_sum, n_samples=n_samples, params_HL=params_HL, output_trace=True)
Write_Pickle_Directory( samples_fields, file_name )



