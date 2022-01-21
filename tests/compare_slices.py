import os, sys
from os import listdir
from os.path import isfile, join
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from load_data import load_snapshot_data_distributed
from tools import *

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

sim_dir = data_dir + 'cosmo_sims/1024_50Mpc/'
input_dir_0 = sim_dir + 'snapshot_files_grackle/'
input_dir_1 = sim_dir + 'snapshot_files_cholla/'
output_dir  = sim_dir + 'figures/slices/'
create_directory( output_dir ) 

precision = np.float64
Lbox = 50000.0    #kpc/h
n_cells = 1024
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid


data_type = 'hydro'

# fields = [ 'density', 'momentum_x', 'momentum_y', 'momentum_z', 'GasEnergy', 'Energy'  ]
fields = [ 'density', 'temperature', 'HI_density' ]
diff = {}

slice_start, slice_depth = 0, 256

n_snapshot = 10 

slices = {} 
data_0 = load_snapshot_data_distributed( data_type, fields, n_snapshot, input_dir_0, box_size, grid_size,  precision, show_progess=True )
data_1 = load_snapshot_data_distributed( data_type, fields, n_snapshot, input_dir_1, box_size, grid_size,  precision, show_progess=True )
z_0 = data_0['Current_z']
z_1 = data_1['Current_z']
if np.abs( z_0 - z_1 ) > 1e-3:
  print( 'ERROR: Redshift of snapshots does not match')
  exit(-1)  

for field in fields:
  if field not in slices: slices[field] = {}
  slices[field][0] = data_0[field][slice_start:slice_start+slice_depth, :, :].sum( axis=0 ) / slice_depth
  slices[field][1] = data_1[field][slice_start:slice_start+slice_depth, :, :].sum( axis=0 ) / slice_depth
  
n_fields = len( fields )

label_size = 16
figure_text_size = 16
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
text_color = 'white'
legend_font_size = 14

ncols, nrows = 3, n_fields
figure_width = 6
figure_height = 6
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*figure_width, nrows*figure_height))
plt.subplots_adjust( hspace = 0.02, wspace=0.02 )

delta = 0.2

cmaps = [ 'viridis', 'jet', 'cividis' ]

for field_id, field in enumerate(fields):
  slice_0 = slices[field][0]
  slice_1 = slices[field][1]
  diff = ( slice_1 - slice_0 ) / slice_0
  
  slice_0 = np.log10( slice_0 )
  slice_1 = np.log10( slice_1 )
  vmin, vmax = min( slice_0.min(), slice_1.min() ), max( slice_0.max(), slice_1.max() )
  
  cmap = cmaps[field_id]
  ax_l[field_id][0].imshow( slice_0, vmin=vmin, vmax=vmax, cmap=cmap )
  ax_l[field_id][1].imshow( slice_1, vmin=vmin, vmax=vmax, cmap=cmap )
  im=ax_l[field_id][2].imshow( diff, vmin=-delta, vmax=delta, cmap='bwr' )
  
  fig.colorbar(im, ax=ax_l.ravel().tolist(), shrink=0.5)
  
  
  ax_l[0][0].text(0.1, 0.93, r'$z=${0:.1f}'.format(z_0), horizontalalignment='center',  verticalalignment='center', transform=ax_l[0][0].transAxes, fontsize=figure_text_size, color=text_color) 

  
  for i in range(3):
    ax_l[field_id][i].set_xticks([])
    ax_l[field_id][i].set_yticks([])
  
  
  ax_l[field_id][0].set_ylabel( field, fontsize=label_size )
  if field_id == 0: 
    ax_l[field_id][0].set_title( 'Grackle', fontsize=label_size )
    ax_l[field_id][1].set_title( 'Cholla', fontsize=label_size )
    ax_l[field_id][2].set_title( 'Fractional Difference', fontsize=label_size )
    
            



figure_name = output_dir + f'slices_comparison_{n_snapshot}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )



  