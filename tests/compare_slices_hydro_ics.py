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

use_mpi = False
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


data_name = 'python'
sim_dir = data_dir + 'cosmo_sims/test_ics/'
input_dir = sim_dir + f'snapshot_files_{data_name}_hydro/'
output_dir  = sim_dir + 'figures/'
if rank == 0: create_directory( output_dir ) 

slice_start, slice_depth = 0, 256

precision = np.float64
Lbox = 50000.0    #kpc/h
n_cells = 256
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
subgrid = [ [slice_start, slice_start+slice_depth], [0, n_cells], [0, n_cells]]


absolute_difference = True
data_type = 'hydro'
fields = [ 'density' ]


n_snapshot = 0

data_g = load_snapshot_data_distributed( 'hydro', fields, n_snapshot, input_dir, box_size, grid_size, precision, subgrid=subgrid, show_progess=True )
data_p = load_snapshot_data_distributed( 'particles', fields, n_snapshot, input_dir, box_size, grid_size, precision, subgrid=subgrid, show_progess=True )
dens_gas = data_g['density']
dens_part = data_p['density']

diff = dens_part / dens_gas

ncols, nrows = 2, 1
figure_width = 6
figure_height = 6
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*figure_width, nrows*figure_height))
plt.subplots_adjust( hspace = 0.02, wspace=0.02 )



ax = ax_l[0]
proj = dens_part.sum( axis=0 )
ax.imshow( proj )


ax = ax_l[1]
proj = dens_gas.sum( axis=0 )
ax.imshow( proj )




figure_name = output_dir + f'slices_comparison_ics_{data_name}.png' 
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


