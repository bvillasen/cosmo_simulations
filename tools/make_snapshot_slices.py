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
root_dir = os.path.dirname(os.getcwd()) + '/'
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


n_wdm = 1.0
input_dir  = data_dir + f'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m{m_wdm:.1f}kev/snapshot_files/'
output_dir = data_dir + f'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m{m_wdm:.1f}kev/slices_gas_density/'
if rank == 0: create_directory( output_dir )
  
n_points = 1024
Lbox = 50000.0 #kpc/h
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_points, n_points, n_points ]
precision = np.float32
  
fields = [ 'density' ]
data_type = 'hydro'

slice_depth = 256
slice_id = 2
slice_start = slice_id * slice_depth
start = max( 0, slice_start )
end   = min( n_points, slice_start+slice_depth )
subgrid = [ [start, end], [0, n_points], [0, n_points] ]

snapshots = range( 1, 97 )
snapshot_ids = split_indices( snapshots, rank, nprocs )

for snap_id in snapshot_ids:
  n_snap = snapshots[snap_id]
  data_snap = load_snapshot_data_distributed( data_type, fields, n_snap, input_dir, box_size, grid_size,  precision, subgrid=subgrid, show_progess=show_progess )
  current_z = data_snap['Current_z']

  # print( f' Slice:  start:{start}   end:{end}' )

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

