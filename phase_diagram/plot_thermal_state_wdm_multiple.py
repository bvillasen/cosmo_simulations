import sys, os
import numpy as np
import h5py as h5
import palettable
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import pylab
import pickle
from matplotlib.legend_handler import HandlerTuple
import os, sys
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from plot_thermal_history import Plot_T0_gamma_evolution
 

base_dir = data_dir + 'cosmo_sims/sim_grid/'
output_dir = base_dir + 'figures_wdm_new/'
create_directory( output_dir )

data_name = 'fit_results_P(k)+_Boera'

HL_key = 'Highest_Likelihood'
# HL_key = 'mean'
# HL_key = 'max'

print( f'HL key: {HL_key}')


# grid_name_0 = '1024_wdmgrid_nsim200_deltaZ_n0p5'
# grid_name_1 = '1024_wdmgrid_nsim200_deltaZ_0p0'
# grid_name_2 = '1024_wdmgrid_nsim200_deltaZ_0p5'
# grid_names = [ grid_name_0, grid_name_1, grid_name_2 ]
# data_labels = [ r'$\Delta z = -0.5$', r'$\Delta z = 0.0$', r'$\Delta z = 0.5$' ]

grid_name_0 = '1024_wdmgrid_nsim600'
grid_names = [ grid_name_0 ]
data_labels = [ '' ]

data_name = 'fit_results_P(k)+_Boera_covMatrix'
line_colors = [ 'C0', 'C1', 'C2' ]

field_name = 'T0'
data_all = {}
for data_id, grid_name in enumerate(grid_names):
  input_dir = base_dir + f'{grid_name}/fit_mcmc/{data_name}/observable_samples/'
  file_name = input_dir + 'samples_fields.pkl'
  data = Load_Pickle_Directory( file_name )
  data_field = data[field_name]
  z = data_field['z']
  T0 = data_field[HL_key]
  T0_h = data_field['higher']
  T0_l = data_field['lower']
  data_all[data_id] = { 'z':z, 'T0':T0, 'high':T0_h, 'low':T0_l }
  data_all[data_id]['label'] = data_labels[data_id]
  data_all[data_id]['line_color'] = line_colors[data_id]

Plot_T0_gamma_evolution(output_dir, data_sets=data_all, points_T0=None, fig_name=f'fig_T0_wdm_{HL_key}.png', interpolate_lines=True, plot_interval=True  )
