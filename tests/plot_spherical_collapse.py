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

sim_dir = '/gpfs/alpine/csc380/proj-shared/cholla/spherical_collapse/'
input_dir = sim_dir + 'snapshot_files/'
output_dir  = sim_dir + 'figures/'
create_directory( output_dir ) 

precision = np.float64
Lbox = 1.0  
n_cells = 256
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid



data_type = 'hydro'
fields = [ 'density' ]

snapshots = np.arange( 0, 1, 1, dtype=int )

cmap = 'jet'

for n_snapshot in snapshots:

  data = load_snapshot_data_distributed( data_type, fields, n_snapshot, input_dir, box_size, grid_size, precision, subgrid=None, show_progess=True )
  t = data['t']
  slice =  data['density'][n_cells//2,:,:]
    
  
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
  
  ncols, nrows = 1, 1
  figure_width = 6
  figure_height = 6
  fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*figure_width, nrows*figure_height))
  plt.subplots_adjust( hspace = 0.02, wspace=0.02 )
  
  
  
  
  ax.imshow( slice,  cmap=cmap )
  ax_l.text(0.1, 0.93, r'$t=${0:.2f}'.format(t), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 
  
  plt.box(False)
  
  
  figure_name = output_dir + f'slice_{n_snapshot}.png' 
  fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
  print( f'Saved Figure: {figure_name}' )
  
  
  
  