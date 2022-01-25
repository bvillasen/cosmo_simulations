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
  if rank == 0: print( 'Grid directory needed')
  exit(-1)


grid_dir = args[1]
skewers_dir = grid_dir + 'skewers_files/'
sim_dirs = [ d for d in os.listdir(skewers_dir) if d[0]=='S' ]
sim_dirs.sort()
n_sims = len( sim_dirs )

grid_files = {}
for sim_id,sim_dir in enumerate(sim_dirs):
  file_indices = [  int(f.split('_')[0]) for f in os.listdir(skewers_dir+sim_dir) if 'skewers.h5' in f ]
  file_indices.sort()
  n_files = len(file_indices)
  grid_files[sim_id] = { 'sim_dir':sim_dir, 'n_files':n_files, 'file_indices':file_indices }
  
n_files_per_sim = np.array([ grid_files[sim_id]['n_files'] for sim_id in grid_files ])
 
if rank == 0: 
  print( f'Grid  Dir: {grid_dir}' )
  print( f'Skewers Dir: {skewers_dir}' )
  print( f'N simulations: {n_sims}' )
  if ( n_files_per_sim == n_files_per_sim[0] ).all(): print( f'N files per sim (all): {n_files_per_sim[0]}')
  else: print( f'N files per sim: {n_files_per_sim} ')
  time.sleep(2)
if use_mpi: comm.Barrier()
# 
# snap_ids = [ int(f.split('_')[0]) for f in files ]
# snap_ids.sort()
# snap_ids = np.array(snap_ids)
# 
# 
# local_snaps = split_array_mpi( snap_ids, rank, n_procs )
# # print( f'proc_id: {rank}  snaps: {local_snaps}' )
# 
# # Box parameters
# Lbox = 50000.0 #kpc/h
# box = {'Lbox':[ Lbox, Lbox, Lbox ] }
# 
# 
# axis_list = [ 'x', 'y', 'z' ]
# n_skewers_list = [ 'all', 'all', 'all']
# skewer_ids_list = [ 'all', 'all', 'all']
# field_list = [  'HI_density', 'los_velocity', 'temperature' ]
# 
# for n_file in local_snaps:
# 
#   skewer_dataset = Load_Skewers_File( n_file, input_dir, axis_list=axis_list, fields_to_load=field_list )
# 
#   # Cosmology parameters
#   cosmology = {}
#   cosmology['H0'] = skewer_dataset['H0']
#   cosmology['Omega_M'] = skewer_dataset['Omega_M']
#   cosmology['Omega_L'] = skewer_dataset['Omega_L']
#   cosmology['current_z'] = skewer_dataset['current_z']
# 
#   skewers_data = { field:skewer_dataset[field] for field in field_list }
#   data_Flux = Compute_Skewers_Transmitted_Flux( skewers_data, cosmology, box )
# 
#   out_file_name = output_dir + f'lya_flux_{n_file:03}.h5'
#   file = h5.File( out_file_name, 'w' )
#   file.attrs['current_z'] = skewer_dataset['current_z']
#   file.attrs['Flux_mean'] = data_Flux['Flux_mean']
#   file.create_dataset( 'vel_Hubble', data=data_Flux['vel_Hubble'] )
#   file.create_dataset( 'skewers_Flux', data=data_Flux['skewers_Flux'] )
#   file.close()
#   print( f'Saved File: {out_file_name}')
# 
# 
# 
