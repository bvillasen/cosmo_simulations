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
output_dir = proj_dir + 'figures/vel_distribution/'
create_directory( output_dir )

base_dir = data_dir + 'cosmo_sims/wdm_sims/new/'


# snap_ids = [ 6, 7, 8 ]
snap_ids = [ 8, 7, 6  ]
data_ps_all = {}

use_log  = True

sim_names =  [ '1024_25Mpc_cdm', '1024_25Mpc_m4.0kev' ]

for data_id, sim_name in enumerate( sim_names ):
  sim_dir = base_dir + sim_name +  '/'
  input_dir = sim_dir + 'velocity_distribution/'
  data_ps_all[data_id] = {}
  for snap_id, n_snap in enumerate(snap_ids):
    file_name = input_dir + f'ps_velocity_{n_snap}.pkl'
    if use_log: file_name = input_dir + f'ps_velocity_{n_snap}_log.pkl'
    data = Load_Pickle_Directory( file_name )
    data_ps_all[data_id][snap_id] = data



fig_width = 8
fig_dpi = 300
label_size = 18
figure_text_size = 18
legend_font_size = 16
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
border_width = 1

text_color = 'black'


nrows, ncols = 1, 3
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.15)


for i in range(3):
  
  data_0 = data_ps_all[0][i]
  data_1 = data_ps_all[1][i]

  z = data_0['z']
  bin_centers_0 = data_0['bin_centers']
  bin_centers_1 = data_1['bin_centers']
  distribution_0 = data_0['distribution']
  distribution_1 = data_1['distribution']
  
  distribution_0 /= distribution_0.sum()
  distribution_1 /= distribution_1.sum()
  
  ax = ax_l[i]
  ax.plot( bin_centers_0, distribution_0, label='CDM' )
  ax.plot( bin_centers_1, distribution_1, label=r'WDM  $m=4 \,\,\mathrm{keV}$' )
  
  ax.text(0.89, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 
      

  ax.legend( frameon=False, loc=5, fontsize=12)
  
  ax.set_yscale('log')
  
  ax.set_ylabel( r'$P(v)$', fontsize=label_size, color= text_color )  
  ax.set_xlabel( r'$v$  [km/s]', fontsize=label_size, color=text_color )
  ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
  ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

  
  


figure_name = output_dir + f'vel_distribution.png'
if use_log: figure_name = output_dir + f'vel_distribution_log.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


