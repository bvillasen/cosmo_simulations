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

grid_name = '1024_wdmgrid_cdm_extended_beta'
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
  samples_all['param'][data_id] = param_samples

  # # Get the Highest_Likelihood parameter values 
  params_HL = Get_Highest_Likelihood_Params( param_samples, n_bins=20 )
  # params_HL = None
  
  # params_HL[2] = 0.80

  stats = pickle.load( open( stats_file, 'rb' ) )

# 
# corner_labels = { 'scale_He':r'$\beta_{\mathrm{He}}$', 'scale_H':r'$\beta_{\mathrm{H}}$', 'deltaZ_He':r'$\Delta z_{\mathrm{He}}$', 'deltaZ_H':r'$\Delta z_{\mathrm{H}}$',
#                   'scale_H_ion': r'$\beta_{\mathrm{H}}^{\mathrm{ion}}$', 'scale_He_ion': r'$\beta_{\mathrm{He}}^{\mathrm{ion}}$', 'scale_He_Eheat': r'$\alpha E_{\mathrm{He}}$', 'scale_H_Eheat': r'$\alpha E_{\mathrm{H}}$',
#                   'wdm_mass':r'$m_{\mathrm{WDM}}$  [keV]', 'inv_wdm_mass':r'$m_{\mathrm{WDM}}^{-1}$  [keV$^{-1}$]'       }
# 

corner_labels = { 'inv_wdm_mass':r'$m_{\mathrm{WDM}}^{-1}$  [keV$^{-1}$]', 'scale_H_ion': r'$\beta$',
                  'scale_H_Eheat': r'$\alpha_{\mathrm{E}}$', 'deltaZ_H':r'$\Delta z$' }

ticks = { 0:[ 0.8, 0.9,  1.0, 1.1,   ], 1:[  0.8, 0.9, 1.0,1.1, 1.2,], 2:[ -0.5, -0.25, 0, 0.25, 0.5,]}
limits = { 0:( 0.85, 1.2 ), 1:( 0.7, 1.25 ), 2:( -0.5, 0.5 )}

Plot_Corner( samples_all['param'], data_labels, corner_labels, output_dir, n_bins_1D=40, n_bins_2D=40, 
             lower_mask_factor=500, multiple=True, show_label=True, HL_vals=params_HL, ticks=ticks, 
             limits=limits, param_values=None, black_background=False, figure_name='corner_cdm_extended_beta.png', show_param_values=False)
