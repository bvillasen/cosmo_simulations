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

use_mpi = False
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

compute_ps = True
  
print_out = False
if rank == 0: print_out = True

grid_dir = args[1]
if grid_dir[-1] != '/': grid_dir += '/'
skewers_dir = grid_dir + 'skewers_files/'
transmitted_flux_dir = grid_dir + 'transmitted_flux/'
ps_dir = grid_dir + 'flux_power_spectrum/'
analysis_dir = grid_dir + 'analysis_files/'
grid_skewers_file_name = grid_dir + 'grid_skewers_files.pkl'

selected_file_indices = [ 25, 29, 33 ] # redshits 5.0, 4.6 and 4.2

if rank == 0: 
  print( f'Loading Grid: {grid_dir}')

  sim_dirs = [ d for d in os.listdir(skewers_dir) if d[0]=='S' ]
  sim_dirs.sort()
  n_sims = len( sim_dirs )

  grid_files = {}
  for sim_id,sim_dir in enumerate(sim_dirs):
    if selected_file_indices is not None: file_indices = selected_file_indices
    else: file_indices = [  int(f.split('_')[0]) for f in os.listdir(skewers_dir+sim_dir) if 'skewers.h5' in f ]
    file_indices.sort()
    n_files = len(file_indices)
    grid_files[sim_id] = { 'sim_dir':sim_dir, 'n_files':n_files, 'file_indices':file_indices }
    
  n_files_per_sim = np.array([ grid_files[sim_id]['n_files'] for sim_id in grid_files ])   
  print( f'Skewers Dir: {skewers_dir}' )
  print( f'N simulations: {n_sims}' )
  if ( n_files_per_sim == n_files_per_sim[0] ).all(): print( f'N files per sim (all): {n_files_per_sim[0]}')
  else: print( f'N files per sim: {n_files_per_sim} ')
  
  skewers_files_data = {}
  file_id = 0
  for sim_id in grid_files:
    sim_dir = grid_files[sim_id]['sim_dir']
    file_indices = grid_files[sim_id]['file_indices']
    for file_indx in file_indices:
      file_name = f'{skewers_dir}{sim_dir}/{file_indx}_skewers.h5'
      is_file = os.path.isfile( file_name )
      if not is_file: print(f'ERROR: File not found {file_name}' )
      skewers_files_data[file_id] = { 'sim_id': sim_id, 'sim_dir':sim_dir, 'file_indx':file_indx, 'file_name':file_name }
      file_id += 1
  
  n_total_files = file_id
  print( f'N total files: {n_total_files}') 
  Write_Pickle_Directory( skewers_files_data, grid_skewers_file_name )
  
  print('Creating Transmitted Flux Directories')
  if not os.path.isdir( transmitted_flux_dir ): create_directory( transmitted_flux_dir )
  for sim_dir in sim_dirs:
    dir = transmitted_flux_dir + sim_dir
    if os.path.isdir( dir ): continue
    create_directory( dir )
  
  if compute_ps:
    print('Creating Flux Power Spectrum Directories')
    if not os.path.isdir( ps_dir ): create_directory( ps_dir )
    for sim_dir in sim_dirs:
      dir = ps_dir + sim_dir
      if os.path.isdir( dir ): continue
      create_directory( dir )

if use_mpi: comm.Barrier()
skewers_files_data = Load_Pickle_Directory( grid_skewers_file_name, print_out=print_out )
file_indices = np.array([ file_id for file_id in skewers_files_data ])
n_total_files = len( file_indices )
local_indices = split_array_mpi( file_indices, rank, n_procs )

# Box parameters
Lbox = 50000.0 #kpc/h
box = {'Lbox':[ Lbox, Lbox, Lbox ] }

axis_list = [ 'x', 'y', 'z' ]
n_skewers_list = [ 'all', 'all', 'all']
skewer_ids_list = [ 'all', 'all', 'all']
field_list = [  'HI_density', 'los_velocity', 'temperature' ]

