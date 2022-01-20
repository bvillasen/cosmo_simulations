import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from plot_mcmc_corner import Plot_Corner
# from mcmc_sampling_functions import Get_Highest_Likelihood_Params

grid_name = '1024_wdmgrid_nsim600'

# fit_names = [ 'fit_results_P(k)+_Boera', 'fit_results_P(k)+_Boera_covMatrix_zeros', 'fit_results_P(k)+_Boera_covMatrix'  ]
# data_labels = [ r'Sigma', r'Diagonal Matrix', r'Covariance Matirx' ]

# fit_names = [ 'fit_results_P(k)+_Boera_covMatrix'  ]
# data_labels = [ 'Covariance Matirx' ]



# fit_names = [ 'fit_results_P(k)+_Boera', 'fit_results_P(k)+_Boera_covMatrix_zeros', 'fit_results_P(k)+_Boera_covMatrix'  ]
# data_labels = [ r'Sigma', r'Diagonal Matrix', r'Covariance Matirx' ]

# fit_names = [ 'fit_results_P(k)+_Boera_covMatrix'  ]
# data_labels = [ 'Covariance Matirx' ]\

# sigma_fractions = [ 1.0, 0.5, 0.1 ]
# # fit_names = [ f'fit_results_P(k)+_Simulated_covMatrix_sigma{sigma_fraction}' for sigma_fraction in sigma_fractions ]
# data_labels = [ r'$x \sigma = {0}$'.format(sigma_fraction) for sigma_fraction in sigma_fractions ]
# 
# fit_names = [ f'fit_results_P(k)+_Simulated_sigma{sigma_fraction}' for sigma_fraction in sigma_fractions ]
# data_labels = [ r'$x \sigma = {0}$'.format(sigma_fraction) for sigma_fraction in sigma_fractions ]


sigma_fraction = 0.1
fit_names = [ f'fit_results_P(k)+_Simulated_sigma{sigma_fraction}', f'fit_results_P(k)+_Simulated_covMatrix_sigma{sigma_fraction}'  ]
data_labels = [ 'Sigma', 'Cov Matrix']


output_dir = data_dir + f'cosmo_sims/sim_grid/1024_wdmgrid_nsim600/figures/'
create_directory( output_dir )

samples_all = {}
samples_all['param'] = {}
for data_id, fit_name in enumerate(fit_names):
   
  root_dir = data_dir + f'cosmo_sims/sim_grid/{grid_name}/'
  mcmc_dir = root_dir + 'fit_mcmc/'

  print(f'Loading Dataset: {fit_name}' )
  input_dir = mcmc_dir + f'{fit_name}/' 
  stats_file = input_dir + 'fit_mcmc.pkl'
  samples_file = input_dir + 'samples_mcmc.pkl'

  print( f'Loading File: {samples_file}')
  param_samples = pickle.load( open( samples_file, 'rb' ) )
  samples_all['param'][data_id] = param_samples

  # # Get the Highest_Likelihood parameter values 
  # params_HL = Get_Highest_Likelihood_Params( param_samples, n_bins=30 )
  params_HL = None

  stats = pickle.load( open( stats_file, 'rb' ) )


corner_labels = { 'scale_He':r'$\beta_{\mathrm{He}}$', 'scale_H':r'$\beta_{\mathrm{H}}$', 'deltaZ_He':r'$\Delta z_{\mathrm{He}}$', 'deltaZ_H':r'$\Delta z_{\mathrm{H}}$',
                  'scale_H_ion': r'$\beta_{\mathrm{H}}^{\mathrm{ion}}$', 'scale_He_ion': r'$\beta_{\mathrm{He}}^{\mathrm{ion}}$', 'scale_He_Eheat': r'$\alpha E_{\mathrm{He}}$', 'scale_H_Eheat': r'$\alpha E_{\mathrm{H}}$',
                  'wdm_mass':r'$m_{\mathrm{WDM}}$  [keV]', 'inv_wdm_mass':r'$m_{\mathrm{WDM}}^{-1}$  [keV$^{-1}$]'       }

ticks = {0:[0., 0.1, 0.2, 0.3, 0.4], 1:[0.4, 0.6, 0.8, 1.0, 1.2, 01.4], 2:[ 0.6, 0.8, 1.0, 1.2, 1.4 ], 3:[ -0.4,-0.2, 0, 0.2, 0.4]}
# ticks = None

limits = {0:( 0, 0.45 ), 1:( 0.8, 1.5 ), 2:( 0.4, 1.4 ), 3:( -0.5, 0.5 )}
Plot_Corner( samples_all['param'], data_labels, corner_labels, output_dir, n_bins_1D=40, n_bins_2D=40, lower_mask_factor=500, multiple=True, show_label=True, HL_vals=params_HL, ticks=ticks, limits=limits, param_values=None, black_background=False)
