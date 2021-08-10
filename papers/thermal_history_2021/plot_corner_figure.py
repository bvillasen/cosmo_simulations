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
output_dir = data_dir + 'cosmo_sims/figures/nature/'

create_directory( output_dir )

data_boss_irsic_boera = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera'


data_sets = [ data_boss_irsic_boera ]
data_labels = [ '' ]

samples_all = {}
samples_all['param'] = {}


for data_id, data_name in enumerate(data_sets):
  
  print(f'Loading Dataset: {data_name}' )
  input_dir = mcmc_dir + f'{data_name}/observable_samples/' 
  stats_file = input_dir + 'fit_mcmc.pkl'
  samples_file = input_dir + 'samples_mcmc.pkl'

  params = Load_Pickle_Directory( input_dir + 'params.pkl' )
  print( f'Loading File: {samples_file}')
  param_samples = pickle.load( open( samples_file, 'rb' ) )
  samples_all['param'][data_id] = param_samples
  
  # Get the Highest_Likelihood parameter values 
  params_HL = Get_Highest_Likelihood_Params( param_samples, n_bins=100 )
  
  stats = pickle.load( open( stats_file, 'rb' ) )
  # for p_id in params.keys():
  #   p_name = params[p_id]['name']
  #   p_stats = stats[p_name]
  #   params[p_id]['mean'] = p_stats['mean']
  #   params[p_id]['sigma'] = p_stats['standard deviation']


corner_labels = { 'scale_He':r'$\beta_{\mathrm{He}}$', 'scale_H':r'$\beta_{\mathrm{H}}$', 'deltaZ_He':r'$\Delta z_{\mathrm{He}}$', 'deltaZ_H':r'$\Delta z_{\mathrm{H}}$'    }

ticks = {0:[0.32, 0.40, 0.48, 0.56, 0.64], 1:[0.76, 0.77, 0.78, 0.79], 2:[0.12, 0.18, 0.24, 0.30, 0.36], 3:[-0.04, 0.00, 0.04, 0.08, 0.12]}
Plot_Corner( samples_all['param'], data_labels, corner_labels, output_dir, n_bins_1D=40, n_bins_2D=40, lower_mask_factor=500, multiple=True, show_label=True, HL_vals=params_HL, ticks=ticks  )
