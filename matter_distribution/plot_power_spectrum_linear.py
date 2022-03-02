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

base_dir = data_dir + 'cosmo_sims/test_ics/'
input_dir  = base_dir + f'snapshot_files_music/'
output_dir = base_dir + f'figures/'
create_directory( output_dir )

snap_ids = [0 ]

pk_data_music = {}
file_name = base_dir + f'power_spectrum_music_hydro.pkl'
pk_data_music['hydro'] = Load_Pickle_Directory( file_name )
file_name = base_dir + f'power_spectrum_music_particles.pkl'
pk_data_music['particles'] = Load_Pickle_Directory( file_name )

pk_data_python = {}
file_name = base_dir + f'power_spectrum_python_hydro.pkl'
pk_data_python['hydro'] = Load_Pickle_Directory( file_name )
file_name = base_dir + f'power_spectrum_python_particles.pkl'
pk_data_python['particles'] = Load_Pickle_Directory( file_name )


data_type = 'hydro'
# data_type = 'particles'

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

ncols, nrows = 2, 2
figure_width = 6
figure_height = 12
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*figure_width,figure_height))
plt.subplots_adjust( hspace = 0.15, wspace=0.2)


for i in range(nrows):
  for j in range(ncols):
    fig_id = j + i*ncols
    ax = ax_l[i][j]
    
    if j == 0: pk_data_all = pk_data_music
    if j == 1: pk_data_all = pk_data_python
    
    if i == 0: pk_data = pk_data_all['particles']
    if i == 1: pk_data = pk_data_all['hydro']
  
    for data_id in pk_data:
      snap_data = pk_data[data_id]
      z = snap_data['z']
      k_vals = snap_data['k_vals']
      power_spectrum = snap_data['power_spectrum']
      # power_spectrum *= k_vals**3
      label = ''
      ax.plot( k_vals, power_spectrum, label=label )
      
    # 
    # ax.text(0.9, 0.95, r'$z=${0:.1f}'.format(np.round(z)), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 
    # 
    leg = ax.legend(  loc=3, frameon=False, fontsize=legend_font_size    )
    
    # ax.set_xlim( -2.5, 4 )
    # ax.set_ylim( 0, .1 )
    
    ax.set_yscale('log')
    ax.set_xscale('log')
    
    # ax.set_ylabel( r' $P\,(k) [h^3\, \mathrm{Mpc}^{-3}]$', fontsize=label_size, color= text_color )
    ax.set_ylabel( r' $P\,(k) [h^3\, \mathrm{Mpc}^{-3}]$', fontsize=label_size, color= text_color )
    ax.set_xlabel( r'$k \,\, [h\, \mathrm{Mpc}^{-1}]$', fontsize=label_size, color= text_color )
    
    ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')


figure_name = output_dir + f'power_spectrum.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )

