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

# base_dir = data_dir + 'cosmo_sims/sim_grid/1024_np4_nsim81/fit_mcmc/fit_results_P(k)+_BoeraC/'
# base_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_nsim192/fit_mcmc/fit_results_P(k)+_BoeraC/'
base_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_nsim192/fit_mcmc/fit_results_P(k)+_Boera/'
# base_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_nsim192/fit_mcmc/fit_results_P(k)+_Viel/'


input_dir_1 = base_dir + 'observable_samples/'
output_dir = base_dir + '/figures/'
create_directory( output_dir ) 

# label = 'CDM' 
# label = 'WDM $m$=2 keV' 
# label = 'WDM $m$=3 keV' 
# label = 'WDM $m$=4 keV' 
# label = '$z_{99.9}$=5.4' 
label = ''



z_vals_all = [  4.2, 4.6, 5.0 ] 


# HL_key = 'Highest_Likelihood'
# HL_key = 'mean'
HL_key = 'max'

print( f'HL key: {HL_key}')

data_ps = {}
z_ids = range( 3 )

T0_vals, T0_vals_h, T0_vals_l = [], [], []
for z_id in z_ids:
  z = z_vals_all[z_id]
  input_dir = base_dir + f'fit_redshift/redshift_{z_id}/'
  file_name = input_dir + 'observable_samples/samples_fields.pkl'
  data = Load_Pickle_Directory( file_name )
  data_field = data['T0']
  z_vals = data_field['z']
  diff = np.abs( z_vals - z )
  diff_min = diff.min()
  if diff_min >= 5e-2: print( "Large z difference" )
  index = np.where( diff == diff_min )[0][0]
  z_val = z_vals[index]
  T0 = data_field[HL_key][index]
  T0_h = data_field['higher'][index]
  T0_l = data_field['lower'][index]
  T0_vals.append( T0 )
  T0_vals_h.append( T0_h )
  T0_vals_l.append( T0_l )
T0_vals = np.array( T0_vals )
T0_vals_h = np.array( T0_vals_h )
T0_vals_l = np.array( T0_vals_l )

data_T0 = {}
data_T0[0] = {'z':z_vals_all, 'mean':T0_vals, 'higher':T0_vals_h, 'lower':T0_vals_l }
data_T0[0]['label'] = r'{0} Individual Fit to Boera P(k)'.format(label) 
# data_T0[0]['label'] = 'WDM $m$=2 keV Individual Fit to Boera P(k)' 
data_T0[0]['color'] = 'C4'

input_dirs = [ input_dir_0, input_dir_1 ]

field_name = 'T0'

data_all = {}
for data_id, input_dir in enumerate(input_dirs):
  file_name = input_dir + 'samples_fields.pkl'
  data = Load_Pickle_Directory( file_name )
  data_field = data[field_name]
  z = data_field['z']
  T0 = data_field[HL_key]
  T0_h = data_field['higher']
  T0_l = data_field['lower']
  data_all[data_id] = { 'z':z, 'T0':T0, 'high':T0_h, 'low':T0_l }

data_all[0]['line_color'] = 'black'
data_all[0]['label'] = 'Original Best-Fit'

data_all[1]['line_color'] = 'C0'
data_all[1]['label'] = r'{0} Joint Fit to Boera P(k)'.format(label)
# data_all[1]['label'] = r'WDM $m$=2 keV Joint Fit to Boera P(k)'


Plot_T0_gamma_evolution(output_dir, data_sets=data_all, points_T0=data_T0, fig_name='fig_T0_fit_to_boera.png', interpolate_lines=True, plot_gamma=False, plot_interval=True  )
