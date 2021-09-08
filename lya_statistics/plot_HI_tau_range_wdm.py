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
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from colors import *
from plot_optical_depth import Plot_tau_HI

root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera/'
input_dir_0 = root_dir + 'observable_samples/'

base_dir = data_dir + 'cosmo_sims/sim_grid/1024_np4_nsim81/fit_mcmc/fit_results_P(k)+_Boera/'
# base_dir = data_dir + 'cosmo_sims/sim_grid/1024_mwdm2p0_nsim64/fit_mcmc/fit_results_P(k)+_Boera/'
input_dir_1 = base_dir + 'observable_samples/'
output_dir = base_dir + '/figures/'
create_directory( output_dir ) 
# 
z_vals_all = [  4.2, 4.6, 5.0 ] 


z_ids = range( 3 )

tau_vals, tau_vals_h, tau_vals_l = [], [], []
for z_id in z_ids:
  z = z_vals_all[z_id]
  input_dir = base_dir + f'fit_redshift/redshift_{z_id}/'
  file_name = input_dir + 'observable_samples/samples_fields.pkl'
  data = Load_Pickle_Directory( file_name )
  data_field = data['tau']
  z_vals = data_field['z']
  diff = np.abs( z_vals - z )
  diff_min = diff.min()
  if diff_min >= 5e-2: print( "Large z difference" )
  index = np.where( diff == diff_min )[0][0]
  z_val = z_vals[index]
  tau = data_field['Highest_Likelihood'][index]
  tau_h = data_field['higher'][index]
  tau_l = data_field['lower'][index]
  tau_vals.append( tau )
  tau_vals_h.append( tau_h )
  tau_vals_l.append( tau_l )
tau_vals = np.array( tau_vals )
tau_vals_h = np.array( tau_vals_h )
tau_vals_l = np.array( tau_vals_l )

data_tau = {}
data_tau[0] = {'z':z_vals_all, 'mean':tau_vals, 'higher':tau_vals_h, 'lower':tau_vals_l, }
data_tau[0]['label'] = 'CDM Individual Fit to Boera P(k)' 
# data_tau[0]['label'] = 'WDM $m$=2 keV Individual Fit to Boera P(k)' 
data_tau[0]['color'] = 'C4'



input_dirs = [ input_dir_0, input_dir_1  ]

field_name = 'tau'

data_all = {}
for data_id, input_dir in enumerate(input_dirs):
  file_name = input_dir + 'samples_fields.pkl'
  data = Load_Pickle_Directory( file_name )
  data_field = data[field_name]
  z = data_field['z']
  field = data_field['mean']
  field_h = data_field['higher']
  field_l = data_field['lower']
  data_all[data_id] = { 'z':z, 'tau':field, 'high':field_h, 'low':field_l }

data_all[0]['line_color'] = 'black'
data_all[0]['label'] = 'Original Best-Fit'


data_all[1]['line_color'] = 'C0'
data_all[1]['label'] = 'CDM Joint Fit to Boera P(k)'
# data_all[1]['label'] = r'WDM $m$=2 keV Joint Fit to Boera P(k)'


Plot_tau_HI( output_dir, points_tau=data_tau,  samples_tau_HI=data_all, labels='', black_background=False, figure_name='fig_tau_HI_fit_to_boera', plot_interval=True )

