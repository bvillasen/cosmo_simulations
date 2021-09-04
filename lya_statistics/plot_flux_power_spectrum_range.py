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

root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera/'
input_dir_0 = root_dir + 'observable_samples/'

# root_dir = data_dir + 'cosmo_sims/sim_grid/1024_np4_nsim81/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera/'
root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+_Boera/'
input_dir_1 = root_dir + 'observable_samples/'

output_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera/figures/'
create_directory( output_dir ) 


input_dirs = [ input_dir_0 ]

data_all = {}
for data_id, input_dir in enumerate(input_dirs):
  file_name = input_dir + 'samples_power_spectrum.pkl'
  data = Load_Pickle_Directory( file_name )
  data_sim = {}
  for snap_id in data:
    data_snap = data[snap_id]
    z = data_snap['z']
    k_vals = data_snap['k_vals']
    ps = data_snap['Highest_Likelihood'] 
    ps_h = data_snap['higher']
    ps_l = data_snap['lower']
    data_sim[snap_id] = { 'z':z, 'k_vals':k_vals, 'Highest_Likelihood':ps, 'higher':ps_h, 'lower':ps_l } 
  data_sim['z_vals'] = np.array([ data_sim[i]['z'] for i in data_sim ])
  data_all[data_id] = data_sim
# 
data_all[0]['line_color'] = 'black'
# # data_all[1]['line_color'] = 'C1'

data_all[0]['label'] = 'Original Best-Fit'
# # data_all[1]['label'] = r'Fit to Bo`era $P(k)$'


# # 
# # alpha_vals = [ 2, 2.5, 3, 3.5, 4, 4.5  ]
# # 
# # data_ps = {}
# # for data_id, input_dir in enumerate(input_dirs):
# #   # if data_id == 1: continue
# #   sim_data = {}
# #   for n_file in range(0,56):
# #     file_name = input_dir + f'{n_file}_analysis.h5'
# #     file = h5.File( file_name, 'r' )
# #     z = file.attrs['current_z'][0]
# #     ps_data = file['lya_statistics']['power_spectrum']
# #     k  = ps_data['k_vals'][...] 
# #     ps = ps_data['p(k)'][...]
# #     indx = ps > 0
# #     snap_data = {  'z':z, 'k_vals': k[indx], 'ps_mean':ps[indx] }
# #     sim_data[n_file] = snap_data
# #   sim_data['z_vals'] = np.array([ sim_data[i]['z'] for i in sim_data ])
# #   data_ps[data_id] = sim_data
# # 
Plot_Power_Spectrum_Grid( output_dir, ps_samples=data_all, fig_name='flux_ps.png', scales='all', line_colors=None, sim_data_sets=None, )

