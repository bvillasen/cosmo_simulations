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



# # input_dir_0 = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc/analysis_files/'
# input_dir = data_dir + 'cosmo_sims/rescaled_P19/modified_gamma/'
# output_dir = data_dir + 'cosmo_sims/rescaled_P19/modified_gamma/figures/'
proj_dir = data_dir + 'projects/thermal_history/'
input_dir = proj_dir + 'data/modified_gamma_sigmoid/'
output_dir = proj_dir + 'figures/modified_gamma_sigmoid/'
create_directory( output_dir ) 
n_sims = 6
input_dirs = [ input_dir + f'sim_{i}/analysis_files/' for i in range(n_sims) ]



alpha_vals = [ 2, 2.5, 3, 3.5, 4, 4.5  ]

data_tau = {}
for data_id, input_dir in enumerate(input_dirs):
  # if data_id == 1: continue
  z_vals, F_vals = [], []
  for n_file in range(10,45):
    file_name = input_dir + f'{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    F_mean =file['lya_statistics'].attrs['Flux_mean_HI'][0]
    z_vals.append( z )
    F_vals.append( F_mean )
  z_vals = np.array( z_vals )
  F_vals = np.array( F_vals )
  tau_vals = -np.log( F_vals )
  if data_id == 0: label = 'Best-Fit V21 '
  else: label = r'$\alpha={0:.1f}$'.format( alpha_vals[data_id-1])
  data_tau[data_id] = { 'z':z_vals, 'tau':tau_vals, 'label':label  }


Plot_tau_HI(output_dir, samples_tau_HI=data_tau, labels='', black_background = False, figure_name='fig_HI_tau_modified_gamma_new.png'  )

