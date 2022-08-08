import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from figure_functions import *
from colors import *


proj_dir = data_dir + 'projects/wdm/'
base_dir = data_dir + 'cosmo_sims/wdm_sims/compare_wdm/'
output_dir = proj_dir + 'figures/'

n_snap = 29

normalized = False

data_names = [ 'cdm', 'm4.0kev', 'm3.0kev',  'm2.0kev', 'm1.0kev' ]
# data_names = [ 'cdm', 'm5.0kev', 'm4.0kev',  'm2.0kev', 'm1.0kev' ]
labels = [ r'$\mathregular{CDM}$', r'$m_\mathregular{WDM}=4.0 \,\mathregular{keV}$', r'$m_\mathregular{WDM}=3.0 \,\mathregular{keV}$', r'$m_\mathregular{WDM}=2.0 \,\mathregular{keV}$', r'$m_\mathregular{WDM}=1.0 \,\mathregular{keV}$']
n_sims = len(data_names)

space = 'redshift'

data_all = {}

for data_id,data_name in enumerate(data_names):
  # data_name = data_names[0]
  sim_name = f'1024_25Mpc_{data_name}'
  input_dir = base_dir + sim_name + '/'
  file_name = input_dir + f'flux_power_spectrum/flux_ps_{space}_{n_snap:03}.h5'
  # file_name = input_dir + f'analysis_files/{n_snap}_analysis.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  k_vals = file['k_vals'][...]
  ps_mean = file['ps_mean'][...]
  # print( z)
  # k_vals = file['lya_statistics']['power_spectrum']['k_vals'][...]
  # ps_mean = file['lya_statistics']['power_spectrum']['p(k)'][...]
  # F_mean = file['lya_statistics'].attrs['Flux_mean_HI'][0]
  # print( F_mean )
  indices = ps_mean > 0 
  ps_mean = ps_mean[indices]
  k_vals = k_vals[indices]
  file.close()
  data_all[data_id] = { 'k_vals':k_vals, 'ps_mean':ps_mean }
  


colors = [ 'k', sky_blue,  ocean_green, light_orange, light_red  ]   

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
h_length = 4
main_length = 3

fig_width = ncols * figure_width
fig_height = nrows * figure_width

fig = plt.figure(0)
fig.set_size_inches(fig_width, fig_height )
fig.clf()

gs = plt.GridSpec(h_length, ncols)
gs.update(hspace=0.0, wspace=0.18, )

i = 0
ax1 = plt.subplot(gs[0:main_length, i])
ax2 = plt.subplot(gs[main_length:h_length, i])

x_range = [3e-3, 3e-1]
y_range = [3e-4, 7e-1]

data = data_all

ref_id = 0

for data_id in data:

  lw, ls = 2, '-'
  if data_id == 0: lw, ls = 2., '-'

  k_vals = data[data_id]['k_vals']
  ps_mean = data[data_id]['ps_mean']
  ps_mean *= k_vals / np.pi

  label = labels[data_id]
  zorder = n_sims - data_id - 1 
  color = colors[data_id]
  ax1.plot( k_vals, ps_mean, c=color, label=label, zorder=zorder, lw=lw )

  ps_mean = data[data_id]['ps_mean']
  ps_reff = data[ref_id]['ps_mean']
  ps_diff = ps_mean / ps_reff 

  if data_id == ref_id: ax2.axhline( y=1., c='k', ls='--', zorder=zorder) 
  else: ax2.plot( k_vals, ps_diff, c=color, label=label, zorder=zorder, lw=lw )


k_min = 10**-2.2
k_max = 10**-0.7
alpha = 0.25
ax1.fill_between( [0, k_min], [-1, -1 ], [1000, 1000], color='gray', alpha=alpha )
ax1.fill_between( [k_max, 1], [-1, -1 ], [1000, 1000], color='gray', alpha=alpha )
ax2.fill_between( [0, k_min], [-1, -1 ], [1000, 1000], color='gray', alpha=alpha )
ax2.fill_between( [k_max, 1], [-1, -1 ], [1000, 1000], color='gray', alpha=alpha )

ax1.text(0.9, 0.95, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax1.transAxes, fontsize=figure_text_size, color=text_color) 
ax1.legend( frameon=False, loc=3, fontsize=legend_font_size)


ax1.set_ylabel( r'$\pi^{\mathregular{-1}} \,k \,P\,(k)$', fontsize=label_size, color= text_color )  
ax1.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax1.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
ax1.set_xscale('log')
ax1.set_yscale('log')
[sp.set_linewidth(border_width) for sp in ax1.spines.values()]



ax2.set_ylabel( r'$ P\,(k) / P_\mathregular{CDM}\,(k)$', fontsize=label_size, color= text_color )  
ax2.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size, color=text_color, labelpad=-5 )
ax2.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax2.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
ax2.set_xscale('log')
[sp.set_linewidth(border_width) for sp in ax2.spines.values()]
ax2.set_yticks([ 0, 0.5, 1.0, 1.5, 2.0])


ax1.set_xlim( x_range[0], x_range[1] )
ax1.set_ylim( y_range[0], y_range[1] )
ax2.set_xlim( x_range[0], x_range[1] )
ax2.set_ylim(0, 2 )

fig.align_ylabels()
# 
figure_name = output_dir + f'flux_ps_wdm.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )




