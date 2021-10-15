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
output_dir = data_dir + f'cosmo_sims/figures/paper_thermal_history/'
create_directory( output_dir )
root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
mcmc_dir = root_dir + 'fit_mcmc/'

data_boss_irsic_boera = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera'
data_boss_irsic_boera_NC = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera_NOT_CORRECTED'
data_sets = [ data_boss_irsic_boera, data_boss_irsic_boera_NC ]
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


factor = 1.08
samples_rescaled = {}
for z_id in samples_ps.keys():
  if z_id == 'z_vals': 
    samples_rescaled['z_vals'] = samples_ps['z_vals']
    continue
  data_snap = samples_ps[z_id]
  samples_rescaled[z_id] = {}
  samples_rescaled[z_id]['k_vals'] = data_snap['k_vals'] 
  samples_rescaled[z_id]['Highest_Likelihood'] = data_snap['Highest_Likelihood'] *factor 


ps_samples = samples_all['P(k)']
ps_samples[1] = samples_rescaled

ps_samples[0]['line_color'] = 'k'
ps_samples[1]['line_color'] = 'C0'
ps_samples[1]['ls'] = '--'

data_labels = [ 'This Work (Best-Fit)', r'Modified to Match HI $\tau_{\mathrm{eff}}$' ]
Plot_Power_Spectrum_Grid( output_dir, ps_samples=ps_samples, data_labels=data_labels, scales='small_z5', ps_data_dir=ps_data_dir, show_middle=False )

