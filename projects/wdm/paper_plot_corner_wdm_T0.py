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

data_name = 'fit_results_P(k)+_Boera_covmatrix'
data_names = [ 'fit_results_P(k)+T0_Boera_covmatrix'  ]
data_labels = [ r'$P\,(k) \, + \, T_0$ constraint',  ]


proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + f'figures/paper_revision/'
create_directory( output_dir )

samples_all = {}
samples_all['param'] = {}
for data_id,data_name in enumerate(data_names):
   
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
  # low = p_stats['quantiles'][2.5]
  # high = p_stats['quantiles'][97.5]
  low, high = p_stats['95% HPD interval']
  delta_l = val - low
  delta_h = high - val
  param_values[p_name]['value'] = val
  param_values[p_name]['delta_h'] = delta_h
  param_values[p_name]['delta_l'] = delta_l

corner_labels = { 'inv_wdm_mass':r'$m_{\mathregular{WDM}}^{\mathregular{-1}} \,\,\, \mathregular{[keV^{-1}]}$', 'scale_H_ion': r'$\beta$',
                  'scale_H_Eheat': r'$\alpha_{\mathrm{E}}$', 'deltaZ_H':r'$\Delta z$' }

param_labels = { 'inv_wdm_mass':r'$m_{\mathregular{WDM}}^{\mathregular{-1}}$', 'scale_H_ion': r'$\beta$',
                  'scale_H_Eheat': r'$\alpha_{\mathrm{E}}$', 'deltaZ_H':r'$\Delta z$' }

ticks = { 0:[0., 0.1, 0.2, 0.3, 0.4], 1:[0.4, 0.6, 0.8, 1.0, 1.2, 01.4], 2:[ 0.6, 0.8, 1.0, 1.2,], 3:[ -0.5, -0.25, 0, 0.25, 0.5,] }
limits = {0:( 0, 0.45 ), 1:( 0.8, 1.5 ), 2:( 0.4, 1.15 ), 3:( -0.5, 0.5 )}

data_names = [ 'fit_results_P(k)+_Boera_covmatrix' ]
samples_outline = {}
samples_outline['param'] = {}
for data_id,data_name in enumerate(data_names):
   
  root_dir = data_dir + f'cosmo_sims/sim_grid/{grid_name}/'
  mcmc_dir = root_dir + 'fit_mcmc/'

  print(f'Loading Dataset: {data_name}' )
  input_dir = mcmc_dir + f'{data_name}/' 
  stats_file = input_dir + 'fit_mcmc.pkl'
  samples_file = input_dir + 'samples_mcmc.pkl'

  print( f'Loading File: {samples_file}')
  param_samples = pickle.load( open( samples_file, 'rb' ) )
  samples_outline['param'][data_id] = param_samples
  
oslo = palettable.scientific.sequential.Oslo_20_r
tempo = palettable.cmocean.sequential.Tempo_20
amp = palettable.cmocean.sequential.Amp_20
devon = palettable.scientific.sequential.Devon_20_r
davos = palettable.scientific.sequential.Davos_20_r  

samples_outline_cmap = oslo
samples_outline_color = samples_outline_cmap.mpl_colors[len(samples_outline_cmap.mpl_colors)//2] 


cmap = amp
ymax = [0.18, 0.26, 0.24, 0.09]
outline_label = r'$P\,(k)$ constraint'

Plot_Corner( samples_all['param'], data_labels, corner_labels, output_dir, n_bins_1D=20, n_bins_2D=50, 
             lower_mask_factor=1e2, multiple=True, show_label=True, HL_vals=params_HL, ticks=ticks, 
             limits=limits, param_values=param_values, black_background=False, figure_name='corner_wdm_T0.png', 
             param_names=p_names, param_labels=param_labels, cmap=cmap, line_color_index=10, 
             samples_outline=samples_outline['param'], samples_outline_color=samples_outline_color, outline_label=outline_label,
             legend_ncol=1, ymax=ymax )
