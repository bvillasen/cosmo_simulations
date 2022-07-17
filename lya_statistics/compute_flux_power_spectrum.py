import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import Load_Skewers_File, load_analysis_data
from calculus_functions import *
from stats_functions import compute_distribution
from data_optical_depth import data_optical_depth_Bosman_2021
from load_skewers import load_skewers_multiple_axis
from spectra_functions import Compute_Skewers_Transmitted_Flux
from flux_power_spectrum import Compute_Flux_Power_Spectrum
from constants_cosmo import Mpc, Myear, Gcosmo, Msun, kpc
from cosmology import Cosmology


use_mpi = False
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

sim_dir  = data_dir + f'cosmo_sims/1024_25Mpc_fragmentation/cdm/'
input_dir = sim_dir + f'transmitted_flux/'
output_dir = sim_dir + f'flux_power_spectrum/'
if rank == 0: create_directory( output_dir )


# Box parameters
Lbox = 25000.0 #kpc/h
box = {'Lbox':[ Lbox, Lbox, Lbox ] }

files_local = [ 25, 29, 33 ]

for n_file in files_local:

  in_file_name = input_dir + f'lya_flux_{n_file:03}_delta_max_10.h5'
  # in_file_name = input_dir + f'lya_flux_{n_file:03}.h5'
  print( f'Loading File: {in_file_name}')
  file = h5.File( in_file_name, 'r' )
  current_z = file.attrs['current_z']
  vel_Hubble = file['vel_Hubble'][...]
  skewers_Flux = file['skewers_Flux'][...]
  file.close()

  data_Flux = { 'vel_Hubble':vel_Hubble, 'skewers_Flux':skewers_Flux }


  data_ps = Compute_Flux_Power_Spectrum( data_Flux )
  k_vals = data_ps['k_vals']
  skewers_ps = data_ps['skewers_ps']
  ps_mean = data_ps['mean']

  out_file_name = output_dir + f'flux_ps_{n_file:03}_delta_max_10.h5'
  # out_file_name = output_dir + f'flux_ps_{n_file:03}.h5'
  file = h5.File( out_file_name, 'w' )
  file.attrs['current_z'] = current_z
  file.create_dataset( 'k_vals', data=data_ps['k_vals'] )
  file.create_dataset( 'ps_mean', data=data_ps['mean'] )
  file.create_dataset( 'skewers_ps', data=data_ps['skewers_ps'] )
  file.close()
  print( f'Saved File: {out_file_name}' )

