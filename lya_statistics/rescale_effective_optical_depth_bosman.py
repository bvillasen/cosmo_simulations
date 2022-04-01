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
from data_optical_depth import data_optical_depth_Bosman_2021, data_optical_depth_Bosman_2018


def Rescale_Optical_Depth_To_F_Mean_Diff( alpha, F_mean, tau_los  ):
  # print(alpha)
  tau_los_rescaled = tau_los * alpha
  F_los_rescaled = np.exp( - tau_los_rescaled )
  F_mean_rescaled = F_los_rescaled.mean()
  diff = F_mean_rescaled - F_mean
  return diff

def Rescale_Optical_Depth_To_F_Mean( tau_los, F_mean ):
  from scipy import optimize
  tau_eff = -np.log( F_mean )
  guess = tau_eff / tau_los.mean()
  alpha = optimize.newton(Rescale_Optical_Depth_To_F_Mean_Diff, guess, args=(F_mean, tau_los ) ) 
  tau_los_rescaled = alpha * tau_los
  F_los_rescaled = np.exp( - tau_los_rescaled )
  F_mean_rescaled = F_los_rescaled.mean()
  diff = np.abs( F_mean_rescaled - F_mean ) / F_mean
  if diff > 1e-6: print( 'WARNING: Rescaled F_mean mismatch: {F_mean_rescaled}   {f_mean}')
  return  tau_los_rescaled, alpha


sim_dir  = data_dir + f'cosmo_sims/1024_50Mpc_V22/'
input_dir = sim_dir + 'skewers_files/transmitted_flux/'
output_dir = sim_dir
create_directory( output_dir )


flux_min = 1e-100
data_sims = {}
for snap_id, n_file in enumerate(range(9,30)):
  file_name = input_dir + f'lya_flux_{n_file:03}.h5'
  print( f'Loding File: {file_name}' )
  file = h5.File( file_name, 'r' )
  current_z = file.attrs['current_z']
  F_mean = file.attrs['Flux_mean'] 
  vel_Hubble = file['vel_Hubble'][...]
  skewers_Flux = file['skewers_Flux'][...]
  skewers_Flux[skewers_Flux < flux_min] = flux_min
  data_sims[snap_id] = { 'z':current_z, 'skewers_Flux':skewers_Flux }

z_sims = np.array([ data_sims[i]['z'] for i in data_sims ])


data = data_optical_depth_Bosman_2018
data_z = data['z']
data_tau = data['tau']
data_tau_sigma = data['tau_sigma']
data_tau_p = data_tau + data_tau_sigma 
data_tau_l = data_tau - data_tau_sigma 
data_F_mean = np.exp( -data_tau_p )

z_vals, alpha_vals = [], []
for z, F_mean  in zip(data_z, data_F_mean):
  # print( z, F_mean)
  diff = np.abs( z_sims - z )
  id = np.where( diff == diff.min() )[0][0]
  data_sim = data_sims[id]
  z_sim = data_sim['z']
  if np.abs( z_sim - z ) > 0.01: print( f'ERROR: Redshift mismatch: z:{z}  z_sim:{z_sim}')
  skewers_flux = data_sim['skewers_Flux']
  skewers_tau = -np.log(skewers_flux)
  skewers_tau_rescaled, alpha = Rescale_Optical_Depth_To_F_Mean( skewers_tau, F_mean )
  print(z, alpha)
  z_vals.append( z )
  alpha_vals.append( alpha )
 
data_out = np.array([ z_vals, alpha_vals ]).T
# file_name = output_dir + 'rescale_tau_to_Bosman_2021.txt'
# file_name = output_dir + 'rescale_tau_to_Bosman_2021_higher.txt'
# file_name = output_dir + 'rescale_tau_to_Bosman_2021_lower.txt'
# file_name = output_dir + 'rescale_tau_to_Bosman_2018.txt'
# file_name = output_dir + 'rescale_tau_to_Bosman_2018_lower.txt'
file_name = output_dir + 'rescale_tau_to_Bosman_2018_higher.txt'
np.savetxt( file_name, data_out )
print( f'Saved File: {file_name}' )  
