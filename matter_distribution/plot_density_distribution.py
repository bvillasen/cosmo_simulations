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

input_dir  = data_dir + f'cosmo_sims/rescaled_P19/wdm/density_distribution_files/'
output_dir = data_dir + f'cosmo_sims/rescaled_P19/wdm/figures/'
create_directory( output_dir )

snap_ids = [1, 4, 8, 13, 23, 42 ]

file_name = input_dir + 'density_distribution_cdm.pkl'
sim_data = Load_Pickle_Directory( file_name )

import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

label_size = 14
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
plt.subplots_adjust( hspace = 0.15, wspace=0.18)

for i in range(nrows):
  for j in range(ncols):
    fig_id = j + i*ncols
    snap_id = snap_ids[fig_id]
    
    snap_data = sim_data[snap_id]
    z = snap_data['z']
    bin_centers = snap_data['bin_centers']
    distribution = snap_data['distribution']
    
    ax = ax_l[i][j]
    ax.plot( bin_centers, distribution )
    
    ax.text(0.9, 0.93, r'$z=${0:.1f}'.format(np.round(z)), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 



figure_name = output_dir + 'density_distribution.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )

