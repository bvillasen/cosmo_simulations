import os, sys
from os import listdir
from os.path import isfile, join
from shutil import copyfile
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1 import ImageGrid
import palettable
import pickle
root_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from load_data import load_snapshot_data_distributed
from tools import *

use_mpi = False
if use_mpi :
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  nprocs = comm.Get_size()
else:
  rank = 0
  nprocs = 1
  
show_progess = False
if rank == 0: show_progess = True

sim_dir    = data_dir + f'cosmo_sims/cholla_ics/4096_375Mpc/'
input_dir = sim_dir + 'slices_gas_density/'
output_dir  = sim_dir + 'slices_gas_density_extended/'
if rank == 0: create_directory( output_dir )
  
n_points = 4096
Lbox = 375000.0 #kpc/h
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_points, n_points, n_points ]
precision = np.float32
  
fields = [ 'density' ]
data_type = 'hydro'

slice_depth = 128

n_slices = n_points // slice_depth
slices = np.linspace( 0, n_slices-1, n_slices, dtype=int )
slices_local = split_array_mpi( slices, rank, nprocs )
print( f' Rank: {rank}  slices_local:{slices_local}' )

n_snap = 5

slice_id = 3
# for slice_id in slices_local:
slice_start = slice_id * slice_depth

file_name = input_dir + f'slice_{n_snap}_start{slice_start}_depth{slice_depth}.h5'
print( f'Loading File: {file_name}' )
file = h5.File( file_name, 'r' )

density = file['density'][...]
file.close()
# 
# nz, ny, nx = density.shape
# 
# n_ghost = 512
# density_extended = np.zeros( [nz, ny+2*n_ghost, nx+2*n_ghost ])
# density_extended[:, n_ghost:-n_ghost, n_ghost:-n_ghost] = density
# density_extended[:,:n_ghost,:] = density_extended[:,-2*n_ghost:-n_ghost,:]
# density_extended[:,-n_ghost:,:] = density_extended[:,n_ghost:2*n_ghost,:]
# density_extended[:,:,:n_ghost] = density_extended[:,:,-2*n_ghost:-n_ghost]
# density_extended[:,:,-n_ghost:] = density_extended[:,:,n_ghost:2*n_ghost] 
# 
# 
# file_name = output_dir + f'slice_{n_snap}_start{slice_start}_depth{slice_depth}.h5'
# file = h5.File( file_name, 'w' )
# 
# file.create_dataset( 'density', data=density_extended )
# file.close()
# print( f'Saved File: {file_name}' )

