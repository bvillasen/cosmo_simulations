import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from spectra_functions import Rescale_Optical_Depth_To_F_Mean
from flux_power_spectrum import Compute_Flux_Power_Spectrum

data_dir = '/raid/bruno/data/'
input_dir  = data_dir + f'cosmo_sims/rescaled_P19/2048_50Mpc/skewers/transmitted_flux_new/'
output_dir = data_dir + f'cosmo_sims/rescaled_P19/2048_50Mpc/skewers/rescaled_power_spectrum_new/'
create_directory( output_dir )

flux_min = 1e-100

files = [ 90, 106, 130, 169 ] 

for n_file in files:
  file_name = input_dir + f'lya_flux_{n_file:03}.h5'
  print( f'Loading File: {file_name}' )
  file = h5.File( file_name, 'r' )
  current_z = file.attrs['current_z']
  print( f'current_z: {current_z}')
  Flux_mean = file.attrs['Flux_mean']
  vel_Hubble = file['vel_Hubble'][...]
  skewers_Flux = file['skewers_Flux'][...]
  file.close()
  skewers_Flux[skewers_Flux < flux_min] = flux_min
  data_Flux = { 'vel_Hubble':vel_Hubble, 'skewers_Flux':skewers_Flux }
  data_ps_original = Compute_Flux_Power_Spectrum( data_Flux )


  data_out = {}
  data_out['z'] = current_z
  data_out['original'] = { 'k_vals': data_ps_original['k_vals'], 'ps_mean':data_ps_original['mean']}

  ps_rescaled = {}
  alpha_vals = [ -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3 ]
  for data_id, alpha in enumerate(alpha_vals):
    print( f'\nalpha: {alpha}' )
    skewers_flux = skewers_Flux.copy()
    flux_mean = skewers_flux.mean()
    skewers_tau = -np.log(skewers_flux)
    tau_eff = -np.log( flux_mean ) 
    rescaled_tau_eff = ( 1 + alpha ) * tau_eff
    rescaled_F_mean = np.exp( - rescaled_tau_eff )
    skewers_tau_rescaled, rescale_factor = Rescale_Optical_Depth_To_F_Mean( skewers_tau, rescaled_F_mean )
    skewers_flux_rescaled = np.exp( -skewers_tau_rescaled )
    data_Flux_rescaled = { 'vel_Hubble':vel_Hubble, 'skewers_Flux':skewers_flux_rescaled }
    data_ps_rescaled = Compute_Flux_Power_Spectrum( data_Flux_rescaled )
    k_vals = data_ps_rescaled['k_vals']
    ps_mean = data_ps_rescaled['mean']
    ps_rescaled[data_id] = { 'alpha':alpha, 'rescale_factor':rescale_factor, 'k_vals':k_vals, 'ps_mean':ps_mean  }
    
  data_out['rescaled'] = ps_rescaled  
  file_name = output_dir + f'rescaled_ps_{n_file}.pkl'
  Write_Pickle_Directory( data_out, file_name )
    