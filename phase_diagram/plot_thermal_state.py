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
 
# input_dir_0 = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc/analysis_files/'
input_dir = data_dir + 'cosmo_sims/rescaled_P19/modified_gamma/'
output_dir = data_dir + 'cosmo_sims/rescaled_P19/modified_gamma/figures/'
create_directory( output_dir ) 
n_sims = 7
input_dirs = [ input_dir + f'sim_{i}/analysis_files/' for i in range(n_sims) if i!=4]


alpha_vals = [ 2, 2.5, 3, 3.5, 4, 4.5  ]

data_all = {}
for data_id, input_dir in enumerate(input_dirs):
  # if data_id == 1: continue
  z_vals, T0_vals, gamma_vals = [], [], []
  for n_file in range(0,56):
    file_name = input_dir + f'{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    file.close()
    z_vals.append( z )
    file_name = input_dir + f'/fit_mcmc_delta_0_1.0/fit_{n_file}.pkl'
    data = Load_Pickle_Directory( file_name )
    T0 = 10**(data['T0']['mean'])
    gamma = data['gamma']['mean']
    T0_vals.append( T0 )
    gamma_vals.append( gamma )   
  z_vals = np.array( z_vals )
  T0_vals = np.array( T0_vals )
  gamma_vals = np.array( gamma_vals )
  T0_vals = np.array( T0_vals )
  gamma_vals = np.array( gamma_vals )
  if data_id == 0: label = 'Best-Fit V21 '
  else: label = r'$\alpha={0:.1f}$'.format( alpha_vals[data_id-1])
  data_all[data_id] = { 'z':z_vals, 'T0':T0_vals, 'gamma':gamma_vals, 'label':label }


Plot_T0_gamma_evolution(output_dir, data_sets=data_all, fig_name='fig_T0_modified_gamma.png', interpolate_lines=True, plot_gamma=False  )
