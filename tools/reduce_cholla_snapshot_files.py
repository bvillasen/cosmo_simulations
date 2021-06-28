import sys, os, time
import numpy as np
import time
import h5py as h5
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

# print_out = False
print_out = True if rank == 0 else False

data_type = 'hydro'
# data_type = 'particles'

precision = np.float32

fields_hydro = [ 'density', 'temperature', 'HI_density', 'HeII_density', 'HeIII_density' ]
fields_particles = [ 'density' ]

if data_type == 'hydro': fields_list = fields_hydro
if data_type == 'particles': fields_list = fields_particles  
  
if data_type == 'hydro': file_name_base = '.h5'
if data_type == 'particles': file_name_base = '_particles.h5' 

data_dir = '/gpfs/alpine/csc434/proj-shared/cholla/'
root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim256/'
output_dir = data_dir + f'cosmo_sims/sim_grid/1024_P19m_np4_nsim256/reduced_snapshot_files_{data_type}/'
if rank == 0: create_directory( output_dir )



input_dir = root_dir + f'snapshot_files_{data_type}/'
simulations_dirs = os.listdir( input_dir ) 
simulations_dirs.sort()
n_sims = len( simulations_dirs )


snapshot_ids = range( 2, 17 )
files_per_snapshot = 128
local_files = split_indices( range(files_per_snapshot), rank, n_procs )

# for snapshot_id in snapshot_ids:
#   file_name = f'{snapshot_id}{file_name_base}.{0}'
#   in_file = h5.File( simulation_dir + file_name, 'r' )
#   z = in_file.attrs['Current_z'][0]
#   print( snapshot_id, z )

snapshots_to_copy = [ 3, 6, 8, 11, 14, 16 ]
n_snapshots = len( snapshots_to_copy )

time_start = time.time()

simulation_dir = input_dir + simulations_dirs[0] + '/'
dst_dir = output_dir + simulations_dirs[0] + '/'
if rank == 0: create_directory( dst_dir )
if print_out: 
  print( f'Copying: {simulation_dir}' ) 
  print( f'Destiny: {dst_dir}' )
if use_mpi: comm.Barrier()

n_snaps_copied = 0
for snapshot_id in snapshots_to_copy:
  if print_out: print( f' Copying snapshot: {snapshot_id}' )

  for file_id in local_files:

    file_name = f'{snapshot_id}{file_name_base}.{file_id}'
    in_file = h5.File( simulation_dir + file_name, 'r' )
    out_file = h5.File( dst_dir + file_name, 'w' )

    # Copy the header
    for key in in_file.attrs.keys():
      out_file.attrs[key] = in_file.attrs[key]

    # Copy the fields
    for field in fields_list:
      # print( f'  Copying Field: {field}')
      data = in_file[field][...].astype( precision )
      out_file.create_dataset( field, data=data )

    in_file.close()
    out_file.close()

  if use_mpi: comm.Barrier()
  n_snaps_copied += 1  

  if rank == 0: 
    files_copied = os.listdir( dst_dir )  
    if len( files_copied ) != n_snaps_copied * files_per_snapshot: 
      print(f'ERROR: Number of files in output dir is incorrect: {len(files_copied)}    {n_snaps_copied * files_per_snapshot}')
      exit(-1)
  
  if rank == 0: print_progress( n_snaps_copied, n_snapshots*n_sims, time_start )

if print_out:   print( '\nFinised Successfully')







