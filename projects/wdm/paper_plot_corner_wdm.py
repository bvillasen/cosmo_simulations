import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from colors import *
from plot_mcmc_corner import Plot_Corner
from mcmc_sampling_functions import Get_Highest_Likelihood_Params

grid_name = '1024_wdmgrid_extended_beta'
grid_names = [ grid_name ]

data_name = 'fit_results_P(k)+_Boera_covmatrix'
data_labels = [ '' ]


proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + f'figures/'
create_directory( output_dir )

samples_all = {}
samples_all['param'] = {}
for data_id,grid_name in enumerate(grid_names):
   
  root_dir = data_dir + f'cosmo_sims/sim_grid/{grid_name}/'
  mcmc_dir = root_dir + 'fit_mcmc/'

  print(f'Loading Dataset: {data_name}' )
  input_dir = mcmc_dir + f'{data_name}/' 
  stats_file = input_dir + 'fit_mcmc.pkl'
  samples_file = input_dir + 'samples_mcmc.pkl'

  print( f'Loading File: {samples_file}')
  param_samples = pickle.load( open( samples_file, 'rb' ) )
  samples_all['param'][data_id] = param_samples

  # # Get the Highest_Likelihood parameter values 
  params_HL = Get_Highest_Likelihood_Params( param_samples, n_bins=30 )
  # params_HL = None
  
  # params_HL[2] = 0.78

  stats = pickle.load( open( stats_file, 'rb' ) )

p_names = [ 'inv_wdm_mass', 'scale_H_ion', 'scale_H_Eheat', 'deltaZ_H' ]

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

corner_labels = { 'inv_wdm_mass':r'$m_{\mathregular{WDM}}^{\mathregular{-1}} \,\,\, \mathregular{[keV^{-1}]}$', 'scale_H_ion': r'$\beta$',
                  'scale_H_Eheat': r'$\alpha_{\mathrm{E}}$', 'deltaZ_H':r'$\Delta z$' }

param_labels = { 'inv_wdm_mass':r'$m_{\mathregular{WDM}}^{\mathregular{-1}}$', 'scale_H_ion': r'$\beta$',
                  'scale_H_Eheat': r'$\alpha_{\mathrm{E}}$', 'deltaZ_H':r'$\Delta z$' }

ticks = {0:[0., 0.1, 0.2, 0.3, 0.4], 1:[0.4, 0.6, 0.8, 1.0, 1.2, 01.4], 2:[ 0.6, 0.8, 1.0, 1.2,], 3:[ -0.5, -0.25, 0, 0.25, 0.5,]}
limits = {0:( 0, 0.45 ), 1:( 0.8, 1.5 ), 2:( 0.4, 1.15 ), 3:( -0.5, 0.5 )}

oslo = palettable.scientific.sequential.Oslo_20_r
tempo = palettable.cmocean.sequential.Tempo_20
devon = palettable.scientific.sequential.Devon_20_r


Plot_Corner( samples_all['param'], data_labels, corner_labels, output_dir, n_bins_1D=20, n_bins_2D=35, 
             lower_mask_factor=500, multiple=True, show_label=True, HL_vals=params_HL, ticks=ticks, 
             limits=limits, param_values=param_values, black_background=False, figure_name='corner_wdm.png', 
             param_names=p_names, param_labels=param_labels, cmap=oslo )
