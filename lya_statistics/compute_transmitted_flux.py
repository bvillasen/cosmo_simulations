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

use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

sim_dir  = data_dir + f'cosmo_sims/1024_25Mpc_fragmentation/cdm/'
input_dir  = sim_dir + f'skewers_files/'
output_dir = sim_dir + f'transmitted_flux/'
if rank == 0: create_directory( output_dir )


# Box parameters
Lbox = 25000.0 #kpc/h
box = {'Lbox':[ Lbox, Lbox, Lbox ] }


axis_list = [ 'x', 'y', 'z' ]
n_skewers_list = [ 'all', 'all', 'all']
skewer_ids_list = [ 'all', 'all', 'all']
field_list = [ 'density', 'HI_density', 'los_velocity', 'temperature' ]


files = np.array([ 25, 29, 33 ])
files_local = split_array_mpi( files, rank, n_procs )

print( f'rank: {rank}  files_local:{files_local}' )

for n_file in files_local:

  skewer_dataset = Load_Skewers_File( n_file, input_dir, axis_list=axis_list, fields_to_load=field_list )

  # Cosmology parameters
  cosmology = {}
  cosmology['H0'] = skewer_dataset['H0']
  cosmology['Omega_M'] = skewer_dataset['Omega_M']
  cosmology['Omega_L'] = skewer_dataset['Omega_L']
  cosmology['current_z'] = skewer_dataset['current_z']
  
  skewers_data = { field:skewer_dataset[field] for field in field_list }
  
  data_Flux = Compute_Skewers_Transmitted_Flux( skewers_data, cosmology, box )
  
  out_file_name = output_dir + f'lya_flux_{n_file:03}.h5'
  file = h5.File( out_file_name, 'w' )
  file.attrs['current_z'] = skewer_dataset['current_z']
  file.attrs['Flux_mean'] = data_Flux['Flux_mean']
  file.create_dataset( 'vel_Hubble', data=data_Flux['vel_Hubble'] )
  file.create_dataset( 'skewers_Flux', data=data_Flux['skewers_Flux'] )
  file.close()
  print( f'Saved File: {out_file_name}')