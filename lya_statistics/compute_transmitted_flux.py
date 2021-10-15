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

data_dir = '/raid/bruno/data/'
input_dir  = data_dir + f'cosmo_sims/rescaled_P19/2048_50Mpc/skewers/'
output_dir = data_dir + f'cosmo_sims/rescaled_P19/2048_50Mpc/skewers/transmitted_flux_new/'
if rank == 0: create_directory( output_dir )

z_vals_all = []
n_start, n_end = 74, 170
for n_file in range(n_start, n_end ):
  file_name = input_dir + f'skewers_x_{n_file}.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  file.close()
  z_vals_all.append( z )
z_vals_all = np.array( z_vals_all )

z_vals = [ 5.0, 4.0, 3.0, 2.0 ]

z_indx = rank
z_val = z_vals[z_indx]
diff = np.abs( z_vals_all - z_val )
if diff.min() > 1e-2:
  print('ERROR: Large redshift difference')
  exit()
n_file = np.where( diff == diff.min() )[0][0] + n_start
  




# Box parameters
Lbox = 50000.0 #kpc/h
nPoints = 2048
nx = nPoints
ny = nPoints
nz = nPoints
ncells = nx * ny * nz
box = {'Lbox':[ Lbox, Lbox, Lbox ] }

# Cosmology parameters
cosmology = {}
cosmology['H0'] = 67.66 
cosmology['Omega_M'] = 0.3111
cosmology['Omega_L'] = 0.6889

axis_list = [ 'x', 'y', 'z' ]
n_skewers_list = [ 'all', 'all', 'all']
skewer_ids_list = [ 'all', 'all', 'all']
# n_skewers_list = [ 500, 500, 500]
# skewer_ids_list = [ 'random', 'random', 'random']
field_list = [ 'density', 'HI_density', 'los_velocity', 'temperature' ]


skewer_dataset = load_skewers_multiple_axis( axis_list, n_skewers_list, n_file, input_dir, ids_to_load_list=skewer_ids_list) 
current_z = skewer_dataset['current_z']
print( f'current_z: {current_z}')
cosmology['current_z'] = current_z
skewers_data = { field:skewer_dataset[field] for field in field_list }
data_Flux = Compute_Skewers_Transmitted_Flux( skewers_data, cosmology, box )

out_file_name = output_dir + f'lya_flux_{n_file:03}.h5'
file = h5.File( out_file_name, 'w' )
file.attrs['current_z'] = current_z
file.attrs['Flux_mean'] = data_Flux['Flux_mean']
file.create_dataset( 'vel_Hubble', data=data_Flux['vel_Hubble'] )
file.create_dataset( 'skewers_Flux', data=data_Flux['skewers_Flux'] )
file.close()
print( f'Saved File: {out_file_name}')



