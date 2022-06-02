import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
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

if len( args ) < 2:
  if rank == 0: print( 'Input dir needed')
  exit(-1)

input_dir = args[1] 
flux_dir = input_dir + f'transmitted_flux/'
fps_dir = input_dir + f'flux_power_spectrum/'

input_dir += 'skewers_files/'
files = [ f for f in os.listdir(input_dir) if 'skewers' in f ]
n_files = len( files )

if rank == 0: create_directory( flux_dir )
if rank == 0: create_directory( fps_dir )
if rank == 0: 
  print( f'Input  Dir: {input_dir}')
  print( f'Flux Dir:   {flux_dir}')
  print( f'PS Dir:   {fps_dir}')
  print( f'N files: {n_files}')
  time.sleep(1)
if use_mpi: comm.Barrier()

snap_ids = [ int(f.split('_')[0]) for f in files ]
snap_ids.sort()
snap_ids = np.array(snap_ids)


local_snaps = split_array_mpi( snap_ids, rank, n_procs )
# print( f'proc_id: {rank}  snaps: {local_snaps}' )

# Box parameters
Lbox = 25000.0 #kpc/h
box = {'Lbox':[ Lbox, Lbox, Lbox ] }


axis_list = [ 'x', 'y', 'z' ]
n_skewers_list = [ 'all', 'all', 'all']
skewer_ids_list = [ 'all', 'all', 'all']
field_list = [  'HI_density', 'los_velocity', 'temperature' ]

for n_file in local_snaps:

  skewer_dataset = Load_Skewers_File( n_file, input_dir, axis_list=axis_list, fields_to_load=field_list )

  # Cosmology parameters
  cosmology = {}
  cosmology['H0'] = skewer_dataset['H0']
  cosmology['Omega_M'] = skewer_dataset['Omega_M']
  cosmology['Omega_L'] = skewer_dataset['Omega_L']
  cosmology['current_z'] = skewer_dataset['current_z']

  out_file_name = flux_dir + f'lya_flux_{n_file:03}.h5'
  file_exists = os.path.isfile( out_file_name )
  if not file_exists:
    
    skewers_data = { field:skewer_dataset[field] for field in field_list }
    data_Flux = Compute_Skewers_Transmitted_Flux( skewers_data, cosmology, box )

    file = h5.File( out_file_name, 'w' )
    file.attrs['current_z'] = skewer_dataset['current_z']
    file.attrs['Flux_mean'] = data_Flux['Flux_mean']
    file.create_dataset( 'vel_Hubble', data=data_Flux['vel_Hubble'] )
    file.create_dataset( 'skewers_Flux', data=data_Flux['skewers_Flux'] )
    file.close()
    print( f'Saved File: {out_file_name}')
    
  if file_exists:
    flux_file_name = out_file_name 
    print( f'Loading File: {flux_file_name}' )
    file = h5.File( flux_file_name, 'r' )
    current_z = file.attrs['current_z']
    Flux_mean = file.attrs['Flux_mean']
    vel_Hubble   = file['vel_Hubble'][...]
    skewers_Flux = file['skewers_Flux'][...]
    file.close()
    data_Flux = { 'vel_Hubble':vel_Hubble, 'skewers_Flux':skewers_Flux }
    
    data_ps = Compute_Flux_Power_Spectrum( data_Flux, print_string='', normalize_by_mean=False  )
    k_vals = data_ps['k_vals']
    skewers_ps = data_ps['skewers_ps']
    ps_mean = data_ps['mean']
    
    
    ps_file_name = fps_dir + f'flux_power_spectrum_{n_file:03}.h5'
    file = h5.File( ps_file_name, 'w' )
    file.attrs['current_z'] = current_z
    file.create_dataset( 'k_vals', data=data_ps['k_vals'] )
    file.create_dataset( 'ps_mean', data=data_ps['mean'] )
    file.create_dataset( 'skewers_ps', data=data_ps['skewers_ps'] )
    file.close()
    print( f'Saved File: {ps_file_name}' )


