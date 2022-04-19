import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from stats_functions import bootstrap_sample_mean, compute_covariance_matrix
from flux_power_spectrum import Compute_Flux_Power_Spectrum


use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

grid_dir = data_dir + 'cosmo_sims/sim_grid/grid_thermal/1024_P19m_np4_nsim400/'
input_dir = grid_dir + 'transmitted_flux/'
output_dir = grid_dir + 'pk_covariance/'
create_directory(output_dir)

sim_dirs = [ f for f in os.listdir(input_dir) if f[0]=='S' ]
sim_dirs.sort()

indices = np.arange( 0, len(sim_dirs), 1, dtype=int )
indices_local = split_array_mpi( indices, rank, n_procs )
print( f'rank{rank} indices_local: {indices_local} ')

for sim_id in indices_local:
  sim_dir = sim_dirs[sim_id]
  out_sim_dir = output_dir + f'{sim_dir}/'
  create_directory( out_sim_dir )

  files = range( 25, 56)

  for n_file in files:
    file_name = input_dir + f'{sim_dir}/lya_flux_{n_file:03}.h5'
    print( f'Loading File: {file_name}' )
    file = h5.File( file_name, 'r' )
    current_z = file.attrs['current_z']
    Flux_mean = file.attrs['Flux_mean']
    vel_Hubble = file['vel_Hubble'][...]
    skewers_Flux = file['skewers_fflux'][...]
    k_vals = file['power_spectrum']['k_vals'][...]
    ps_mean = file['power_spectrum']['ps_mean'][...]
    indices = ps_mean > 0 
    k_vals = k_vals[indices]
    ps_mean = ps_mean[indices]
    file.close()

    data_Flux = { 'vel_Hubble':vel_Hubble, 'skewers_Flux':skewers_Flux }
    data_ps = Compute_Flux_Power_Spectrum( data_Flux )
    k_vals = data_ps['k_vals']
    skewers_ps = data_ps['skewers_ps']

    cov_matrix = compute_covariance_matrix( skewers_ps )
    sigma = np.sqrt( cov_matrix.diagonal() )
    data_covariance = { 'k_vals':k_vals, 'covariance_matrix': cov_matrix, 'sigma':sigma, 'current_z':current_z, 'ps_mean':ps_mean }

    file_name = out_sim_dir + f'covariance_{n_file:03}.pkl'
    Write_Pickle_Directory( data_covariance, file_name )
