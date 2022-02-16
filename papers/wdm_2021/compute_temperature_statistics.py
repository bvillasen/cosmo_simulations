import sys, os, time
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
sys.path.append( cosmo_dir + 'lya_statistics/data' )
from tools import *
from stats_functions import get_highest_probability_interval

# grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_nsim600/'
grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_cdm/'
fit_name = 'fit_results_P(k)+_Boera_covmatrix'
input_dir = grid_dir + f'fit_mcmc/{fit_name}/'
output_dir = grid_dir + f'fit_mcmc/{fit_name}/'
create_directory( output_dir )


file_name = input_dir + f'samples_T0_evolution.h5'
print( f'Loading File: {file_name}' )
file = h5.File( file_name, 'r' )
z = file['z'][...]
T0 = file['T0'][...]
file.close()
n_samples, n_z = T0.shape

n_bins = 500
fill_sum = 0.68
low, high, max, mean = [], [], [], []
time_start = time.time()
for z_id in range(n_z):
  T0_vals = T0[:,z_id]
  v_mean = T0_vals.mean()
  hist, bin_edges = np.histogram( T0_vals, bins=n_bins ) 
  distribution = hist / hist.sum()
  bin_centers = ( bin_edges[:-1] + bin_edges[1:] ) / 2.
  v_l, v_r, v_max,  sum_interval = get_highest_probability_interval( bin_centers, distribution, fill_sum, log=False, n_interpolate=None, print_eval=False)
  low.append(v_l)
  high.append(v_r)
  max.append(v_max)
  mean.append(v_mean)
  print_progress( z_id, n_z, time_start )  
low  = np.array(low)
high = np.array(high)
mean = np.array(mean)
max  = np.array(max)
stats = {'percentile':fill_sum, 'z':z, 'low':low, 'high':high, 'mean':mean, 'max':max }

out_file_name = output_dir + 'T0_stats.pkl'
Write_Pickle_Directory( stats, out_file_name )



