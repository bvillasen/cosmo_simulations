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


data_dir = '/raid/bruno/data/'
input_dir  = data_dir + f'cosmo_sims/rescaled_P19/1024_50Mpc_high_z/'
output_dir = data_dir + f'cosmo_sims/rescaled_P19/1024_50Mpc_high_z/neutral_fraction/'
create_directory( output_dir )

flux_min = 1e-100
data_sims = {}
for n_file in range(17):
  data = load_analysis_data( n_file, input_dir+'analysis_files/', phase_diagram=False, lya_statistics=True )
  skewers_data = Load_Skewers_File( n_file, input_dir+'skewers_files/', chem_type = 'HI', axis_list = [ 'x', 'y', 'z' ] )
  current_z = skewers_data['current_z']
  vel_Hubble = skewers_data['vel_Hubble']
  dv = vel_Hubble[1] - vel_Hubble[0] 
  skewers_flux = skewers_data['skewers_flux_HI']
  skewers_flux[skewers_flux < flux_min] = flux_min
  data_sims[n_file] = { 'z':current_z, 'skewers_flux':skewers_flux }
  
z_sims = np.array([ data_sims[i]['z'] for i in data_sims ])



data = data_optical_depth_Bosman_2021
data_z = data['z']
data_tau = data['tau']
data_F_mean = np.exp( -data_tau )

z_vals, alpha_vals = [], []
for z, F_mean  in zip(data_z, data_F_mean):
  # print( z, F_mean)
  diff = np.abs( z_sims - z )
  id = np.where( diff == diff.min() )[0][0]
  data_sim = data_sims[id]
  z_sim = data_sim['z']
  if np.abs( z_sim - z ) > 0.01: print( 'ERROR: Redshift mismatch')
  skewers_flux = data_sim['skewers_flux']
  skewers_tau = -np.log(skewers_flux)
  skewers_tau_rescaled, alpha = Rescale_Optical_Depth_To_F_Mean( skewers_tau, F_mean )
  print(z, alpha)
  z_vals.append( z )
  alpha_vals.append( alpha )
  
data_out = np.array([ z_vals, alpha_vals ]).T
file_name = output_dir + 'rescale_tau_to_Bosman_2021.txt'
np.savetxt( file_name, data_out )
print( f'Saved File: {file_name}' )  
  