for file_id in local_indices:
    
  file_data = skewers_files_data[file_id]
  sim_dir = file_data['sim_dir']
  file_indx = file_data['file_indx']
  input_dir = skewers_dir + sim_dir + '/'
  flux_dir = transmitted_flux_dir + sim_dir + '/'
  if not os.path.isdir(input_dir):
    print( f'ERROR: Directory not found {input_dir}' )
    continue  
  if not os.path.isdir(flux_dir):
    print( f'ERROR: Directory not found {flux_dir}' )
    continue  
    
  print_string = f'  file  {file_id:04} / {n_total_files}.  '
  
  flux_file_name = flux_dir + f'lya_flux_{file_indx:03}.h5'
  flux_file_exists = False
  if os.path.isfile( flux_file_name ):  flux_file_exists = True
  if flux_file_exists: continue
    
  skewer_dataset = Load_Skewers_File( file_indx, input_dir, axis_list=axis_list, fields_to_load=field_list )
  current_z = skewer_dataset['current_z']
  
  # Cosmology parameters
  cosmology = {}
  cosmology['H0'] = skewer_dataset['H0']
  cosmology['Omega_M'] = skewer_dataset['Omega_M']
  cosmology['Omega_L'] = skewer_dataset['Omega_L']
  cosmology['current_z'] = skewer_dataset['current_z']

  skewers_data = { field:skewer_dataset[field] for field in field_list }
  data_Flux = Compute_Skewers_Transmitted_Flux( skewers_data, cosmology, box, print_string=print_string )
  
  file = h5.File( flux_file_name, 'w' )
  file.attrs['current_z'] = current_z
  file.attrs['Flux_mean'] = data_Flux['Flux_mean']
  file.create_dataset( 'vel_Hubble', data=data_Flux['vel_Hubble'] )
  file.create_dataset( 'skewers_Flux', data=data_Flux['skewers_Flux'] )
  file.close()
  # print( f'Saved File: {out_file_name}')

if use_mpi: comm.Barrier()
if rank == 0: print('')

# Now compute the flux power spectrum
for file_id in local_indices:
  if not compute_ps: continue
    
  file_data = skewers_files_data[file_id]
  sim_dir = file_data['sim_dir']
  file_indx = file_data['file_indx']
  flux_dir = transmitted_flux_dir + sim_dir + '/'
  ps_sim_dir = ps_dir + sim_dir + '/'
  print_string = f'  file  {file_id:04} / {n_total_files}.  '
  
  flux_file_name = flux_dir + f'lya_flux_{file_indx:03}.h5'      
  file = h5.File( flux_file_name, 'r' )
  current_z = file.attrs['current_z']
  Flux_mean = file.attrs['Flux_mean']
  vel_Hubble   = file['vel_Hubble'][...]
  skewers_Flux = file['skewers_Flux'][...]
  file.close()
  data_Flux = { 'vel_Hubble':vel_Hubble, 'skewers_Flux':skewers_Flux }

  ps_file_name = ps_sim_dir + f'flux_ps_{file_indx:03}.h5'
  ps_file_exists = False
  if os.path.isfile( ps_file_name ):  ps_file_exists = True
  if ps_file_exists: continue
  
  data_ps = Compute_Flux_Power_Spectrum( data_Flux, print_string=print_string )
  file = h5.File( ps_file_name, 'w' )
  file.attrs['current_z'] = current_z
  file.create_dataset( 'k_vals', data=data_ps['k_vals'] )
  file.create_dataset( 'ps_mean', data=data_ps['mean'] )
  file.create_dataset( 'skewers_ps', data=data_ps['skewers_ps'] )
  file.close()

if use_mpi: comm.Barrier()
if rank != 0: exit()

# Now compare the Power Spectrum to the one computed in-the-fly
for file_id in file_indices:
  if not compute_ps: continue
    
  file_data = skewers_files_data[file_id]
  sim_dir = file_data['sim_dir']
  file_indx = file_data['file_indx']
  ps_sim_dir = ps_dir + sim_dir + '/'
  analysis_sim_dir = analysis_dir + sim_dir + '/'
  print_string = f'  file  {file_id:04} / {n_total_files}.  '

  ps_file_name = ps_sim_dir + f'flux_ps_{file_indx:03}.h5'
  file = h5.File( ps_file_name, 'r' )
  current_z = file.attrs['current_z']
  k_vals = file['k_vals'][...] 
  ps_mean = file['ps_mean'][...]
  file.close()
  
  analysis_file_name = analysis_dir + f'{file_indx}_analysis.h5'
  file = h5.File( analysis_file_name, 'r' )
  
  
  
  break
  
  
