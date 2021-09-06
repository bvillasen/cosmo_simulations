import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools')
from tools import *
from load_data import Load_Skewers_File
from spectra_functions import Compute_Skewers_Transmitted_Flux
from flux_power_spectrum import Compute_Flux_Power_Spectrum


analysis_dir = data_dir + 'cosmo_sims/256_hydro_50Mpc/analysis_files/'
analysis_dir_0 = data_dir + 'cosmo_sims/256_hydro_50Mpc/analysis_files_0/'
input_dir = data_dir + 'cosmo_sims/256_hydro_50Mpc/skewers_files/'

n_file = 15


data_skewers = Load_Skewers_File( n_file, input_dir, fields_to_load=['density', 'HI_density', 'temperature', 'los_velocity'] )

# # Box parameters
# Lbox = data_skewers['Lbox'] #kpc/h
# box = {'Lbox':[ Lbox, Lbox, Lbox ] }
# 
# # Cosmology parameters
# cosmology = {}
# cosmology['H0'] = data_skewers['H0'] 
# cosmology['Omega_M'] = data_skewers['Omega_M']
# cosmology['Omega_L'] = data_skewers['Omega_L']
# cosmology['current_z'] = data_skewers['current_z']
# # 
# data_flux = Compute_Skewers_Transmitted_Flux( data_skewers, cosmology, box ) 
# data_ps = Compute_Flux_Power_Spectrum( data_flux )


for n_file in range(16):
  file_name = analysis_dir + f'{n_file}_analysis.h5'
  file = h5.File( file_name, 'r' )
  lya_stats = file['lya_statistics']

  F_mean = lya_stats.attrs['Flux_mean_HI']
  k_vals  = lya_stats['power_spectrum']['k_vals'][...]
  ps_mean = lya_stats['power_spectrum']['p(k)'][...]
  indices = ps_mean > 0
  k_vals = k_vals[indices]
  ps_mean = ps_mean[indices]


  file_name = analysis_dir_0 + f'{n_file}_analysis.h5'
  file = h5.File( file_name, 'r' )
  lya_stats = file['lya_statistics']

  F_mean_0 = lya_stats.attrs['Flux_mean_HI']
  k_vals_0  = lya_stats['power_spectrum']['k_vals'][...]
  ps_mean_0 = lya_stats['power_spectrum']['p(k)'][...]
  indices_0 = ps_mean_0 > 0
  k_vals_0 = k_vals_0[indices_0]
  ps_mean_0 = ps_mean_0[indices_0]
  
  print( ps_mean/ ps_mean_0 )


