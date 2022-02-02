import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from stats_functions import bootstrap_sample_mean, compute_covariance_matrix
from load_tabulated_data import load_tabulated_data_boera 

ps_data_dir = root_dir + 'lya_statistics/data/'
data_boera_dir = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_tabulated_data_boera( data_boera_dir )
k_vals_boera = data_boera[0]['k_vals']


args = sys.argv

use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

# if len( args ) < 2:
#   if rank == 0: print( 'Grid directory needed')
#   exit(-1)

  
print_out = False
if rank == 0: print_out = True

# grid_dir = args[1]
grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_nsim600'
if grid_dir[-1] != '/': grid_dir += '/'
ps_dir = grid_dir + 'flux_power_spectrum/'
analysis_dir = grid_dir + 'analysis_files/'

selected_file_indices = [ 25, 29, 33 ] # redshits 5.0, 4.6 and 4.2

bootstrap = False


sim_dirs = [ d for d in os.listdir(ps_dir) if d[0]=='S' ]
sim_dirs.sort()
indices = np.arange( 0, len(sim_dirs), 1, dtype=int )
indices_local = split_array_mpi( indices, rank, n_procs )
print( f'rank{rank} indices_local: {indices_local} ')

data_name = 'sampled_boera_native'

for sim_id in indices_local:
  sim_dir = sim_dirs[sim_id]

  for file_indx in selected_file_indices:
    # Load the skewers power spectrum
    # ps_file_name = ps_dir + f'{sim_dir}/flux_ps_{file_indx:03}.h5'
    ps_file_name = ps_dir + f'{sim_dir}/flux_ps_{data_name}_{file_indx:03}.h5'
    ps_file = h5.File( ps_file_name, 'r' )
    current_z = ps_file.attrs['current_z']
    k_vals = ps_file['k_vals'][...]
    ps_mean = ps_file['ps_mean'][...]
    skewers_ps = ps_file['skewers_ps'][...]
    ps_file.close()
    
    mean_ps = skewers_ps.mean( axis=0 )
    mean_diff = np.abs( mean_ps - ps_mean) / ps_mean
    if ( mean_diff > 1e-6 ).any(): 
      print( 'ERROR: P(k) mean mismatch from file' )
      exit(-1)
    
    # Interpolate P(k) to boera
    # print( f'Resampling power spectrum' )
    # k_vals_resample = k_vals_boera
    # skewers_ps_resampled = np.array([ np.interp( k_vals_boera, k_vals, skewer_ps ) for skewer_ps in skewers_ps ])
    # k_vals = k_vals_resample
    # skewers_ps = skewers_ps_resampled
    
    data_covariance = {}
    if bootstrap:
      n_iterations = 10000
      samples = [ 50, 100, 500, 1000 ]
      for data_id, n_in_sample in enumerate(samples):
        bootstrap_samples = bootstrap_sample_mean( n_iterations, n_in_sample, skewers_ps, print_out )
        cov_matrix = compute_covariance_matrix( bootstrap_samples )
        sigma = np.sqrt( cov_matrix.diagonal() )
        data_covariance[data_id] = { 'n_in_sample':n_in_sample, 'k_vals':k_vals, 'bootstrap_samples':bootstrap_samples, 'covariance_matrix': cov_matrix, 'sigma':sigma }
    
    else:
      cov_matrix = compute_covariance_matrix( skewers_ps )
      sigma = np.sqrt( cov_matrix.diagonal() )
      data_covariance = { 'k_vals':k_vals, 'covariance_matrix': cov_matrix, 'sigma':sigma, 'current_z':current_z, 'ps_mean':ps_mean }
  

    if bootstrap:file_name = ps_dir + f'{sim_dir}/bootstrap_statistics_{data_name}_{file_indx:03}.pkl'
    else: file_name = ps_dir + f'{sim_dir}/statistics_{data_name}_{file_indx:03}.pkl'
    # if bootstrap:file_name = ps_dir + f'{sim_dir}/bootstrap_statistics_{file_indx:03}.pkl'
    # else: file_name = ps_dir + f'{sim_dir}/statistics_{file_indx:03}.pkl'
    Write_Pickle_Directory( data_covariance, file_name )


