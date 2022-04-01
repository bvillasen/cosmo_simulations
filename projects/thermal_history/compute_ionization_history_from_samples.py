import sys, os, time
import numpy as np
import h5py as h5
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from stats_functions import compute_distribution, get_highest_probability_interval

fit_name = 'fit_results_covariance_systematic'
grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
input_dir = grid_dir + f'fit_mcmc/{fit_name}/'
output_dir = data_dir + 'figures/thermal_history/paper/data/'
create_directory(output_dir)

file_name = input_dir + f'samples_thermal_evolution.h5'
file = h5.File( file_name, 'r' )

fill_sum = 0.95
data_out = {}
for key in [ 'x_HI', 'n_e', 'T0' ]:
  print( f'Computing distribution: {key}' )
  key_vals = file[key][...]
  n_samples, nz = key_vals.shape
  vals_high, vals_low, vals_max, vals_mean = [], [], [], [] 
  for z_id in range(nz):
    # if z_id != 48: continue 
    slice = key_vals[:,z_id]
    distribution, bin_centers = compute_distribution( slice, n_bins=100, log=True )
    v_l, v_h, v_max, sum_interval = get_highest_probability_interval( bin_centers, distribution, fill_sum, log=True, n_interpolate=10000 )
    v_mean = slice.mean()
    vals_low.append( v_l )
    vals_high.append( v_h )
    vals_max.append( v_max )
    vals_mean.append( v_mean )
  vals_low = np.array( vals_low )
  vals_high = np.array( vals_high )
  vals_max = np.array( vals_max )
  vals_mean = np.array( vals_mean )
  data_out[key] = { 'low':vals_low, 'high':vals_high, 'mean':vals_mean, 'max':vals_max }

z = file['z'][...]
data_out['z'] = z

file_name = output_dir + 'ionization_history.pkl'
Write_Pickle_Directory( data_out, file_name )
  
