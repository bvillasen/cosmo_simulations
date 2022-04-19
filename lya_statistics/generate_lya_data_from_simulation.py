import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import load_analysis_data
from load_tabulated_data import load_data_irsic, load_data_boera,  load_data_boss
from interpolation_functions import interpolate_1d_linear 
from data_optical_depth_HeII import data_tau_HeII_Worserc_2019

ps_data_dir =  root_dir + 'lya_statistics/data/'

dir_boss = ps_data_dir + 'data_power_spectrum_boss/'
data_boss = load_data_boss( dir_boss )

dir_data_boera = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_data_boera( dir_data_boera, corrected=False )

dir_irsic = ps_data_dir + 'data_power_spectrum_irsic_2017/'
data_irsic = load_data_irsic( dir_irsic )

sim_dir = data_dir + 'cosmo_sims/1024_50Mpc_HM12/'
input_dir = sim_dir + 'analysis_files/'
output_dir = ps_data_dir

snapshots = range( 15, 56 )

# z_vals = 

data_all = { }
for data_id, n_snap in enumerate(snapshots):
  data = load_analysis_data( n_snap, input_dir, phase_diagram=False, lya_statistics=True, load_fit=True, load_flux_Pk=True, mcmc_fit_dir='fit_mcmc_delta_0_1.0')
  z  = data['cosmology']['current_z']
  tau_H = data['lya_statistics']['tau']
  tau_He = data['lya_statistics']['tau_HeII']
  k_vals  = data['lya_statistics']['power_spectrum']['k_vals'] 
  ps_vals = data['lya_statistics']['power_spectrum']['ps_mean']
  data_all[data_id] = { 'z':z, 'tau':tau_H, 'tau_HeII':tau_He, 'k_vals':k_vals, 'ps_vals':ps_vals }

z_sim = np.array([ data_all[data_id]['z'] for data_id in data_all ])  


# Apply resolution correction
correction_file_name = ps_data_dir + 'FPS_resolution_correction_1024_50Mpc.pkl'
FPS_correction = Load_Pickle_Directory( correction_file_name ) 
corr_z_vals = FPS_correction['z_vals']
 

n_snapshots = len(z_sim)
for z_id in range(n_snapshots):
  ps_data = data_all[z_id]
  z = ps_data['z']
  k_vals = ps_data['k_vals']
  ps_mean = ps_data['ps_vals']
  z_diff = np.abs( corr_z_vals - z )
  if z_diff.min() > 5e-2: 
    print( f'Large redshift diference: {z_diff.min()}')
    continue  
  z_indx = np.where( z_diff == z_diff.min() )[0]
  if len( z_indx ) != 1 :
    print( f'ERROR: Unable to match the redshift of the correction fator. {z} -> {correction_z_vals[z_indx]}  ')
    exit(-1)
  z_indx = z_indx[0]
  print( z_id, z, z_indx)
  correction = FPS_correction[z_indx]
  correction_k_vals = correction['k_vals']
  correction_ps_factor = correction['delta_factor']
  indices = correction_ps_factor > 1
  new =  correction_ps_factor[indices] - 1
  correction_ps_factor[indices] = 1 + new * 1
  k_diff = np.abs( k_vals - correction_k_vals )
  print( f'{z} {correction_ps_factor}')
  if k_diff.sum() > 1e-6:
     print(f'ERROR: Large k difference for FPS correction: {k_diff.sum()}.')
     exit(-1)
  ps_mean = ps_mean / correction_ps_factor
  if z in [3.0, 3.2]:
    k_l = 0.01
    indices = k_vals >= k_l
    n = indices.sum()
    factor = np.linspace( 1, 1.2, n)
    ps_mean[indices] *= factor
  ps_data['ps_vals'] = ps_mean
  


data_set = data_tau_HeII_Worserc_2019
data_z = data_set['z']
data_tau = data_set['tau']
data_sigma = data_set['tau_sigma']
sim_tau_vals = np.array([ data_all[data_id]['tau_HeII'] for data_id in data_all ])
tau_vals = []
for z in data_z:
  tau_interp = interpolate_1d_linear( z, z_sim[::-1], sim_tau_vals[::-1] )
  tau_vals.append( tau_interp )
tau_vals = np.array( tau_vals )
simulated_tau_HeII = { 'z':data_z, 'tau':tau_vals, 'tau_sigma':data_sigma, 'name':'Simulated HM12' }
Write_Pickle_Directory( simulated_tau_HeII, output_dir+'simulated_tau_HeII_HM12.pkl')





data_sets = {'Boss':data_boss, 'Boera':data_boera, 'Irsic':data_irsic }
simulated_ps = {}

for data_name in data_sets:
  simulated_ps[data_name] = {}
  data_set = data_sets[data_name]
  k_data = data_set['k_vals']
  z_data = data_set['z_vals']
  print(f'Generating data_set: {data_name}')
  for data_id in data_set:
    if data_id in [ 'k_vals', 'z_vals', 'full_covariance' ]: continue
    data = data_set[data_id]
    z = data['z']
    print( f'{data_id}  z={z}')
    z_diff = np.abs( z_sim - z )
    diff_min = z_diff.min()
    if diff_min > 1e-3: print( 'ERROR: Large z difference')
    z_indx = np.where( z_diff == diff_min )[0]
    if len(z_indx) != 1: print( 'ERROR: not a valid z_indx')
    data_sim = data_all[z_indx[0]]
    k_sim = data_sim['k_vals']
    ps_sim = data_sim['ps_vals']
    delta_sim = ps_sim * k_sim / np.pi
    k_min, k_max = k_sim.min(), k_sim.max()
    k_indices = ( k_data >= k_min ) * ( k_data <= k_max )
    data_delta = data['delta_power'][k_indices]
    data_sigma = data['delta_power_error'][k_indices]
    selected_k  = k_data[k_indices]
    selected_delta = interpolate_1d_linear( selected_k, k_sim, delta_sim, log_y=True )
    ps_diff = ( selected_delta - data_delta ) / data_delta 
    # print( ps_diff )
    ps = selected_delta / selected_k * np.pi
    ps_sigma = data_sigma / selected_k * np.pi
    simulated_ps[data_name][data_id] = {'z':z, 'power_spectrum':ps, 'sigma_power_spectrum':ps_sigma, 'delta_power':selected_delta, 'delta_power_error':data_sigma, 'k_vals':selected_k  }
  simulated_ps[data_name]['k_vals'] = selected_k
  simulated_ps[data_name]['z_vals'] = z_data



Write_Pickle_Directory( simulated_ps, output_dir+'simulated_power_spectrum_HM12_corrected.pkl')