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
from mcmc_sampling_functions import Get_Highest_Likelihood_Params, Get_1D_Likelihood_max, Get_Params_mean,Sample_Fields_from_Trace, Sample_Power_Spectrum_from_Trace


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

independent_redshift = True

# Directories 
ps_data_dir = base_dir + '/lya_statistics/data/'

# data_name = 'fit_results_P(k)+_BoeraC'
# data_name = 'fit_results_P(k)+_Boera'
# data_name = 'fit_results_P(k)+_Viel'
# data_name = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera_NOT_CORRECTED'
# data_name = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera_systematic'
# data_name = 'fit_results_P(k)+_Boera_sigma'
data_name = 'fit_results_P(k)+_Boera_covmatrix'

if independent_redshift: data_name += f'/fit_redshift/redshift_{z_indx}'
mcmc_dir = root_dir + 'fit_mcmc/'
input_dir = mcmc_dir + f'{data_name}/' 
output_dir = input_dir + 'observable_samples/'
create_directory( output_dir )


load_global_properties = False

# correction_file_name = ps_data_dir + 'FPS_resolution_correction_1024_50Mpc.pkl'
# FPS_resolution_correction = Load_Pickle_Directory( correction_file_name ) 
FPS_resolution_correction = None

use_inv_wdm = True
# Change wdm_mass to inv_wdm_mass
if use_inv_wdm: Grid_Parameters = Invert_wdm_masses( Grid_Parameters )

#Load custom power spectrum measurement
custom_ps_data = { 'root_dir': root_dir + 'flux_power_spectrum', 'file_base_name':'flux_ps_sampled_boera_extended', 'stats_base_name':None }
custom_data = { 'P(k)': custom_ps_data } 

# sim_ids = range(10)
sim_ids = None
files_to_load = range( 36 )
SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
SG.Load_Grid_Analysis_Data( sim_ids=sim_ids, load_pd_fit=True, mcmc_fit_dir='fit_mcmc_delta_0_1.0', FPS_correction=FPS_resolution_correction, load_thermal=load_global_properties, files_to_load=files_to_load, custom_data=custom_data )
params = SG.parameters

kmax = 0.2
ps_range = SG.Get_Power_Spectrum_Range( kmax=kmax )
sim_ids = SG.sim_ids

# z_vals = [ 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4,  4.6, 5.0   ]
# z_vals = [ 4.2, 4.6, 5.0, 5.4   ]
z_vals = [ 4.2, 4.6, 5.0  ]
z_fields_min = 4.0

fields_to_sample = ['P(k)', 'T0', 'gamma', 'tau', 'tau_HeII', ]
if load_global_properties: fields_to_sample.append( 'z_ion_H' )
data_grid, data_grid_power_spectrum = Get_Data_Grid_Composite(  fields_to_sample, SG, z_vals=z_vals, z_fields_min=z_fields_min, sim_ids=sim_ids, load_uvb_rates=False  )


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
# params_HL = Get_Highest_Likelihood_Params( param_samples, n_bins=10 )
params_max = Get_1D_Likelihood_max( param_samples, n_bins_1D=100 )
params_mean = Get_Params_mean( param_samples )

# Get the Highest_Likelihood parameter values 
n_bins = 10
params_HL = Get_Highest_Likelihood_Params( param_samples, n_bins=n_bins )

params_HL = { 'Highest_Likelihood':params_HL, 'max':params_max, 'mean':params_mean }
if use_mpi: comm.Barrier()
print( f'Rank: {rank}  HL:{params_HL} ' )


hpi_sum = 0.95
n_samples = None
# n_samples = 4500000 // 10

# Obtain distribution of the power spectrum
file_name = output_dir + 'samples_power_spectrum.pkl'
if FPS_resolution_correction is not None: file_name = output_dir + 'samples_power_spectrum_corrected.pkl'
samples_ps = Sample_Power_Spectrum_from_Trace( param_samples, data_grid_power_spectrum, SG, hpi_sum=hpi_sum, n_samples=n_samples, params_HL=params_HL, output_trace=True )
Write_Pickle_Directory( samples_ps, file_name )

# Obtain distribution of the other fields
file_name = output_dir + 'samples_fields.pkl' 
# field_list = ['T0', 'gamma', 'tau', 'tau_HeII']
field_list = ['T0', 'tau']
if load_global_properties: fields_list.append( 'z_ion_H' )
samples_fields = Sample_Fields_from_Trace( field_list, param_samples, data_grid, SG, hpi_sum=hpi_sum, n_samples=n_samples, params_HL=params_HL, output_trace=True)
Write_Pickle_Directory( samples_fields, file_name )



