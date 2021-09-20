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

base_dir = data_dir + 'cosmo_sims/sim_grid/1024_np4_nsim81/fit_mcmc/fit_results_P(k)+_Boss_Irsic_Boera_Walther/'
output_dir = data_dir + 'cosmo_sims/sim_grid/1024_np4_nsim81/fit_mcmc/fit_results_P(k)+_Boss_Irsic_Boera_Walther/figures/'
create_directory( output_dir ) 

z_vals_all = [ 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 5.0 ] 



data_ps = {}
z_ids = range( 14 )

T0_vals, T0_vals_h, T0_vals_l = [], [], []
for z_id in z_ids:
  z = z_vals_all[z_id]
  input_dir = base_dir + f'redshift_{z_id}/'
  file_name = input_dir + 'observable_samples/samples_fields.pkl'
  data = Load_Pickle_Directory( file_name )
  data_field = data['T0']
  z_vals = data_field['z']
  diff = np.abs( z_vals - z )
  diff_min = diff.min()
  if diff_min >= 5e-2: print( "Large z difference" )
  index = np.where( diff == diff_min )[0][0]
  z_val = z_vals[index]
  T0 = data_field['Highest_Likelihood'][index]
  T0_h = data_field['higher'][index]
  T0_l = data_field['lower'][index]
  T0_vals.append( T0 )
  T0_vals_h.append( T0_h )
  T0_vals_l.append( T0_l )
T0_vals = np.array( T0_vals )
T0_vals_h = np.array( T0_vals_h )
T0_vals_l = np.array( T0_vals_l )

data_T0 = {}
data_T0[0] = {'z':z_vals_all, 'mean':T0_vals, 'higher':T0_vals_h, 'lower':T0_vals_l, 'label':'Fit to redshift' }


input_dirs = [ input_dir_0 ]

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

data_all[0]['label'] = 'Original Best-Fit'

Plot_T0_gamma_evolution(output_dir, data_sets=data_all, points_T0=data_T0, fig_name='fig_T0_separate_heat_ion_redshift.png', interpolate_lines=True, plot_gamma=False, plot_interval=True  )
