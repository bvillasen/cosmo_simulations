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
base_dir = proj_dir + 'data/'
output_dir = proj_dir + 'figures/'

n_snap = 29

data_names = [ 'cdm', 'wdm_m4.0kev', 'wdm_m3.0kev',  'wdm_m2.0kev', 'wdm_m1.0kev' ]
labels = [ 'CDM', r'$m_\mathrm{WDM}=4.0 \,keV$', r'$m_\mathrm{WDM}=3.0 \,keV$', r'$m_\mathrm{WDM}=2.0 \,keV$', r'$m_\mathrm{WDM}=1.0 \,keV$']
n_sims = len( data_names )

input_dir = base_dir + 'density_distribution/'
data_density = {}
for data_id, data_name in enumerate(data_names):
  file_name = input_dir + f'density_distribution_{data_name}_{n_snap}.pkl'
  data_density[data_id] = Load_Pickle_Directory( file_name )

input_dir = base_dir + 'flux_distribution/'
data_flux = {}
for data_id, data_name in enumerate(data_names):
  file_name = input_dir + f'flux_distribution_{data_name}_{n_snap}.pkl'
  data_flux[data_id] = Load_Pickle_Directory( file_name )


data_all = [ data_density, data_flux ]

colors = [ 'k', sky_blue,  ocean_green, light_orange, light_red  ]   

fig_width = 8
fig_dpi = 300
label_size = 18
figure_text_size = 16
legend_font_size = 16
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
border_width = 1.5
text_color = 'k'

nrows, ncols = 1, 2

fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.2 )


x_labels = [ r'$\rho_\mathrm{gas}/\bar{\rho}$', r'$F$',  ]
y_labels = [ r'$f(\rho_\mathrm{gas}/\bar{\rho})$', r'$f(F\,)$'   ]

x_range = [ [7e-2, 2e1], [7e-2, 1]  ]
y_max = [ .032, .03 ]


f_min, f_max = 10, 0

for i in range(2):
  
  ax = ax_l[i]
  data = data_all[i]
  
  for data_id in data:
    
    lw, ls = 2, '-'
    if data_id == 0: lw, ls = 2., '-'
    
    z = data[data_id]['z']
    bin_centers = data[data_id]['bin_centers']
    distribution = data[data_id]['distribution']
    
    label = labels[data_id]
    zorder = n_sims - data_id - 1 
    color = colors[data_id]
    ax.plot( bin_centers, distribution, c=color, label=label, zorder=zorder, lw=lw )
    
    if i == 1:
      F_mean = data[data_id]['F_mean']
      
      arr_length, arr_width = 0.002, 0.002
      head_length = arr_length*0.2
      head_width = 3 * arr_width
      plt.arrow( F_mean, arr_length, 0, -arr_length+head_length*1.25, color=color, width=arr_width, head_length=head_length, head_width=head_width, zorder=zorder ) 
      
      f_min = min( F_mean, f_min )
      f_max = max( F_mean, f_max )
      
  if i == 1:  
    y_line = arr_length * 1.2
    delta = 0.03
    plt.plot( [f_min*(1-delta), f_max* (1+delta)], [y_line, y_line], c='k' )
    ax.text( 0.4, .11, r'$\overline{F}$', horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=15, color=text_color) 

  
  ax.set_xscale('log')
  


  if i == 0: ax.text(0.09, 0.95, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 

  loc = 1
  if i == 1: loc = 2   
  ax.legend( frameon=False, loc=loc, fontsize=12)

  ax.set_ylabel( y_labels[i], fontsize=label_size, color= text_color )  
  ax.set_xlabel( x_labels[i], fontsize=label_size, color=text_color )
  ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
  ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

  [sp.set_linewidth(border_width) for sp in ax.spines.values()]
  
  ax.set_xlim( x_range[i][0], x_range[i][1] )
  ax.set_ylim( 0, y_max[i])

figure_name = output_dir + f'density_flux_distributions.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )




