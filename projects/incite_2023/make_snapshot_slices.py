import os, sys
from os import listdir
from os.path import isfile, join
from shutil import copyfile
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1 import ImageGrid
import pickle
root_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from load_data import load_snapshot_data_distributed
from tools import *

use_mpi = True
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
input_dir  = sim_dir + 'snapshot_files/'
output_dir = sim_dir + 'slices_gas_density/'
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

for slice_id in slices_local:

  slice_start = slice_id * slice_depth

  start = max( 0, slice_start )
  end   = min( n_points, slice_start+slice_depth )
  subgrid = [ [start, end], [0, n_points], [0, n_points] ]

  n_snap = 5
  data_snap = load_snapshot_data_distributed( data_type, fields, n_snap, input_dir, box_size, grid_size,  precision, subgrid=subgrid, show_progess=show_progess )
  current_z = data_snap['Current_z']

  print( f' Slice:  start:{start}   end:{end}' )

  out_file_name = output_dir + f'slice_{n_snap}_start{slice_start}_depth{slice_depth}.h5'
  outfile = h5.File( out_file_name, 'w' )
  outfile.attrs['current_z'] = current_z

  for field in fields:
    data = data_snap[field]
    data_slice = data 
    # data_slice = data[slice_start:end, :, :] 
    outfile.create_dataset( field, data=data_slice )

  outfile.close()
  print( f'Saved File: {out_file_name}' )

