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

use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

sim_dir = data_dir + 'cosmo_sims/cholla_ics/512_100Mpc/'
input_dir = sim_dir + 'snapshot_files/'
output_dir  = sim_dir + 'figures/'
if rank == 0: create_directory( output_dir ) 

slice_start, slice_depth = 0, 128

precision = np.float64
Lbox = 100000.0    #kpc/h
n_cells = 512
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
subgrid = [ [slice_start, slice_start+slice_depth], [0, n_cells], [0, n_cells]]


data_type = 'hydro'

fields = [ 'density' ]
diff = {}

snapshots = np.arange( 0, 6, 1, dtype=int )
snapshots_local = split_array_mpi( snapshots, rank, n_procs )
print( f'rank: {rank}  snapshots_local:{snapshots_local}' )


for n_snapshot in snapshots_local:

  slices = {} 
  data_gas = load_snapshot_data_distributed( 'hydro', fields, n_snapshot, input_dir, box_size, grid_size, precision, subgrid=subgrid, show_progess=True )
  data_particles = load_snapshot_data_distributed( 'particles', fields, n_snapshot, input_dir, box_size, grid_size, precision, subgrid=subgrid, show_progess=True )
  z = data_gas['Current_z']
  dens_gas = data_gas['density']
  dens_dm  = data_dm['density']
  
  slice_gas = dens_gas.sum( axis=0 ) / slice_depth
  slice_dm  = dens_dm.sum( axis=0 ) / slice_depth
  
  slice_gas = np.log10( slice_gas )
  slice_dm  = np.log10( slice_dm )
  
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

  ncols, nrows = 2, 1
  figure_width = 6
  figure_height = 6
  fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*figure_width, nrows*figure_height))
  plt.subplots_adjust( hspace = 0.02, wspace=0.02 )


  ax_l[0].imshow( slice_dm, cmap=cmap_dm )
  ax_l[1].imshow( slice_dm, cmap=cmap_gas )
  ax_l[0].text(0.1, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax_l[0].transAxes, fontsize=figure_text_size, color=text_color) 
    
  for i in range(2):
    ax_l[i].set_xticks([])
    ax_l[i].set_yticks([])

  figure_name = output_dir + f'slice_{n_snapshot}.png' 
  if absolute_difference: figure_name = output_dir + f'slices_comparison_absolute_{n_snapshot}.png'
  fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
  print( f'Saved Figure: {figure_name}' )



    