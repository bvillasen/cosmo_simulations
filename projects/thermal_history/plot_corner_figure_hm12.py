import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from plot_mcmc_corner import Plot_Corner
from mcmc_sampling_functions import Get_Highest_Likelihood_Params

ps_data_dir = 'lya_statistics/data/'
 
root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
mcmc_dir = root_dir + 'fit_mcmc/'
output_dir = data_dir + f'figures/thermal_history/paper/'
create_directory( output_dir )

data_boss_irsic_boera = 'fit_results_covariance_systematic'


data_sets = [ data_boss_irsic_boera ]
data_labels = [ '' ]

samples_all = {}
samples_all['param'] = {}


for data_id, data_name in enumerate(data_sets):
  
  print(f'Loading Dataset: {data_name}' )
  input_dir = mcmc_dir + f'{data_name}/' 
  stats_file = input_dir + 'fit_mcmc.pkl'
  samples_file = input_dir + 'samples_mcmc.pkl'

  params = Load_Pickle_Directory( input_dir + 'observable_samples/params.pkl' )
  print( f'Loading File: {samples_file}')
  param_samples = pickle.load( open( samples_file, 'rb' ) )
  samples_all['param'][data_id] = param_samples
  
  # Get the Highest_Likelihood parameter values 
  params_HL = Get_Highest_Likelihood_Params( param_samples, n_bins=30 )
  
  stats = pickle.load( open( stats_file, 'rb' ) )
  # for p_id in params.keys():
  #   p_name = params[p_id]['name']
  #   p_stats = stats[p_name]
  #   params[p_id]['mean'] = p_stats['mean']
  #   params[p_id]['sigma'] = p_stats['standard deviation']


corner_labels = { 'scale_He':r'$\beta_{\mathrm{He}}$', 'scale_H':r'$\beta_{\mathrm{H}}$', 'deltaZ_He':r'$\Delta z_{\mathrm{He}}$', 'deltaZ_H':r'$\Delta z_{\mathrm{H}}$'    }

p_names = [ 'scale_He', 'scale_H', 'deltaZ_He', 'deltaZ_H' ]

param_values = {}
for p_id, p_name in enumerate(p_names):
  param_values[p_name] = {}
  val = params_HL[p_id]
  p_stats = stats[p_name]
  low = p_stats['quantiles'][2.5]
  high = p_stats['quantiles'][97.5]
  delta_l = val - low
  delta_h = high - val
  param_values[p_name]['value'] = val
  param_values[p_name]['delta_h'] = delta_h
  param_values[p_name]['delta_l'] = delta_l
  
ticks = {0:[0.3, 0.40, 0.5,  0.6], 1:[0.75, 0.8,  0.85, 0.9], 2:[ .1, 0.2, 0.3, 0.4, ], 3:[ -0.4, -0.2, 0.0, 0.20]}
# ticks = None

limits = {0:( 0.26, 0.69 ), 1:( 0.75, 0.9 ), 2:( 0.05, 0.45 ), 3:( -0.5, 0.21 )}
Plot_Corner( samples_all['param'], data_labels, corner_labels, output_dir, n_bins_1D=40, n_bins_2D=40, lower_mask_factor=500, multiple=True, show_label=True, HL_vals=params_HL, ticks=ticks, limits=limits, param_values=param_values, black_background=False)
