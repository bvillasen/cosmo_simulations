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
 

root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera/'
input_dir_0 = root_dir + 'observable_samples/'

# root_dir = data_dir + 'cosmo_sims/sim_grid/1024_np4_nsim81/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera/'
root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+_Boera/'
input_dir_1 = root_dir + 'observable_samples/'

output_dir = data_dir + 'cosmo_sims/sim_grid/figures/'
create_directory( output_dir ) 

input_dirs = [ input_dir_0, input_dir_1 ]

field_name = 'T0'

data_all = {}
for data_id, input_dir in enumerate(input_dirs):
  file_name = input_dir + 'samples_fields.pkl'
  data = Load_Pickle_Directory( file_name )
  data_field = data[field_name]
  z = data_field['z']
  T0 = data_field['mean']
  T0_h = data_field['higher']
  T0_l = data_field['lower']
  data_all[data_id] = { 'z':z, 'T0':T0, 'high':T0_h, 'low':T0_l }

data_all[0]['line_color'] = 'black'
data_all[1]['line_color'] = 'C1'

data_all[0]['label'] = 'Original Best-Fit'
data_all[1]['label'] = r'Fit to Boera $P(k)$'

Plot_T0_gamma_evolution(output_dir, data_sets=data_all, fig_name='fig_T0_boera_ps.png', interpolate_lines=True, plot_gamma=False, plot_interval=True  )
