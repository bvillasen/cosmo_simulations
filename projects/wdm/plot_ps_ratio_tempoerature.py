import sys, os
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
from data_optical_depth import *
from colors import * 
from stats_functions import compute_distribution, get_highest_probability_interval
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid
from load_tabulated_data import load_data_boera
from matrix_functions import Merge_Matrices


proj_dir = data_dir + 'projects/wdm/'
input_dir = data_dir + 'cosmo_sims/1024_25Mpc_wdm/m_3.0kev/flux_power_spectrum/'
output_dir = proj_dir + 'figures/'
create_directory( output_dir )

temp_factors = [ 1.4, 1.2, 1.0, 0.8, 0.6 ]




data_all = {}
for data_id, temp_factor in enumerate(temp_factors):
  file_name = input_dir + f'ps_data_temperature_factor_{temp_factor}.pkl'
  ps_data = Load_Pickle_Directory( file_name )
   
  k_vals = ps_data['k_vals']
  power_spectrum = ps_data['mean']
  indices = power_spectrum > 0
  data_all[data_id] = { 'k_vals':k_vals[indices], 'power_spectrum':power_spectrum[indices] }


temp_factor = 1.0
input_dir = data_dir + 'cosmo_sims/1024_25Mpc_wdm/cdm/flux_power_spectrum/'
file_name = input_dir + f'ps_data_temperature_factor_{temp_factor}.pkl'
ps_data = Load_Pickle_Directory( file_name )
k_vals = ps_data['k_vals']
ps_reference = ps_data['mean']

for data_id in data_all:
  data_all[data_id]['ps_ratio'] = data_all[data_id]['power_spectrum'] / ps_reference


font_size = 16
legend_font_size = 12

label_size = 18
figure_text_size = 18
legend_font_size = 12
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
border_width = 1
text_color = 'k'

nrows, ncols = 1, 1

fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.15)

ax = ax_l
for data_id in data_all:
  k_vals = data_all[data_id]['k_vals']
  ps_ratio = data_all[data_id]['ps_ratio']
  label = r'$\alpha_\mathrm{temp}$' + f'={temp_factors[data_id]}'
  ax.plot( k_vals, ps_ratio, label=label )

ax.axhline( y=1, ls='--', c='k')

# ax.text(0.8, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 
ax.legend(frameon=False, fontsize=legend_font_size, loc=3 )  
ax.set_xscale('log')
ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax.set_ylabel( r'$P_\mathrm{flux}(k) \, / \, P_\mathrm{flux,CDM}(k)$', fontsize=font_size, color=text_color  )
ax.set_xlabel( r'$k$  [$h$ Mpc$^{\mathrm{\mathregular{-1}}}$]', fontsize=font_size, color=text_color )
[sp.set_linewidth(border_width) for sp in ax.spines.values()]

ax.set_ylim( 0, 2)

figure_name = output_dir + 'ps_ratio_temperature.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


