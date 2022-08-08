import sys, os, time
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
sys.path.append( cosmo_dir + 'lya_statistics/data' )
from tools import *
from figure_functions import *
from data_thermal_history import *
from interpolation_functions import interp_line_cubic


proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + f'figures/'
create_directory( output_dir )


grid_names = [ '1024_wdmgrid_extended_beta', '1024_wdmgrid_cdm_extended_beta' ]

sim_labels = [ 'Best Fit WDM Grid', 'Best Fit CDM-Only Grid', ]
 

fit_name = 'fit_results_P(k)+_Boera_covmatrix'
stats_all = {}
for sim_id, grid_name in enumerate(grid_names):
  grid_dir = data_dir + f'cosmo_sims/sim_grid/{grid_name}/'
  input_dir = grid_dir + f'fit_mcmc/{fit_name}/'
  file_name = input_dir + 'T0_stats.pkl'
  stats = Load_Pickle_Directory( file_name )
  stats_all[sim_id] = stats



nrows = 1
ncols = 1

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

bar_alpha = 0.5

line_width = 0.6
border_width = 1.5

text_color  = 'black'

sim_colors = [ 'midnightblue', 'orange' ]
c_boera = 'dodgerblue'
c_gaikwad = 'C3'

plot_boera = True 
plot_gaikwad = True

fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))

n_samples_interp = 1000

plot_key = 'mean'
for sim_id in stats_all:
  stats = stats_all[sim_id]
  z = stats['z']
  T0 = stats[plot_key] / 1e4
  high = stats['high']
  low = stats['low']
  label = sim_labels[sim_id]
  color = sim_colors[sim_id]
  z_end = 4.0
  z_interp = np.linspace( z[0], z_end, n_samples_interp )
  T0_interp = interp_line_cubic( z, z_interp, T0 )
  low_interp = interp_line_cubic( z, z_interp, low )
  high_interp = interp_line_cubic( z, z_interp, high ) 
  ax.plot( z_interp, T0_interp, label=label, color=color, zorder=2 )
  ax.fill_between( z_interp, high_interp/1e4, low_interp/1e4, alpha=bar_alpha, zorder=1, color=color )  
  
if plot_boera:
  data_set = data_thermal_history_Boera_2019
  data_z = data_set['z']
  data_mean = data_set['T0'] 
  data_error = np.array([ data_set['T0_sigma_minus'], data_set['T0_sigma_plus'] ])
  name = data_set['name']   
  ax.errorbar( data_z, data_mean/1e4, yerr=data_error/1e4, label=name, fmt='o', color= c_boera, zorder=3)

if plot_gaikwad:    
  data_set = data_thermal_history_Gaikwad_2020a
  data_z = data_set['z']
  data_mean = data_set['T0'] 
  data_error =  np.array([ data_set['T0_sigma_minus'],  data_set['T0_sigma_plus'] ])
  name = data_set['name']   
  ax.errorbar( data_z, data_mean/1e4, yerr=data_error/1e4, label=name, fmt='o', color= c_gaikwad, zorder=3)
  
ax.legend( loc=2, frameon=False, fontsize=legend_font_size )

ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax.set_ylabel( r'$T_0   \,\,\,\, \mathregular{[10^4 \,\,\,K\,]}$', fontsize=label_size, color=text_color  )
ax.set_xlabel( r'$\mathregular{Redshift} \,\,\, z$', fontsize=label_size, color=text_color )
[sp.set_linewidth(border_width) for sp in ax.spines.values()]


ax.set_xlim( 4, 7. )
ax.set_ylim( 0.57, 1.45 )


# figure_name = output_dir + f'T0_evolution_{plot_key}.png'
figure_name = output_dir + f'T0_evolution.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
