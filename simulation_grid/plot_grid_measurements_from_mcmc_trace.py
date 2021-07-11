import sys, os
import numpy as np
import h5py as h5
import pickle
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from plot_optical_depth import Plot_tau_HI

data_dir = '/raid/bruno/data/'
grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
mcmc_dir = grid_dir + 'fit_mcmc/'
output_dir = mcmc_dir + f'observable_figures/'
create_directory( output_dir )

data_boss = 'fit_results_P(k)+tau_HeII_Boss'
data_boss_irsic = 'fit_results_P(k)+tau_HeII_Boss_Irsic'
data_boss_boera = 'fit_results_P(k)+tau_HeII_Boss_Boera'
data_boss_irsic_boera = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera'
data_boss_irsic_boera_tau = 'fit_results_P(k)+tau_HeII+tau_Boss_Irsic_Boera'

data_sets = [ data_boss_irsic_boera ]
data_labels = [ r'$P(k)\,+\, \mathrm{HeII} \tau_{eff}$' ]

samples_all = {}
samples_all['param'] = {}
samples_all['P(k)'] = {}
field_list = ['T0', 'gamma', 'tau', 'tau_HeII']
for field in field_list:
  samples_all[field] = {}
  

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
   
  # Obtain distribution of the power spectrum
  file_name = input_dir + 'samples_power_spectrum.pkl'
  samples_ps = Load_Pickle_Directory( file_name )
  
  # Obtain distribution of the other fields
  file_name = input_dir + 'samples_fields.pkl'
  samples_fields = Load_Pickle_Directory( file_name )
  
  samples_all['P(k)'][data_id] = samples_ps
  for field in field_list:
    samples_all[field][data_id] = samples_fields[field] 

# corner_labels = { 'scale_He':r'$\beta_{\mathrm{He}}$', 'scale_H':r'$\beta_{\mathrm{H}}$', 'deltaZ_He':r'$\Delta z_{\mathrm{He}}$', 'deltaZ_H':r'$\Delta z_{\mathrm{H}}$'    }
# Plot_Corner( samples_all['param'], data_labels, corner_labels, output_dir, n_bins_1D=40, n_bins_2D=40, lower_mask_factor=500, multiple=True, show_label=True  )

Plot_tau_HI(  samples_all['tau'], output_dir, system=system, labels=data_labels  )
