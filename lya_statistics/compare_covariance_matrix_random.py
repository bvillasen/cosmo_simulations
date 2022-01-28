import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from stats_functions import bootstrap_sample_mean, compute_covariance_matrix
from load_tabulated_data import load_tabulated_data_boera 
from matrix_functions import Normalize_Covariance_Matrix

ps_data_dir = root_dir + 'lya_statistics/data/'
data_boera_dir = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_tabulated_data_boera( data_boera_dir )
k_vals_boera = data_boera[0]['k_vals']

# grid_dir = args[1]
grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_nsim600'
if grid_dir[-1] != '/': grid_dir += '/'
ps_dir = grid_dir + 'flux_power_spectrum/'
analysis_dir = grid_dir + 'analysis_files/'
output_dir = grid_dir + 'figures/covariance_matrix/'
create_directory( output_dir )

selected_file_indices = [ 25, 29, 33 ] # redshits 5.0, 4.6 and 4.2
file_indx = selected_file_indices[0]

sim_dirs = [ d for d in os.listdir(ps_dir) if d[0]=='S' ]
sim_dirs.sort()
n_sims = len( sim_dirs )

bootstrap = False
bootstrap_indx = 3

sim_data_all = {}
for sim_id, sim_dir in enumerate(sim_dirs):
  if bootstrap:  file_name = ps_dir + f'{sim_dir}/bootstrap_statistics_sampled_boera_{file_indx:03}.pkl'
  else: file_name = ps_dir + f'{sim_dir}/statistics_sampled_boera_{file_indx:03}.pkl'
  stats_data = Load_Pickle_Directory( file_name )
  if bootstrap: stats_data = stats_data[bootstrap_indx]
  sim_data_all[sim_id] = stats_data


ncols, nrows = 4, 5
n_to_plot = ncols * nrows

cov_min, cov_max = np.inf, -np.inf

plot_normalized = True

data_to_plot = {}
indices = []
for data_id in range(n_to_plot):
  indx = np.random.randint(0, n_sims, 1)[0]
  while indx in indices:
    indx = np.random.randint(0, n_sims, 1)[0]
  indices.append( indx )
  sim_data = sim_data_all[indx]
  if bootstrap: n_in_sample = sim_data['n_in_sample']
  cov_matrix = sim_data['covariance_matrix']
  cov_matrix_norm = Normalize_Covariance_Matrix( cov_matrix )
  if plot_normalized: cov_matrix = cov_matrix_norm
  cov_min, cov_max = min( cov_min, cov_matrix.min() ), max( cov_max, cov_matrix.max() )
  data_to_plot[data_id] = { 'covariance_matrix': cov_matrix }  
  

colormap = 'turbo'

ax_lenght = 6 
figure_width, figure_height = ncols * ax_lenght, nrows * ax_lenght
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width,figure_height))
plt.subplots_adjust( hspace = 0.05, wspace=0.05)

for i in range(nrows):
  for j in range(ncols):
    fig_id = i*ncols + j
    
    ax = ax_l[i][j]
    fig_data = data_to_plot[fig_id]
    cov_matrix = fig_data['covariance_matrix']
    ax.imshow( cov_matrix, vmin=cov_min, vmax=cov_max, cmap=colormap )
    
    ax.set_xticks([])
    ax.set_yticks([])



figure_indx = 0
figure_name = output_dir + 'cm_multiple'
if plot_normalized: figure_name += '_normalized'
figure_name += f'_{figure_indx}'
figure_name += '.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )

