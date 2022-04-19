import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
base_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from mcmc_sampling_functions import Get_Highest_Likelihood_Params
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid
from plot_flux_power_spectrum_grid_diff import Plot_Power_Spectrum_Grid_diff
from colors import *
from load_tabulated_data import load_power_spectrum_table, load_data_irsic, load_data_boera, load_tabulated_data_viel, load_data_boss, load_data_gaikwad
from interpolation_functions import interpolate_1d_linear
from data_optical_depth_HeII import data_tau_HeII_Worserc_2019


black_background = False

ps_data_dir =  base_dir + 'lya_statistics/data/'
proj_dir = data_dir + 'projects/thermal_history/'
output_dir = proj_dir + f'figures/'
if black_background: output_dir += 'black_background/'
create_directory( output_dir )
root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
mcmc_dir = root_dir + 'fit_mcmc/'

data_name = 'fit_results_covariance_systematic'

samples_all = {}
samples_all['param'] = {}
samples_all['P(k)'] = {}

print(f'Loading Dataset: {data_name}' )
input_dir = mcmc_dir + f'{data_name}/observable_samples/' 
stats_file = input_dir + 'fit_mcmc.pkl'
samples_file = input_dir + 'samples_mcmc.pkl'

params = Load_Pickle_Directory( input_dir + 'params.pkl' )

print( f'Loading File: {stats_file}')
stats = pickle.load( open( stats_file, 'rb' ) )
for p_id in params.keys():
  p_name = params[p_id]['name']
  p_stats = stats[p_name]
  params[p_id]['mean'] = p_stats['mean']
  params[p_id]['sigma'] = p_stats['standard deviation']
print( f'Loading File: {samples_file}')
param_samples = pickle.load( open( samples_file, 'rb' ) )
samples_all['param'] = param_samples

# Get the Highest_Likelihood parameter values 
params_HL = Get_Highest_Likelihood_Params( param_samples, n_bins=100 )
 
# Obtain distribution of the power spectrum
file_name = input_dir + 'samples_power_spectrum.pkl'
samples_ps = Load_Pickle_Directory( file_name )  
samples_ps['z_vals'] = np.array([ samples_ps[i]['z'] for i in samples_ps ])
samples_all['P(k)'] = samples_ps


ps_samples = samples_all['P(k)']


# Apply resolution correction
correction_file_name = ps_data_dir + 'FPS_resolution_correction_1024_50Mpc.pkl'
FPS_correction = Load_Pickle_Directory( correction_file_name ) 
corr_z_vals = FPS_correction['z_vals']


n_snapshots = 14
for z_id in range(n_snapshots):
  ps_data = ps_samples[z_id]
  z = ps_data['z']
  k_vals = ps_data['k_vals']
  ps_mean = ps_data['Highest_Likelihood']
  ps_h = ps_data['higher']
  ps_l = ps_data['lower']
  z_diff = np.abs( corr_z_vals - z )
  if z_diff.min() > 5e-2: 
    print( f'Large redshift diference: {z_diff.min()}')
    continue  
  z_indx = np.where( z_diff == z_diff.min() )[0]
  if len( z_indx ) != 1 :
    print( f'ERROR: Unable to match the redshift of the correction fator. {z} -> {correction_z_vals[z_indx]}  ')
    exit(-1)
  z_indx = z_indx[0]
  correction = FPS_correction[z_indx]
  correction_k_vals = correction['k_vals']
  correction_ps_factor = correction['delta_factor']
  indices = correction_ps_factor > 1
  new =  correction_ps_factor[indices] - 1
  correction_ps_factor[indices] = 1 + new * 1
  k_diff = np.abs( k_vals - correction_k_vals )
  # print( f'{z} {correction_ps_factor}')
  if k_diff.sum() > 1e-6:
     print(f'ERROR: Large k difference for FPS correction: {k_diff.sum()}.')
     exit(-1)
  ps_mean = ps_mean / correction_ps_factor
  ps_h = ps_h / correction_ps_factor
  ps_l = ps_l / correction_ps_factor
  if z >= 4.0:
    k_l = 0.08
    indices = k_vals >= k_l
    n = indices.sum()
    factor = np.linspace( 1, 1.2, n)
    ps_mean[indices] *= factor
    ps_h[indices] *= factor
    ps_l[indices] *= factor
  ps_data['Highest_Likelihood'] = ps_mean
  ps_data['higher'] = ps_h
  ps_data['lower'] = ps_l

