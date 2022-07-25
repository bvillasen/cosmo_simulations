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
from spectra_functions import Compute_Skewers_Transmitted_Flux, Rescale_Optical_Depth_To_F_Mean
from flux_power_spectrum import Compute_Flux_Power_Spectrum

use_mpi = False
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

base_dir = data_dir + 'cosmo_sims/wdm_sims/compare_delta_z/'

# Box parameters
Lbox = 25000.0 #kpc/h
box = {'Lbox':[ Lbox, Lbox, Lbox ] }


axis_list = [ 'x', 'y', 'z' ]
n_skewers_list  = [ 'all', 'all', 'all']
skewer_ids_list = [ 'all', 'all', 'all']
field_list = [ 'HI_density', 'los_velocity', 'temperature' ]


sim_names = [ 'sim_0', 'sim_1', 'sim_2', 'sim_3', 'sim_4', 'sim_5', 'sim_6' ]
n_sim = len(sim_names)
delta_z_vals = [ -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75 ]

rescale_T0 = False

snap_ids =  [ 25, 29, 33 ]
for snap_id in snap_ids:

  for space in [ 'real', 'redshift']:

    reference_name = 'sim_3'
    sim_dir = base_dir + reference_name + '/'
    input_dir  = sim_dir + 'transmitted_flux/'
    
    in_file_name = input_dir + f'lya_flux_{space}_{snap_id:03}.h5'
    if rescale_T0: in_file_name = input_dir + f'lya_flux_{space}_{snap_id:03}_rescaled_T0.h5'
    file = h5.File( in_file_name, 'r' )
    z = file.attrs['current_z']
    reference_skewers_Flux = file['skewers_Flux'][...]
    file.close()
    reference_F_mean = reference_skewers_Flux.mean()

    for sim_name in sim_names:

      sim_dir = base_dir + sim_name + '/'
      input_dir  = sim_dir + 'transmitted_flux/'
      output_dir = sim_dir + 'transmitted_flux/'

      in_file_name = input_dir + f'lya_flux_{space}_{snap_id:03}.h5'
      if rescale_T0: in_file_name = input_dir + f'lya_flux_{space}_{snap_id:03}_rescaled_T0.h5'
      file = h5.File( in_file_name, 'r' )
      z = file.attrs['current_z']
      vel_Hubble = file['vel_Hubble'][...]
      skewers_Flux = file['skewers_Flux'][...]
      file.close()

      sim_F_mean = skewers_Flux.mean()

      flux_min = 1e-100
      skewers_Flux[ skewers_Flux < flux_min ] = flux_min
      skewers_tau = -np.log( skewers_Flux )
      skewers_tau_rescaled, alpha = Rescale_Optical_Depth_To_F_Mean( skewers_tau, reference_F_mean )
      skewers_Flux_rescaled = np.exp( - skewers_tau_rescaled )
      F_mean_rescaled = skewers_Flux_rescaled.mean()
      print( f'{sim_name}     Simulation: {sim_F_mean}   Reference: {reference_F_mean}   Rescaled:{F_mean_rescaled}' )

      out_file_name = input_dir + f'lya_flux_{space}_{snap_id:03}_rescaled_tau.h5'
      if rescale_T0: out_file_name = input_dir + f'lya_flux_{space}_{snap_id:03}_rescaled_T0_rescaled_tau.h5'
      file = h5.File( out_file_name, 'w' )
      file.attrs['current_z'] = z
      file.attrs['Flux_mean'] = F_mean_rescaled
      file.create_dataset( 'vel_Hubble', data=vel_Hubble )
      file.create_dataset( 'skewers_Flux', data=skewers_Flux_rescaled )
      file.close()
      print( f'Saved File: {out_file_name}')





