import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
from scipy import interpolate as interp 
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from colors import *
from plot_mcmc_corner import Plot_Corner
from mcmc_sampling_functions import Get_Highest_Likelihood_Params
from figure_functions import *

grid_name = '1024_wdmgrid_extended_beta'

data_name_0 = 'fit_results_P(k)+_Boera_covmatrix_inv_mwdm_off'
data_name_1 = 'fit_results_P(k)+_Boera_covmatrix'
data_names = [ data_name_0, data_name_1 ]


proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + f'figures/paper_revision/'
create_directory( output_dir )

samples_all = {}
samples_all['param'] = {}
for data_id, data_name in enumerate(data_names):
   
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

# p_names = [ 'inv_wdm_mass', 'scale_H_ion', 'scale_H_Eheat', 'deltaZ_H' ]
# p_names = [ 'wdm_mass', 'scale_H_ion', 'scale_H_Eheat', 'deltaZ_H' ]
# 
# param_values = {}
# for p_id, p_name in enumerate(p_names):
#   param_values[p_name] = {}
#   val = params_HL[p_id]
#   p_stats = stats[p_name]
#   low = p_stats['quantiles'][2.5]
#   high = p_stats['quantiles'][97.5]
#   delta_l = val - low
#   delta_h = high - val
#   param_values[p_name]['value'] = val
#   param_values[p_name]['delta_h'] = delta_h
#   param_values[p_name]['delta_l'] = delta_l
# # 

indx = 0
name  = samples_all['param'][indx][0]['name']
trace = samples_all['param'][indx][0]['trace']
n_bin = 100
bin_min, bin_max = 1.5, 100
bins_1D = np.linspace( bin_min, bin_max, n_bin )
hist, bin_edges = np.histogram( trace, bins=bins_1D ) 
hist = hist.astype(np.float) / hist.sum()
bin_centers = ( bin_edges[:-1] + bin_edges[1:] ) / 2.
bin_width = bin_centers[0] - bin_centers[1]
bin_centers_interp = np.linspace( bin_centers[0], bin_centers[-1], 100000 )
f_interp  = interp.interp1d( bin_centers, hist,  kind='cubic' )
f_interp_0  = interp.interp1d( 1/bin_centers, hist,  kind='cubic' )
mwdm_distribution = f_interp(bin_centers_interp)
indx_neg = mwdm_distribution < 0
mwdm_distribution[indx_neg] = 0 

indx_max = np.where(mwdm_distribution == mwdm_distribution.max())[0]
mwdm_max = bin_centers_interp[indx_max]


indx = 1
name  = samples_all['param'][indx][0]['name']
trace = samples_all['param'][indx][0]['trace']
n_bin = 80
bin_min, bin_max = 1/100, 0.5
bins_1D = np.linspace( bin_min, bin_max, n_bin )
hist, bin_edges = np.histogram( trace, bins=bins_1D ) 
hist = hist.astype(np.float) / hist.sum()
bin_centers = ( bin_edges[:-1] + bin_edges[1:] ) / 2.
bin_width = bin_centers[0] - bin_centers[1]
bin_centers_interp_1 = np.linspace( bin_centers[0], bin_centers[-1], 100000 )
f_interp  = interp.interp1d( bin_centers, hist,  kind='cubic' )
mwdm_distribution_0 = f_interp_0(bin_centers_interp_1)
mwdm_distribution_1 = f_interp(bin_centers_interp_1)
indx_neg = mwdm_distribution < 0
mwdm_distribution_1[indx_neg] = 0 

indx_neg = mwdm_distribution_0 < 0
mwdm_distribution_0[indx_neg] = 0 

fig_width = 8
fig_dpi = 300
label_size = 18
figure_text_size = 16
legend_font_size = 14
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 6
tick_size_minor = 4
tick_width_major = 2
tick_width_minor = 1.5
border_width = 1.5
text_color = 'k'

nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))


fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))

line_color = 'C0'
label = 'Sampling over ' + r'$m_{\mathregular{WDM}}$'
mwdm_dist = mwdm_distribution_0
mwdm_dist /= mwdm_dist.sum()
ax.plot( bin_centers_interp_1, mwdm_dist,   color=line_color, label=label, zorder=3  )

line_color = 'C1'

mwdm_dist_1 = mwdm_distribution_1 
mwdm_dist_1 /= mwdm_dist_1.sum()

label = 'Sampling over ' + r'$m_{\mathregular{WDM}}^{\mathregular{-1}}$' 
ax.plot( bin_centers_interp_1, mwdm_dist_1,   color=line_color, label=label, zorder=3  )


x_label = r'$m_{\mathregular{WDM}}^{\mathregular{-1}} \,\,\, \mathregular{[keV^{-1}]}$'
y_label = r'$\mathcal{L}(m_{\mathregular{WDM}}^{\mathregular{-1}}) $'
ax.set_ylabel( y_label, fontsize=label_size, color= text_color )  
ax.set_xlabel( x_label, fontsize=label_size, color=text_color )
ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

[sp.set_linewidth(border_width) for sp in ax.spines.values()]


ax.legend( frameon=False, loc=1, fontsize=legend_font_size, labelcolor=text_color )

figure_name = output_dir + f'mwdm_distribution.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )



print( f'Saved Figure: {figure_name}' )
