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
  return  tau_los_rescaled


data_dir = '/raid/bruno/data/'
input_dir  = data_dir + f'cosmo_sims/rescaled_P19/1024_50Mpc_high_z/'
output_dir = data_dir + f'cosmo_sims/rescaled_P19/1024_50Mpc_high_z/figures/'
create_directory( output_dir )

data_sims = {}
for n_file in range(17):
  data = load_analysis_data( n_file, input_dir+'analysis_files/', phase_diagram=False, lya_statistics=True )
  skewers_data = Load_Skewers_File( n_file, input_dir+'skewers_files/', chem_type = 'HI', axis_list = [ 'x', 'y', 'z' ] )
  current_z = skewers_data['current_z']
  vel_Hubble = skewers_data['vel_Hubble']
  dv = vel_Hubble[1] - vel_Hubble[0] 
  skewers_flux = skewers_data['skewers_flux_HI']
  data_sims[n_file] = { 'z':current_z, 'skewers_flux':skewers_flux }
  
z_sims = np.array([ data_sims[i]['z'] for i in data_sims ])

