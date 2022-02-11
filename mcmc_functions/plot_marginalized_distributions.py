import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
from scipy import interpolate as interp 
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from plot_mcmc_corner import Plot_Corner
# from mcmc_sampling_functions import Get_Highest_Likelihood_Params


grid_name = '1024_wdmgrid_nsim600'
root_dir = data_dir + f'cosmo_sims/sim_grid/{grid_name}/'
output_dir = data_dir + f'cosmo_sims/sim_grid/1024_wdmgrid_nsim600/figures/fit_covariance_matrix/'
create_directory( output_dir )


# selected_sim_ids = [ -1, -2,  168, 170, 171, 173, 183, 185, 186, 188, 318, 320, 321, 323, 333, 335, 336, 338]


selected_sim_ids = [ -1, -2, 22, 97, 172, 247, 322, 397, 472, 547]


mcmc_dir = root_dir + 'fit_mcmc/'

# fit_base_name = 'closest_to_best_fit/fit_results_P(k)+_Boera_covmatrix'
# figure_name = 'marginalized_closest_to_best_fit.png'

# fit_base_name = 'closest_to_best_fit_bootstrap/fit_results_P(k)+_Boera_covmatrix'
# figure_name = 'marginalized_closest_to_best_fit_bootstrap.png'

# fit_base_name = 'wdm_masses/fit_results_P(k)+_Boera_covmatrix'
# figure_name = 'marginalized_wdm_masses.png'
    
fit_base_name = 'wdm_masses_bootstrap/fit_results_P(k)+_Boera_covmatrix'
figure_name = 'marginalized_wdm_masses_bootstrap.png'
        

extra_name = None

samples_all = {}
samples_all['param'] = {}
for data_id, sim_id in enumerate(selected_sim_ids):
  
  if    sim_id == -1: fit_name = 'fit_results_P(k)+_Boera_sigma/' 
  elif  sim_id == -2: fit_name = 'fit_results_P(k)+_Boera_covmatrix/' 
  else: fit_name =  f'{fit_base_name}_covfromsim_{sim_id:03}/'
  
  print(f'Loading Dataset: {fit_name}' )
  input_dir = mcmc_dir + f'{fit_name}/'
  if extra_name is not None: input_dir += extra_name 
  stats_file = input_dir + 'fit_mcmc.pkl'
  samples_file = input_dir + 'samples_mcmc.pkl'
  
  print( f'Loading File: {samples_file}')
  param_samples = pickle.load( open( samples_file, 'rb' ) )
  samples_all['param'][data_id] = param_samples
  
  stats = pickle.load( open( stats_file, 'rb' ) )

limits = {0:( 0, 0.65 ), 1:( 0.8, 1.5 ), 2:( 0.4, 1.4 ), 3:( -0.5, 0.5 )}
ticks = {0:[0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], 1:[0.4, 0.6, 0.8, 1.0, 1.2, 01.4], 2:[ 0.6, 0.8, 1.0, 1.2, 1.4 ], 3:[ -0.4,-0.2, 0, 0.2, 0.4]}


param_labels = { 'scale_He':r'$\beta_{\mathrm{He}}$', 'scale_H':r'$\beta_{\mathrm{H}}$', 'deltaZ_He':r'$\Delta z_{\mathrm{He}}$', 'deltaZ_H':r'$\Delta z_{\mathrm{H}}$',
                  'scale_H_ion': r'$\beta_{\mathrm{H}}^{\mathrm{ion}}$', 'scale_He_ion': r'$\beta_{\mathrm{He}}^{\mathrm{ion}}$', 'scale_He_Eheat': r'$\alpha E_{\mathrm{He}}$', 'scale_H_Eheat': r'$\alpha E_{\mathrm{H}}$',
                  'wdm_mass':r'$m_{\mathrm{WDM}}$  [keV]', 'inv_wdm_mass':r'$m_{\mathrm{WDM}}^{-1}$  [keV$^{-1}$]'       }


n_param = 4

n_bins_1D = 40

fig_size = 5
label_size = 16
tick_label_size = 12
tick_length = 7
tick_width = 2
text_color = 'black'

space = 0.05
nrows, ncols = 1, n_param
line_width =  1.5
alpha = 0.5

fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_size*ncols,fig_size*nrows)  )
fig.subplots_adjust( wspace=space, hspace=space )


labels = [r'm=1.0 keV', r'm=2.0 keV', r'm=3.0 keV', r'm=4.0 keV', r'm=5.0 keV', r'm=6.0 keV', r'm=8.0 keV', 'CDM']


for data_id in samples_all['param']:
  # if data_id > 4: continue
  
  samples = samples_all['param'][data_id]
  
  for param_id in samples:
    
    if data_id in [ 0, 1 ]:
      lw = 2.0
      alpha = 1
    else:
      lw = 1.5
      alpha = 0.5
    
    label = labels[data_id-2]  
    if data_id == 0: label = 'Boera Sigma'
    if data_id == 1: label = 'Boera Cov M'
    
    
    
    param_name = samples[param_id]['name'] 
    param_trace = samples[param_id]['trace']
    hist, bin_edges = np.histogram( param_trace, bins=n_bins_1D ) 
    bin_centers = ( bin_edges[:-1] + bin_edges[1:] ) / 2.
    bin_width = bin_centers[0] - bin_centers[1]  
    bin_centers_interp = np.linspace( bin_centers[0], bin_centers[-1], 10000 )
    f_interp  = interp.interp1d( bin_centers, hist,  kind='cubic' )
    ax = ax_l[param_id]
    y = f_interp(bin_centers_interp)
    ax.plot( bin_centers_interp, y,  linewidth=lw, label=label, alpha=alpha  )
    
    

for i in samples:
  
  ax = ax_l[i]
  x_lims = limits[i]
  ax.set_xlim( x_lims[0], x_lims[1] )
  ax.set_xticks(ticks[i])
  ax.set_yticks([])
  ax.set_ylim(0, None)
  
  param_name = samples[i]['name'] 
  label = param_labels[param_name]
  ax.set_xlabel( label, fontsize=label_size )
  ax.tick_params(axis='x', which='major', direction='in', labelsize=tick_label_size, length=tick_length, width=tick_width, color=text_color, labelcolor=text_color )
  
  if i == 0: ax.legend( loc=1, frameon=False, fontsize= 13)
  
    

figure_name = output_dir + figure_name
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


