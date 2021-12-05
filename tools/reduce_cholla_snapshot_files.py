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

verify_output_number = True

precision = np.float32

fields_hydro = [ 'density'  ]
fields_particles = [ 'density' ]

if data_type == 'hydro': fields_list = fields_hydro
if data_type == 'particles': fields_list = fields_particles  
  
if data_type == 'hydro': file_name_base = '.h5'
if data_type == 'particles': file_name_base = '_particles.h5' 

root_dir = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m0.5kev/'
input_dir  = root_dir + f'snapshot_files/'
output_dir = root_dir + f'reduced_snapshots_{data_type}_density/'
if rank == 0: create_directory( output_dir )


snapshot_ids = range( 97 )
files_per_snapshot = 16
local_files = split_indices( range(files_per_snapshot), rank, n_procs )
n_snapshots = len( snapshot_ids )
print( f'proc_id: {rank}  local_files: {local_files}'  )
# 
# time_start = time.time()
# n_snaps_copied = 0
# for snapshot_id in snapshot_ids:
# 
#   for file_id in local_files:
# 
#     file_name = f'{snapshot_id}{file_name_base}.{file_id}'
#     in_file = h5.File( input_dir + file_name, 'r' )
#     out_file = h5.File( output_dir + file_name, 'w' )
# 
#     # Copy the header
#     for key in in_file.attrs.keys():
#       out_file.attrs[key] = in_file.attrs[key]
# 
#     # Copy the fields
#     for field in fields_list:
#       # print( f'  Copying Field: {field}')
#       data = in_file[field][...].astype( precision )
#       out_file.create_dataset( field, data=data )
# 
#     in_file.close()
#     out_file.close()
# 
#   if use_mpi: comm.Barrier()
#   n_snaps_copied += 1  
# 
#   if rank == 0 and verify_output_number: 
#     files_copied = os.listdir( output_dir )  
#     if len( files_copied ) != n_snaps_copied * files_per_snapshot: 
#       print(f'ERROR: Number of files in output dir is incorrect: {len(files_copied)}    {n_snaps_copied * files_per_snapshot}')
#       exit(-1)
# 
#   if rank == 0: print_progress( n_snaps_copied, n_snapshots, time_start )
# 
# if print_out:   print( '\nFinised Successfully')
# 
