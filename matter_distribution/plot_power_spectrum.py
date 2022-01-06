import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import load_snapshot_data_distributed


wdm_masses = [ 0.25, 0.5, 1.0, 2.0, 3.0 ]

input_dir  = data_dir + f'cosmo_sims/rescaled_P19/wdm/power_spectrum_files/'
output_dir = data_dir + f'cosmo_sims/rescaled_P19/wdm/figures/'
create_directory( output_dir )

snap_ids = [1, 4, 8, 13, 23, 42 ]
data_type = 'hydro'

import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

label_size = 16
figure_text_size = 14
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
text_color = 'black'
legend_font_size = 14

ncols, nrows = 2, 3
figure_width = 6
figure_height = 18
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*figure_width,figure_height))
plt.subplots_adjust( hspace = 0.15, wspace=0.2)

wdm_masses = [ 0.25, 0.5, 1.0, 2.0, 3.0 ]

sim_names = [ ]
# for wdm_mass in wdm_masses:
#   sim_names.append( f'wdm_m{wdm_mass}kev' )
sim_names.append('cdm')


for i in range(nrows):
  for j in range(ncols):
    fig_id = j + i*ncols
    snap_id = snap_ids[fig_id]
    ax = ax_l[i][j]
    
    for sim_id,sim_name in enumerate(sim_names):
      file_name = input_dir + f'power_spectrum_{sim_name}_{data_type}.pkl'
      sim_data = Load_Pickle_Directory( file_name )

      snap_data = sim_data[snap_id]
      z = snap_data['z']
      bin_centers = snap_data['bin_centers']
      distribution = snap_data['distribution']
      if sim_name == 'cdm': label = 'CDM'
      else:
        wdm_mass = wdm_masses[sim_id]
        label = f'WDM {wdm_mass} keV'
       
      ax.plot( bin_centers, distribution, label=label )
    
    ax.text(0.1, 0.95, r'$z=${0:.1f}'.format(np.round(z)), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 

    leg = ax.legend(  loc=1, frameon=False, fontsize=legend_font_size    )
    
    
    ax.set_xlim( -2.5, 4 )
    # ax.set_ylim( 0, .1 )
    
    # ax.set_ylim( 10**-8, 1 )
    # ax.set_yscale('log')
    
    ax.set_ylabel( r' $P\,(\Delta)$', fontsize=label_size, color= text_color )
    ax.set_xlabel( r'$ \mathrm{log_{10}} \, \Delta$', fontsize=label_size, color= text_color )


    ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')




figure_name = output_dir + 'density_distribution.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )

