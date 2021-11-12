import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
cosmo_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
sys.path.append( cosmo_dir + 'lya_statistics/data' )
from tools import *
from data_optical_depth import *
from colors import * 
from stats_functions import compute_distribution, get_highest_probability_interval
from plot_optical_depth import Plot_tau_HI



base_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_nsim120/fit_mcmc/fit_results_P(k)+_Boera_/'

input_dir_0 = base_dir + 'observable_samples/'
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
  tau = data_field[HL_key][index]
  tau_h = data_field['higher'][index]
  tau_l = data_field['lower'][index]
  tau_vals.append( tau )
  tau_vals_h.append( tau_h )
  tau_vals_l.append( tau_l )
tau_vals = np.array( tau_vals )
tau_vals_h = np.array( tau_vals_h )
tau_vals_l = np.array( tau_vals_l )

data_tau = {}
data_tau[0] = {'z':z_vals_all, 'mean':tau_vals, 'higher':tau_vals_h, 'lower':tau_vals_l }
data_tau[0]['label'] = r'{0} Individual Fit to Boera P(k)'.format(label) 
# data_tau[0]['label'] = 'WDM $m$=2 keV Individual Fit to Boera P(k)' 
data_tau[0]['color'] = 'C0'


data_all  = {}
file_name = input_dir_0 + 'samples_fields.pkl'
data = Load_Pickle_Directory( file_name )
data_field = data['tau']
z = data_field['z']
tau = data_field[HL_key]
tau_h = data_field['higher']
tau_l = data_field['lower']
data_all[0] = { 'z':z, 'tau':tau, 'high':tau_h, 'low':tau_l }

data_all[0]['line_color'] = 'k'
data_all[0]['label'] = r'{0} Joint Fit to Boera P(k)'.format(label)
# data_all[1]['label'] = r'WDM $m$=2 keV Joint Fit to Boera P(k)'

Plot_tau_HI(output_dir, samples_tau_HI=data_all, points_tau=data_tau, labels='', black_background = False, figure_name='fig_HI_tau_wdm.png'  )

