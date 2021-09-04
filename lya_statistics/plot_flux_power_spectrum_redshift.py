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
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid


base_dir = data_dir + 'cosmo_sims/sim_grid/1024_np4_nsim81/fit_mcmc/fit_results_P(k)+_Boss_Irsic_Boera_Walther/'
output_dir = data_dir + 'cosmo_sims/sim_grid/1024_np4_nsim81/fit_mcmc/fit_results_P(k)+_Boss_Irsic_Boera_Walther/figures/'
create_directory( output_dir ) 


data_ps = {}

z_ids = range( 14 )
for z_id in z_ids:
  input_dir = base_dir + f'redshift_{z_id}/'
  file_name = input_dir + 'observable_samples/samples_power_spectrum.pkl'
  data = Load_Pickle_Directory( file_name )
  data_snap = data[z_id]
  z = data_snap['z']
  k_vals = data_snap['k_vals']
  ps_mean = data_snap['Highest_Likelihood']
  ps_h = data_snap['higher']
  ps_l = data_snap['lower']
  data_ps[z_id] = {'z':z, 'k_vals':k_vals, 'ps_mean':ps_mean, 'higher':ps_h, 'lower':ps_l }
data_ps['z_vals'] = np.array([ data_ps[i]['z'] for i in data_ps ])

data_ps_all = {}
data_ps_all[0] = data_ps

Plot_Power_Spectrum_Grid( output_dir, ps_data=data_ps_all, fig_name='flux_fit_redshift.png', scales='all', line_colors=None, sim_data_sets=None, plot_interval=True )


# data_ps = {}
# for data_id, input_dir in enumerate(input_dirs):
#   sim_data = {}
#   for n_file in range(0,56):
#     file_name = input_dir + f'{n_file}_analysis.h5'
#     file = h5.File( file_name, 'r' )
#     z = file.attrs['current_z'][0]
#     ps_data = file['lya_statistics']['power_spectrum']
#     k  = ps_data['k_vals'][...] 
#     ps = ps_data['p(k)'][...]
#     indx = ps > 0
#     snap_data = {  'z':z, 'k_vals': k[indx], 'ps_mean':ps[indx] }
#     sim_data[n_file] = snap_data
#   sim_data['z_vals'] = np.array([ sim_data[i]['z'] for i in sim_data ])
#   data_ps[data_id] = sim_data
# 
# data_ps[0]['label'] = 'Modified P19'
# data_ps[1]['label'] = 'Modified from Eq to match HI '
# 
# # Plot_Power_Spectrum_Grid( output_dir, ps_data=data_ps, scales='large', line_colors=None, sim_data_sets=None, )
# # Plot_Power_Spectrum_Grid( output_dir, ps_data=data_ps, scales='middle', line_colors=None, sim_data_sets=None, )

