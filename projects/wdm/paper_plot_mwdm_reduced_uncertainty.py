import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate as interp
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from figure_functions import *
from colors import *
from stats_functions import get_highest_probability_interval

proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + 'figures/'

base_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_extended_beta/fit_mcmc/'

n_bins = 100
bins_1D = np.linspace( 0, 1, n_bins )

fit_names = [ 'fit_results_P(k)+_Boera_covmatrix_limited_data', 'fit_results_P(k)+_Boera_covmatrix' ]

data_all = {}
for data_id, fit_name in enumerate(fit_names):
  input_dir = base_dir + f'{fit_name}/'
  file_name = input_dir + 'samples_mcmc.pkl'
  samples = Load_Pickle_Directory( file_name )
  trace = samples[0]['trace'] 
  hist, bin_edges = np.histogram( trace, bins=bins_1D ) 
  distribution = hist.astype(np.float) / hist.sum()
  bin_centers = ( bin_edges[:-1] + bin_edges[1:] ) / 2.
  data_all[data_id] = { 'bin_centers':bin_centers.copy(), 'distribution':distribution.copy() }

colors = [ light_orange, 'C0'  ]   
labels = [ r'Fit to $k \leq 0.1 \, \mathrm{s \, km^{-1}}$ data points', 'Fit to all data points']

fig_width = 8
fig_dpi = 300
label_size = 18
figure_text_size = 16
legend_font_size = 16
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 6
tick_size_minor = 4
tick_width_major = 2
tick_width_minor = 1.5
border_width = 1.5
text_color = 'k'

nrows, ncols = 1, 1

lw = 3.0

fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.2 )

for data_id in data_all:
  
  ls = '-'
  if data_id == 1: ls = '--'

  data = data_all[data_id]
  bin_centers = data['bin_centers']
  distribution = data['distribution']

  bin_centers_interp = np.linspace( 0, bin_centers[-1], 100000 )
  f_interp  = interp.interp1d( bin_centers, distribution,  kind='cubic', fill_value='extrapolate' )
  label = labels[data_id]
  ax.plot( bin_centers_interp, f_interp(bin_centers_interp), ls=ls,   color=colors[data_id], linewidth=lw, label=label,   )
  # ax.plot( bin_centers, distribution ,   color=colors[data_id], linewidth=lw, label=label,   )

  if data_id == 0:
    hl_color = 'gray' 
    hl_line_width = 2.5 
    
    hl_val = 0.0
    fill_sum = 0.68
    v_l, v_r, v_max,  sum = get_highest_probability_interval( bin_centers, distribution, fill_sum, log=False, n_interpolate=100000, print_eval=False)
    print( f'Eval f(l): {f_interp(v_l)}  f(r): {f_interp(v_r)}  sum: {sum}')
    vals_simgna = np.linspace( 0, v_r, 1000 )
    sigma_l = hl_val - v_l
    sigma_r = v_r - hl_val
    ax.fill_between( vals_simgna, f_interp(vals_simgna), color=hl_color, alpha=0.5, zorder=1)
    fill_sum = 0.95
    v_l, v_r, v_max,  sum = get_highest_probability_interval( bin_centers, distribution, fill_sum, log=False, n_interpolate=100000, print_eval=False)
    print( f'Eval f(l): {f_interp(v_l)}  f(r): {f_interp(v_r)}  sum: {sum}')
    vals_simgna = np.linspace( 0, v_r, 1000 )
    two_sigma_l = hl_val - v_l
    two_sigma_r = v_r - hl_val
    ax.fill_between( vals_simgna, f_interp(vals_simgna), color=hl_color, alpha=0.3, zorder=1)


ax.legend( frameon=False, loc=2, fontsize=legend_font_size)

y_label = r'$\mathcal{L}(m_{\mathregular{WDM}}^{\mathregular{-1}})$'
x_label = r'$m_{\mathregular{WDM}}^{\mathregular{-1}} \,\,\, \mathregular{[keV^{-1}]}$'
ax.set_ylabel( y_label, fontsize=label_size, color= text_color )  
ax.set_xlabel( x_label, fontsize=label_size, color=text_color )
ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

[sp.set_linewidth(border_width) for sp in ax.spines.values()]

ax.set_xlim( 0, 0.42 )
ax.set_ylim( 0, 0.071 )


figure_name = output_dir + f'mwdm_reduced_sigma.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )

