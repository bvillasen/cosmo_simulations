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
input_dir = data_dir + 'cosmo_sims/1024_25Mpc_wdm/power_spectrum_files/'
output_dir = proj_dir + 'figures/'
create_directory( output_dir )


data_names = [ 'cdm', 'm_2.0kev', 'm_3.0kev', 'm_4.0kev', 'm_5.0kev' ]

labels = [ 'CDM', r'$m_\mathrm{WDM}=2 \, keV$', r'$m_\mathrm{WDM}=3 \, keV$', r'$m_\mathrm{WDM}=4 \, keV$', r'$m_\mathrm{WDM}=5 \, keV$']

z_id = 1

data_all = {}
for data_id, data_name in enumerate(data_names):
  file_name = input_dir + f'power_spectrum_hydro_{data_name}.pkl'
  ps_data_all = Load_Pickle_Directory( file_name ) 
  ps_data = ps_data_all[z_id]
  z = ps_data['z']
  k_vals = ps_data['k_vals'][:-1]
  power_spectrum = ps_data['power_spectrum'][:-1]
  data_all[data_id] = { 'k_vals':k_vals, 'power_spectrum':power_spectrum }

reference_id = 0
for data_id in data_all:
  data_all[data_id]['ps_ratio'] = data_all[data_id]['power_spectrum'] / data_all[reference_id]['power_spectrum']   


data_all_dm = {}
for data_id, data_name in enumerate(data_names):
  file_name = input_dir + f'power_spectrum_particles_{data_name}.pkl'
  ps_data_all = Load_Pickle_Directory( file_name ) 
  ps_data = ps_data_all[z_id]
  z = ps_data['z']
  k_vals = ps_data['k_vals'][:-1]
  power_spectrum = ps_data['power_spectrum'][:-1]
  data_all_dm[data_id] = { 'k_vals':k_vals, 'power_spectrum':power_spectrum }

for data_id in data_all:
  data_all_dm[data_id]['ps_ratio'] = data_all_dm[data_id]['power_spectrum'] / data_all_dm[reference_id]['power_spectrum']   



sim_dir = input_dir = data_dir + 'cosmo_sims/1024_25Mpc_wdm/'

flux_ps_data = {}

n_file = 25
for data_id, data_name in enumerate(data_names):
  input_dir = sim_dir + data_name + '/analysis_files/'
  file_name = input_dir + f'{n_file}_analysis.h5'
  file = h5.File( file_name, 'r' )
  k  = file['lya_statistics']['power_spectrum']['k_vals'][...]
  pk = file['lya_statistics']['power_spectrum']['p(k)'][...] 
  indices =  pk > 0 
  k = k[indices][:-1]
  pk = pk[indices][:-1]
  flux_ps_data[data_id] = { 'k_vals': k, 'ps_mean':pk }
   
for data_id in data_all:
  flux_ps_data[data_id]['ps_ratio'] = flux_ps_data[data_id]['ps_mean'] / flux_ps_data[reference_id]['ps_mean']   

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

nrows, ncols = 1, 3

fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.15)

ax = ax_l[0]
for data_id in data_all:
  k_vals = data_all_dm[data_id]['k_vals']
  ps_ratio = data_all_dm[data_id]['ps_ratio']
  ax.plot( k_vals, ps_ratio, label=labels[data_id])
  
# ax.text(0.8, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 
ax.legend(frameon=False, fontsize=legend_font_size, loc=3 )  
ax.set_xscale('log')
ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax.set_ylabel( r'$P_\mathrm{DM}(k) \, / \, P_\mathrm{DM,CDM}(k)$', fontsize=font_size, color=text_color  )
ax.set_xlabel( r'$k$  [$h$ Mpc$^{\mathrm{\mathregular{-1}}}$]', fontsize=font_size, color=text_color )
[sp.set_linewidth(border_width) for sp in ax.spines.values()]

ax = ax_l[1]
for data_id in data_all:
  k_vals = data_all[data_id]['k_vals']
  ps_ratio = data_all[data_id]['ps_ratio']
  ax.plot( k_vals, ps_ratio, label=labels[data_id])
  
ax.text(0.8, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 
ax.legend(frameon=False, fontsize=legend_font_size, loc=2 )  
ax.set_xscale('log')
ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax.set_ylabel( r'$P_\mathrm{gas}(k) \, / \, P_\mathrm{gas,CDM}(k)$', fontsize=font_size, color=text_color  )
ax.set_xlabel( r'$k$  [$h$ Mpc$^{\mathrm{\mathregular{-1}}}$]', fontsize=font_size, color=text_color )
[sp.set_linewidth(border_width) for sp in ax.spines.values()]

ax = ax_l[2]
for data_id in flux_ps_data:
  k_vals = flux_ps_data[data_id]['k_vals']
  ps_ratio = flux_ps_data[data_id]['ps_ratio']
  ax.plot( k_vals, ps_ratio, label=labels[data_id] )
  
  ax.legend(frameon=False, fontsize=legend_font_size, loc=3 )  
ax.set_xscale('log')
ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax.set_ylabel( r'$P_\mathrm{flux}(k) \, / \, P_\mathrm{flux,CDM}(k)$', fontsize=font_size, color=text_color  )
ax.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=font_size, color=text_color )
[sp.set_linewidth(border_width) for sp in ax.spines.values()]


figure_name = output_dir + 'ps_ratio_wdm.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


