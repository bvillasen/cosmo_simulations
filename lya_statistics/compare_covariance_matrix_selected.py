import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_grid_parameters import Grid_Parameters
from simulation_grid import Simulation_Grid
from simulation_parameters import *
from stats_functions import bootstrap_sample_mean, compute_covariance_matrix
from load_tabulated_data import load_tabulated_data_boera 
from matrix_functions import Normalize_Covariance_Matrix

ps_data_dir = base_dir + 'lya_statistics/data/'
data_boera_dir = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_tabulated_data_boera( data_boera_dir )
k_vals_boera = data_boera[0]['k_vals']


import matplotlib
matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/fonts/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

# grid_dir = args[1]
grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_nsim600'
if grid_dir[-1] != '/': grid_dir += '/'
ps_dir = grid_dir + 'flux_power_spectrum/'
analysis_dir = grid_dir + 'analysis_files/'

selected_file_indices = [ 25, 29, 33 ] # redshits 5.0, 4.6 and 4.2
file_indx = selected_file_indices[2]

output_dir = grid_dir + f'figures/covariance_matrix/sampled_boera_native/snap_{file_indx}/'
create_directory( output_dir )

sim_dirs = [ d for d in os.listdir(ps_dir) if d[0]=='S' ]
sim_dirs.sort()
n_sims = len( sim_dirs )

bootstrap = False
bootstrap_indx = 3

SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )

params = [ 'wdm_mass', 'scale_H_ion', 'scale_H_Eheat', 'deltaZ_H' ]

# param_to_plot = 'wdm_mass'
# param_to_plot = 'scale_H_ion'
# param_to_plot = 'scale_H_Eheat'
# param_to_plot = 'deltaZ_H'

for param_to_plot in params:

  params_to_select = { 'wdm_mass': 10000, 'scale_H_ion':1, 'scale_H_Eheat':0.9, 'deltaZ_H':0.0 }
  params_to_select[param_to_plot] = None

  selected_sims = SG.Select_Simulations( params_to_select, tolerance=5e-3 )
  n_sims = len(selected_sims)

  sim_data_all = {}
  for sim_id in selected_sims:
    sim_dir = sim_dirs[sim_id]
    if bootstrap:  file_name = ps_dir + f'{sim_dir}/bootstrap_statistics_sampled_boera_native_{file_indx:03}.pkl'
    else: file_name = ps_dir + f'{sim_dir}/statistics_sampled_boera_native_{file_indx:03}.pkl'
    # if bootstrap:  file_name = ps_dir + f'{sim_dir}/bootstrap_statistics_{file_indx:03}.pkl'
    # else: file_name = ps_dir + f'{sim_dir}/statistics_{file_indx:03}.pkl'
    stats_data = Load_Pickle_Directory( file_name )
    if bootstrap: stats_data = stats_data[bootstrap_indx]
    sim_data_all[sim_id] = stats_data
    sim = SG.Grid[sim_id]
    for key in sim:
      sim_data_all[sim_id][key] =  sim[key] 
    print( sim['parameter_values'] )
    
    

  param_labels = { 'scale_He':r'$\beta_{\mathrm{He}}$', 'scale_H':r'$\beta_{\mathrm{H}}$', 'deltaZ_He':r'$\Delta z_{\mathrm{He}}$', 'deltaZ_H':r'$\Delta z_{\mathrm{H}}$',
                    'scale_H_ion': r'$\beta_{\mathrm{H}}^{\mathrm{ion}}$', 'scale_He_ion': r'$\beta_{\mathrm{He}}^{\mathrm{ion}}$', 'scale_He_Eheat': r'$\alpha E_{\mathrm{He}}$', 'scale_H_Eheat': r'$\alpha E_{\mathrm{H}}$',
                    'wdm_mass':r'$m_{\mathrm{WDM}}$', 'inv_wdm_mass':r'$m_{\mathrm{WDM}}^{-1}$  [keV$^{-1}$]'       }

  param_label = param_labels[param_to_plot]


  ncols, nrows = n_sims, 1
  if param_to_plot == 'wdm_mass':ncols, nrows = n_sims//2, 2
  n_to_plot = ncols * nrows

  cov_min, cov_max = np.inf, -np.inf

  plot_normalized = True

  data_to_plot = {}
  for data_id, sim_id in enumerate(selected_sims):
    sim_data = sim_data_all[sim_id]
    if bootstrap: n_in_sample = sim_data['n_in_sample']
    cov_matrix = sim_data['covariance_matrix']
    k_vals = sim_data['k_vals']
    cov_matrix_norm = Normalize_Covariance_Matrix( cov_matrix )
    if plot_normalized: cov_matrix = cov_matrix_norm
    cov_min, cov_max = min( cov_min, cov_matrix.min() ), max( cov_max, cov_matrix.max() )
    data_to_plot[data_id] = { 'covariance_matrix': cov_matrix } 
    data_to_plot[data_id]['parameters'] = sim_data['parameters'] 


  colormap = 'turbo'
  figure_text_size = 18
  label_size = 16
  text_color = 'black'

  ax_lenght = 6 
  figure_width, figure_height = ncols * ax_lenght, nrows * ax_lenght
  fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width,figure_height))
  plt.subplots_adjust( hspace = 0.1, wspace=0.1)


  k_min, k_max = np.log10(k_vals.min()), np.log10(k_vals.max())
  for i in range(nrows):
    for j in range(ncols):
      fig_id = i*ncols + j
      if nrows > 1:  ax = ax_l[i][j]
      else: ax = ax_l[j]
      
      fig_data = data_to_plot[fig_id]
      cov_matrix = fig_data['covariance_matrix']
      im = ax.imshow( cov_matrix, vmin=cov_min, vmax=cov_max, cmap=colormap,extent=(k_min, k_max, k_max, k_min) )
      
      if j == ncols-1:
        cax = ax.inset_axes([1.04, 0.1, 0.05, 0.8], transform=ax.transAxes)
        fig.colorbar(im, ax=ax, cax=cax)
      
      
      param_val = fig_data['parameters'][param_to_plot]
      text = param_label + f'= {param_val:.1f}'
      if param_to_plot == 'wdm_mass': text += ' keV'
      if param_to_plot == 'wdm_mass' and param_val == 10000: text = 'CDM'
      text_pos_x = 0.8
      if param_to_plot == 'wdm_mass': text_pos_x = 0.7
      ax.text(text_pos_x, 0.92, r'{0}'.format(text), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='white') 

      if i == nrows-1:  ax.set_xlabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )
      if j == 0: ax.set_ylabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )

      # ax.set_xticks([ -2.5, -2, -1.5, -1, -0.5])
      # ax.set_yticks([ -2.5, -2, -1.5, -1, -0.5])
      ax.set_xticks([ -2, -1.5, -1 ])
      ax.set_yticks([ -2, -1.5, -1 ])
      # ax.set_xticks([])
      # ax.set_yticks([])



  figure_indx = 0
  figure_name = output_dir + f'cm_multiple_{param_to_plot}'
  if plot_normalized: figure_name += '_normalized'
  figure_name += '.png'
  fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
  print( f'Saved Figure: {figure_name}' )

