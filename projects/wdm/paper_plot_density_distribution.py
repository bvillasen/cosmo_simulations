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

normalized = False

data_names = [ 'cdm', 'wdm_m4.0kev', 'wdm_m3.0kev',  'wdm_m2.0kev', 'wdm_m1.0kev' ]
labels = [ r'$\mathrm{CDM}$', r'$m_\mathrm{WDM}=4.0 \,\mathrm{keV}$', r'$m_\mathrm{WDM}=3.0 \,\mathrm{keV}$', r'$m_\mathrm{WDM}=2.0 \,\mathrm{keV}$', r'$m_\mathrm{WDM}=1.0 \,\mathrm{keV}$']
n_sims = len(data_names)

input_dir = base_dir + 'density_distribution/'
data_density = {}
for data_id, data_name in enumerate(data_names):
  file_name = input_dir + f'density_distribution_{data_name}_{n_snap}.pkl'
  if normalized: file_name = input_dir + f'density_distribution_{data_name}_{n_snap}_normalized.pkl'
  data_density[data_id] = Load_Pickle_Directory( file_name )


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

nrows, ncols = 1, 1

fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.2 )


x_label = r'$\rho_\mathrm{gas}/\bar{\rho}$' 
y_label = r'$f(\rho_\mathrm{gas}/\bar{\rho})$'


x_range = [7e-2, 2e1]
y_max = .032

data = data_density

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
  
  ax.set_xscale('log')
  
  ax.text(0.09, 0.95, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 

  ax.legend( frameon=False, loc=1, fontsize=12)

  ax.set_ylabel( y_label, fontsize=label_size, color= text_color )  
  ax.set_xlabel( x_label, fontsize=label_size, color=text_color )
  ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
  ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

  [sp.set_linewidth(border_width) for sp in ax.spines.values()]
  
  ax.set_xlim( x_range[0], x_range[1] )
  ax.set_ylim( 0, y_max )

figure_name = output_dir + f'density_distribution.png'
if normalized: figure_name = output_dir + f'density_distribution_normalized.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )




