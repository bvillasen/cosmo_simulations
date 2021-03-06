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

grid_name = '1024_wdmgrid_extended_beta'
grid_names = [ grid_name ]

data_name = 'fit_results_P(k)+_Boera_covmatrix'
data_labels = [ '' ]

output_dir = data_dir + f'figures/wdm/'
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
  
  # Select CDM from the chain
  chain_inv_wdm_mass = param_samples[0]['trace']
  indices = chain_inv_wdm_mass <= 0.05
  n_selected = indices.sum()
  print( f'Selected CDM samples: {n_selected}')
  
  chain_selected = {} 
  for p_id in range(3):
    chain_selected[p_id] = { 'name':param_samples[p_id+1]['name'], 'trace':param_samples[p_id+1]['trace'][indices] }
  
  samples_all['param'][data_id] = chain_selected

  # # Get the Highest_Likelihood parameter values 
  params_HL_0 = Get_Highest_Likelihood_Params( param_samples, n_bins=20 )
  params_HL = Get_Highest_Likelihood_Params( chain_selected, n_bins=20 )
  

  stats = pickle.load( open( stats_file, 'rb' ) )


corner_labels = { 'inv_wdm_mass':r'$m_{\mathrm{WDM}}^{-1}$  [keV$^{-1}$]', 'scale_H_ion': r'$\beta$',
                  'scale_H_Eheat': r'$\alpha_{\mathrm{E}}$', 'deltaZ_H':r'$\Delta z$' }

ticks = {0:[0.4, 0.6, 0.8, 1.0, 1.2, 01.4], 1:[ 0.6, 0.8, 1.0, 1.2,], 2:[ -0.5, -0.25, 0, 0.25, 0.5,]}
limits = { 0:( 0.85, 1.3 ), 1:( 0.7, 1.25 ), 2:( -0.5, 0.5 )}

Plot_Corner( samples_all['param'], data_labels, corner_labels, output_dir, n_bins_1D=20, n_bins_2D=25, 
             lower_mask_factor=500, multiple=True, show_label=True, HL_vals=params_HL, ticks=ticks, 
             limits=limits, param_values=None, black_background=False, figure_name='corner_cdm_slice_extended_beta.png', show_param_values=False)
