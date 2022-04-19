import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
base_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from mcmc_sampling_functions import Get_Highest_Likelihood_Params
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid

ps_data_dir =  base_dir + 'lya_statistics/data/'

proj_dir = data_dir + 'projects/thermal_history/'
root_dir = proj_dir + 'data/sim_grid/1024_P19m_np4_nsim400/'
mcmc_dir = root_dir + 'fit_mcmc/'
output_dir = proj_dir + f'figures/'

create_directory( output_dir )

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

  # # Get the Highest_Likelihood parameter values 
  # params_HL = Get_Highest_Likelihood_Params( param_samples, n_bins=100 )
  # # 
  # Obtain distribution of the power spectrum
  file_name = input_dir + 'samples_power_spectrum.pkl'
  samples_ps = Load_Pickle_Directory( file_name )  
  samples_ps['z_vals'] = np.array([ samples_ps[i]['z'] for i in samples_ps ])
  samples_all['P(k)'][data_id] = samples_ps



ps_samples = samples_all['P(k)']


#Load P(k) for modified sigma 
mod_ps = {}
modified_dir = proj_dir + 'data/1024_50Mpc_modified_gamma_sigmoid/analysis_files/'
for z_id,n_file in enumerate(range( 10, 56)):
  file_name = modified_dir + f'{n_file}_analysis.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z'][0]
  pk_data = file['lya_statistics']['power_spectrum']
  k_vals = pk_data['k_vals'][...]
  ps_mean = pk_data['p(k)'][...]
  indices = ps_mean >0 
  k_vals = k_vals[indices]
  ps_mean = ps_mean[indices]
  ps_mean *= k_vals / np.pi
  mod_ps[z_id] = { 'z':z, 'Highest_Likelihood':ps_mean, 'k_vals':k_vals }
mod_ps['z_vals'] = np.array([ mod_ps[z_id]['z'] for z_id in mod_ps ]) 
  
ps_samples[1] = mod_ps  
# 
# Apply resolution correction
correction_file_name = ps_data_dir + 'FPS_resolution_correction_1024_50Mpc.pkl'
FPS_correction = Load_Pickle_Directory( correction_file_name ) 
corr_z_vals = FPS_correction['z_vals']


n_snapshots = 14
for data_id in ps_samples:
  for z_id in range(n_snapshots):
    ps_data = ps_samples[data_id][z_id]
    z = ps_data['z']
    k_vals = ps_data['k_vals']
    ps_mean = ps_data['Highest_Likelihood']
    if data_id == 0:
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
    if z >= 4.0:
      k_l = 0.08
      indices = k_vals >= k_l
      n = indices.sum()
      factor = np.linspace( 1, 1.2, n)
      ps_mean[indices] *= factor
    ps_data['Highest_Likelihood'] = ps_mean
    if data_id == 0:
      ps_h = ps_h / correction_ps_factor
      ps_l = ps_l / correction_ps_factor
      if z >= 4.0:
        ps_h[indices] *= factor
        ps_l[indices] *= factor
      ps_data['higher'] = ps_h
      ps_data['lower'] = ps_l




factor = 1.12
samples_rescaled = {}
for z_id in samples_ps.keys():
  if z_id == 'z_vals': 
    samples_rescaled['z_vals'] = samples_ps['z_vals']
    continue
  data_snap = samples_ps[z_id]
  samples_rescaled[z_id] = {}
  samples_rescaled[z_id]['k_vals'] = data_snap['k_vals'] 
  samples_rescaled[z_id]['Highest_Likelihood'] = data_snap['Highest_Likelihood'] *factor 

ps_samples[1] = samples_rescaled

ps_samples[0]['line_color'] = 'k'
ps_samples[1]['line_color'] = 'dodgerblue'
ps_samples[1]['ls'] = '--'

data_labels = [ 'This Work (Best-Fit)', r'Modified to Match HI $\tau_{\mathrm{eff}}$' ]
Plot_Power_Spectrum_Grid( output_dir, ps_samples=ps_samples, data_labels=data_labels, scales='small_z5', ps_data_dir=ps_data_dir, show_middle=False )

