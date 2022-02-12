import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
sys.path.append( cosmo_dir + 'lya_statistics/data' )
from tools import *
from data_optical_depth import *
from colors import * 
from stats_functions import compute_distribution, get_highest_probability_interval
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid


ps_data_dir = cosmo_dir + 'lya_statistics/data/'
data_name = 'fit_results_P(k)+_Boera'
base_dir = data_dir + 'cosmo_sims/sim_grid/'
output_dir = base_dir + '1024_wdmgrid_nsim600/figures/fit_covariance_matrix/'
create_directory( output_dir )


grid_name = '1024_wdmgrid_nsim600'
data_names = [ 'fit_results_P(k)+_Boera_sigma', 'fit_results_P(k)+_Boera_covmatrix', ]
data_labels = [ 'Boera Sigma', 'Boera Cov M' ]

HL_key = 'Highest_Likelihood'
# HL_key = 'mean'
# HL_key = 'max'
print( f'HL key: {HL_key}')

line_colors = [ 'C0', 'C1', 'C2' ]

z_indices = [ 0, 1 , 2]
 
data_all = {} 
for data_id, data_name in enumerate(data_names):
  data_dir = base_dir + f'{grid_name}/fit_mcmc/{data_name}/'
  data_sim = {}
  for z_indx in z_indices:
    input_dir = data_dir + f'fit_redshift/redshift_{z_indx}/observable_samples/'
    file_name = input_dir + 'samples_power_spectrum.pkl'
    data = Load_Pickle_Directory( file_name, print_out=True )
    data_snap = data[z_indx]
    z = data_snap['z']
    k_vals = data_snap['k_vals']
    ps_mean = data_snap['mean'] 
    ps_HL = data_snap['Highest_Likelihood'] 
    ps_max = data_snap['max'] 
    ps_h = data_snap['higher']
    ps_l = data_snap['lower']
    data_sim[z_indx] = { 'z':z, 'k_vals':k_vals, 'Highest_Likelihood':ps_HL, 'mean':ps_mean, 'max':ps_max, 'higher':ps_h, 'lower':ps_l } 
  data_sim['z_vals'] = np.array([ data_sim[i]['z'] for i in data_sim ])
  data_all[data_id] = data_sim
  data_all[data_id]['label'] = data_labels[data_id]
  data_all[data_id]['line_color'] = line_colors[data_id]

data_all[0]['line_color'] = ocean_green

fig_name = f'flux_ps_wdm_{HL_key}_independent_redshift.png'
Plot_Power_Spectrum_Grid( output_dir, ps_samples=data_all, fig_name=fig_name, scales='small_highz', line_colors=None, sim_data_sets=None, plot_boeraC=False, HL_key=HL_key, ps_data_dir=ps_data_dir )

