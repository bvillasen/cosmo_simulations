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

fit_name = 'fit_results_P(k)+_Boera_covmatrix'
output_dir = data_dir + f'figures/wdm/'
create_directory( output_dir )


grid_names = [ '1024_wdmgrid_nsim600', '1024_wdmgrid_cdm' ]

sim_labels = [ 'Best Fit', 'Best Fit CDM', ]
 

sim_id = 0
stats_all = {}
for sim_id, grid_name in enumerate(grid_names):
  grid_dir = data_dir + f'cosmo_sims/sim_grid/{grid_name}/'
  input_dir = grid_dir + f'fit_mcmc/{fit_name}/'
  file_name = input_dir + 'T0_stats.pkl'
  stats = Load_Pickle_Directory( file_name )
  stats_all[sim_id] = stats



nrows = 1
ncols = 1

tick_size_major, tick_size_minor = 6, 4
tick_label_size_major, tick_label_size_minor = 14, 12
tick_width_major, tick_width_minor = 1.5, 1

font_size = 18
label_size = 16
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

n_samples_interp = 100

plot_key = 'mean'
for sim_id in stats_all:
  stats = stats_all[sim_id]
  z = stats['z']
  T0 = stats[plot_key]
  high = stats['high']
  low = stats['low']
  label = sim_labels[sim_id]
  color = sim_colors[sim_id]
  z_interp = np.linspace( z[0], z[-1], n_samples_interp )
  low_interp = interp_line_cubic( z, z_interp, low )
  high_interp = interp_line_cubic( z, z_interp, high ) 
  ax.plot( z, T0/1e4, label=label, color=color, zorder=2 )
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
  
ax.legend( loc=2, frameon=False)

ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax.set_ylabel( r'$T_0   \,\,\,\, \mathregular{[10^4 \,\,\,K\,]}$', fontsize=font_size, color=text_color  )
ax.set_xlabel( r'Redshift  $z$', fontsize=font_size, color=text_color )
[sp.set_linewidth(border_width) for sp in ax.spines.values()]


ax.set_xlim( 4, 7. )
ax.set_ylim( 0.55, 1.5 )


figure_name = output_dir + f'T0_evolution_{plot_key}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
