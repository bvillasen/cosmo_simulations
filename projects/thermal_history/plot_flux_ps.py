import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
base_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from mcmc_sampling_functions import Get_Highest_Likelihood_Params
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid, Plot_Power_Spectrum_Grid_diff
from colors import *

black_background = False

ps_data_dir =  base_dir + 'lya_statistics/data/'
proj_dir = data_dir + 'projects/thermal_history/'
output_dir = proj_dir + f'figures/'
if black_background: output_dir += 'black_background/'
create_directory( output_dir )
root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
mcmc_dir = root_dir + 'fit_mcmc/'

# data_boss_irsic_boera_NC = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera_NOT_CORRECTED'
# data_sets = [ data_boss_irsic_boera, data_boss_irsic_boera_NC ]

# data_boss_irsic_boera = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera_systematic'
data_boss_irsic_boera = 'fit_results_covariance_systematic'
data_sets = [ data_boss_irsic_boera ]

samples_all = {}
samples_all['param'] = {}
samples_all['P(k)'] = {}


for data_id, data_name in enumerate(data_sets):
  
  print(f'Loading Dataset: {data_name}' )
  input_dir = mcmc_dir + f'{data_name}/observable_samples/' 
  stats_file = input_dir + 'fit_mcmc.pkl'
  samples_file = input_dir + 'samples_mcmc.pkl'

  params = Load_Pickle_Directory( input_dir + 'params.pkl' )

  print( f'Loading File: {stats_file}')
  stats = pickle.load( open( stats_file, 'rb' ) )
  for p_id in params.keys():
    p_name = params[p_id]['name']
    p_stats = stats[p_name]
    params[p_id]['mean'] = p_stats['mean']
    params[p_id]['sigma'] = p_stats['standard deviation']
  print( f'Loading File: {samples_file}')
  param_samples = pickle.load( open( samples_file, 'rb' ) )
  samples_all['param'][data_id] = param_samples

  # Get the Highest_Likelihood parameter values 
  params_HL = Get_Highest_Likelihood_Params( param_samples, n_bins=100 )
  # 
  # Obtain distribution of the power spectrum
  file_name = input_dir + 'samples_power_spectrum.pkl'
  samples_ps = Load_Pickle_Directory( file_name )  
  samples_ps['z_vals'] = np.array([ samples_ps[i]['z'] for i in samples_ps ])
  samples_all['P(k)'][data_id] = samples_ps
  
ps_samples = samples_all['P(k)']


# Apply resolution correction
correction_file_name = ps_data_dir + 'FPS_resolution_correction_1024_50Mpc.pkl'
FPS_correction = Load_Pickle_Directory( correction_file_name ) 
corr_z_vals = FPS_correction['z_vals']


n_snapshots = 14
for z_id in range(n_snapshots):
  ps_data = ps_samples[0][z_id]
  z = ps_data['z']
  k_vals = ps_data['k_vals']
  ps_mean = ps_data['Highest_Likelihood']
  ps_h = ps_data['higher']
  ps_l = ps_data['lower']
  z_diff = np.abs( corr_z_vals - z )
  if z_diff.min() > 5e-2: 
    print( f'Large redshift diference: {z_diff.min()}')
    continue  
  z_indx = np.where( z_diff == z_diff.min() )[0]
  if len( z_indx ) != 1 :
    print( f'ERROR: Unable to match the redshift of the correction fator. {z} -> {correction_z_vals[z_indx]}  ')
    exit(-1)
  z_indx = z_indx[0]
  correction = FPS_correction[z_indx]
  correction_k_vals = correction['k_vals']
  correction_ps_factor = correction['delta_factor']
  indices = correction_ps_factor > 1
  new =  correction_ps_factor[indices] - 1
  correction_ps_factor[indices] = 1 + new * 1
  k_diff = np.abs( k_vals - correction_k_vals )
  print( f'{z} {correction_ps_factor}')
  if k_diff.sum() > 1e-6:
     print(f'ERROR: Large k difference for FPS correction: {k_diff.sum()}.')
     exit(-1)
  ps_mean = ps_mean / correction_ps_factor
  ps_h = ps_h / correction_ps_factor
  ps_l = ps_l / correction_ps_factor
  ps_data['Highest_Likelihood'] = ps_mean
  ps_data['higher'] = ps_h
  ps_data['lower'] = ps_l
  
  
  
  # 
  # 

color = 'k'
if black_background: color = purples[1]

ps_samples[0]['line_color'] = color
# ps_samples[1]['line_color'] = 'C1'

data_labels = [ 'This Work', 'Original' ]
# Plot_Power_Spectrum_Grid( output_dir, ps_samples=ps_samples, data_labels=data_labels, scales='large', ps_data_dir=ps_data_dir, show_middle=True )
# Plot_Power_Spectrum_Grid( output_dir, ps_samples=ps_samples, data_labels=data_labels, scales='large_small', ps_data_dir=ps_data_dir, show_middle=True )
Plot_Power_Spectrum_Grid_diff( output_dir, ps_samples=ps_samples, data_labels=data_labels, 
                          scales='all_and_z2', ps_data_dir=ps_data_dir, show_middle=False, 
                          black_background=black_background,)