dir_boss = ps_data_dir + 'data_power_spectrum_boss/'
data_boss = load_data_boss( dir_boss )

dir_data_boera = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_data_boera( dir_data_boera, corrected=False, print_out=False )

dir_irsic = ps_data_dir + 'data_power_spectrum_irsic_2017/'
data_irsic = load_data_irsic( dir_irsic )

data_sets = {'BOSS':data_boss, 'Irsic':data_irsic, 'Boera':data_boera}

z_sim = samples_ps['z_vals']

delta_L = {}
for data_name in data_sets:
  delta_L[data_name] = {}
  data_set = data_sets[data_name]
  z_data = data_set['z_vals']
  for z_id, z in enumerate(z_data):
    indx, selected_z = select_closest_index( z, z_sim )
    sim_ps_data = samples_ps[indx]
    sim_k  = sim_ps_data['k_vals']
    sim_ps = sim_ps_data['Highest_Likelihood'] / sim_k * np.pi
    kmin, kmax = sim_k.min(), sim_k.max()
    data_k  = data_set[z_id]['k_vals']
    data_ps = data_set[z_id]['power_spectrum']
    # data_sigma = data_set[z_id]['sigma_power_spectrum']
    cov_matrix = data_set[z_id]['covariance_matrix']
    indices =  ( data_k >= kmin ) * ( data_k <= kmax )
    data_k  = data_k[indices]
    data_ps = data_ps[indices]
    # data_sigma = data_sigma[indices]
    sim_ps  = interpolate_1d_linear( data_k, sim_k, sim_ps, log_y=True ) 
    k_indices = np.where( indices == True )[0]
    n_samples = len(k_indices)
    cov_matrix_adjusted = np.zeros([n_samples, n_samples])
    for i in range(n_samples):
      for j in range(n_samples):
        indx_i, indx_j = k_indices[i], k_indices[j]
        cov_matrix_adjusted[i,j] = cov_matrix[indx_i, indx_j]
    cov_matrix = cov_matrix_adjusted
    delta_ps = data_ps - sim_ps
    inv_cov = np.linalg.inv( cov_matrix )
    L_ps_0 = np.matmul( delta_ps.T, inv_cov )
    L_ps = np.matmul( L_ps_0, delta_ps )
    det = np.linalg.det( cov_matrix )
    N = n_samples
    L = - 0.5 * ( L_ps + np.log(det) + N*np.log(2*np.pi) )
    delta_L[data_name][z_id] = { 'z':z, 'delta_L': L}
  

z_vals = [ 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 5.0 ]
# 
# for z in z_vals:
#   L_redshift = 0
#   for data_name in data_sets:
#     data_set = data_sets[data_name]
#     data_z = data_set['z_vals']
#     indx, selected_z = select_closest_index( z, data_z )
#     if indx is None: continue
#     L_local = delta_L[data_name][indx]['delta_L']
#     print( f' z:{z}    data:{data_name}    indx:{indx}    L:{L_local}')
#     L_redshift += L_local
#   print( f'z:{z}    L:{L_redshift}   ')
# 
    
    
data_set = data_tau_HeII_Worserc_2019
data_z = data_set['z']  
data_tau = data_set['tau']
data_sigma = data_set['tau_sigma']
n_data = len( data_z )
    
    
    
    
# Obtain distribution of tau_He
file_name = input_dir + 'samples_fields.pkl'
samples_fields = Load_Pickle_Directory( file_name )  
samples_tau = samples_fields['tau_HeII']
sim_z = samples_tau['z'][::-1]
sim_tau = samples_tau['Highest_Likelihood'][::-1]


for indx in range(n_data):
  z = data_z[indx]
  tau = data_tau[indx]
  sigma = data_sigma[indx]
  tau_sim = interpolate_1d_linear( z, sim_z, sim_tau )
  L =  0.5* ( ( ( tau_sim - tau  ) / sigma )**2 + np.log( 2*np.pi * sigma**2 ) )    
  print( f'z:{z}   tau_data:{tau}   tau_sim:{tau_sim}   sigma:{sigma}    L:{L}' )  
    
    
    
      
   
  