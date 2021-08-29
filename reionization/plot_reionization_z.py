import sys, os
import numpy as np
import h5py as h5
import palettable
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import pylab
import pickle
from matplotlib.legend_handler import HandlerTuple
import matplotlib.pyplot as plt
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import * 
from colors import *
from stats_functions import compute_distribution, get_highest_probability_interval


root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera/'
input_dir_0 = root_dir + 'observable_samples/'

# root_dir = data_dir + 'cosmo_sims/sim_grid/1024_np4_nsim81/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera/'
root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+_Boera/'
input_dir_1 = root_dir + 'observable_samples/'

output_dir = data_dir + 'cosmo_sims/sim_grid/figures/'
create_directory( output_dir ) 

input_dirs = [ input_dir_0, input_dir_1 ]

field_name = 'z_ion_H'
n_bins = 50

data_all = {}
for data_id, input_dir in enumerate(input_dirs):
  file_name = input_dir + 'samples_fields.pkl'
  data = Load_Pickle_Directory( file_name )
  data_field = data[field_name]
  z_ion = data_field['mean']
  z_ion_h = data_field['higher']
  z_ion_l = data_field['lower']
  trace = data_field['trace']
  distribution, bin_centers = compute_distribution( trace, n_bins, log=False, normalize_to_bin_width=True )

  data_all[data_id] = { 'z_ion':z_ion, 'high':z_ion_h, 'low':z_ion_l, 'distribution':distribution, 'bin_centers':bin_centers }

data_all[0]['line_color'] = 'black'
data_all[1]['line_color'] = 'C1'

data_all[0]['label'] = 'Original Best-Fit'
data_all[1]['label'] = r'Fit to Boera $P(k)$'


global_prop_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/global_properties/'
file_name = global_prop_dir + 'grid_z_reionization.pkl'
data_grid = Load_Pickle_Directory( file_name )
z_reion_vals = np.array([ data_grid[i] for i in data_grid ])
distribution_sim, bin_centers_sim = compute_distribution( z_reion_vals, n_bins, log=False, normalize_to_bin_width=True )


import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"





label_size = 11
legend_font_size = 9
fig_label_size = 15


tick_label_size_major = 10
tick_label_size_minor = 10
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.3
tick_width_minor = 1

color_data_tau = light_orange
sim_color = 'k'


if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=legend_font_size)
if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size)
if system == 'Tornado': 
  prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size)
  prop_bold = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica_bold.ttf"), size=legend_font_size)


ncols, nrows = 1, 1 
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6*ncols,6*nrows))

ax.plot( bin_centers_sim, distribution_sim, ls='--',color='C0', zorder=1, label='Simulation Grid',  )


for sim_id in data_all:
  sim_data = data_all[sim_id]
  bin_centers = sim_data['bin_centers']
  distribution = sim_data['distribution']
  sim_color = sim_data['line_color']
  label = sim_data['label']
  ax.plot( bin_centers, distribution, color=sim_color, zorder=2, label=label )

ax.legend( loc=2, frameon=False, prop=prop)
# ax.set_xlim(2.09, 3.19 )
# ax.set_ylim(0.5, 7 )
# 
ax.set_xlabel( r'$z_{\mathregular{99.9}}$', fontsize=label_size )
ax.set_ylabel( r'$f(z_{\mathregular{99.9}})$', fontsize=label_size )

ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')


figure_name = output_dir + 'z_reionization.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )

