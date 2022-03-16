import sys, os, time
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
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

grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
fit_name = 'fit_results_covariance_systematic'
input_dir = grid_dir + f'fit_mcmc/{fit_name}/thermal/'
output_dir = grid_dir + f'fit_mcmc/{fit_name}/thermal_merged/'
if rank == 0: create_directory( output_dir )

n_files = 400000
if rank == 0:print( f'N files: {n_files}')

ids_global = np.arange(0, n_files, 1, dtype=int)
ids_local = split_array_mpi( ids_global, rank, n_procs )
n_local = len( ids_local )
print( f'proc_id: {rank}  n_local: {n_local}' )
selected_files = ids_local
n_samples = len( selected_files )

comm.Barrier()

out_file_name = output_dir + f'samples_T0_evolution_id_{rank}.h5'
file_exits = os.path.isfile(out_file_name)

if not file_exits:
  
  z_vals = None
  T0_vals = []
  x_HI_vals, x_HeII_vals, n_e_vals = [], [], []
  time_start = time.time()
  for sim_id,file_id in enumerate(selected_files):
    file_name = input_dir + f'solution_{file_id}.h5'
    file = h5.File( file_name, 'r' )
    if z_vals is None: z_vals = file['z'][...]
    T0 = file['temperature'][...]
    n_H  = file['n_H'][...]
    n_HI = file['n_HI'][...]
    # n_He  = file['n_He'][...]
    # n_HeII = file['n_HeII'][...]
    n_e  = file['n_e'][...]
    file.close()
    x_HI = n_HI / n_H
    # x_HeII = n_HeII / n_He
    
    T0_vals.append( T0 )
    x_HI_vals.append( x_HI )
    # x_HeII_vals.append( x_HeII )
    n_e_vals.append( n_e )
    if sim_id %100 == 0: print_progress( sim_id, n_samples, time_start )
  print('\n')
  T0_vals = np.array( T0_vals )
  x_HI_vals = np.array( x_HI_vals )
  # x_HeII_vals = np.array( x_HeII_vals )
  n_e_vals = np.array( n_e_vals )

  out_file = h5.File( out_file_name, 'w' )
  out_file.create_dataset('selected_files', data=selected_files )
  out_file.create_dataset( 'z', data=z_vals )
  out_file.create_dataset( 'T0', data=T0_vals )
  out_file.create_dataset( 'x_HI', data=x_HI_vals )
  # out_file.create_dataset( 'x_HeII', data=x_HeII_vals )
  out_file.create_dataset( 'n_e', data=n_e_vals )
  out_file.close()
  print( f'Saved File: {out_file_name}' )

comm.Barrier()
if rank != 0: exit(0) 

selected_files_all = []
T0_vals_all = []
x_HI_vals_all = []
# x_HeII_vals_all = []
n_e_vals_all = []
for file_id in range(n_procs):  
  in_file_name = output_dir + f'samples_T0_evolution_id_{file_id}.h5'
  print( f'Loading File: {in_file_name}' )
  in_file = h5.File( in_file_name, 'r')
  z_vals = in_file['z'][...]
  selected_files = in_file['selected_files'][...]
  T0 = in_file['T0'][...]
  x_HI = in_file['x_HI'][...]
  # x_HeII = in_file['x_HeII'][...]
  n_e = in_file['n_e'][...]
  in_file.close()
  T0_vals_all.append(T0)
  x_HI_vals_all.append(x_HI)
  # x_HeII_all.append(x_HeII)
  n_e_vals_all.append(n_e)
  selected_files_all.append( selected_files )
  
selected_files_all = np.concatenate( selected_files_all )
selected_files_all.sort()
n_files = len( selected_files_all )
files_ids = np.arange( 0, n_files, 1, dtype=int)
file_diff = np.abs( files_ids - selected_files_all).sum()
print( f'file_diff: {file_diff}' ) 
T0_vals_all = np.concatenate( T0_vals_all, axis=0 )
x_HI_vals_all = np.concatenate( x_HI_vals_all, axis=0 )
# x_HeII_vals_all = np.concatenate( x_HeII_vals_all, axis=0 )
n_e_vals_all = np.concatenate( n_e_vals_all, axis=0 )
print( f'T0 shape: {T0_vals_all.shape}')
print( f'x_HI shape: {x_HI_vals_all.shape}')
# print( f'x_HeII shape: {x_HeII_vals_all.shape}')
print( f'n_e shape: {n_e_vals_all.shape}')
  
output_dir = grid_dir + f'fit_mcmc/{fit_name}/'
out_file_name = output_dir + f'samples_thermal_evolution.h5'
out_file = h5.File( out_file_name, 'w' )
out_file.create_dataset( 'z', data=z_vals )
out_file.create_dataset( 'T0', data=T0_vals_all )
out_file.create_dataset( 'x_HI', data=x_HI_vals_all )
# out_file.create_dataset( 'x_HeII', data=x_HeII_vals_all )
out_file.create_dataset( 'n_e', data=n_e_vals_all )
out_file.close()
print( f'Saved File: {out_file_name}' )
