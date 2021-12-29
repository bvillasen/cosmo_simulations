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
 
root_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_nsim200_deltaZ_0p5/'
analysis_dir = root_dir + 'analysis_files/'
output_dir = root_dir + 'figures/'
create_directory( output_dir ) 

sim_dirs = [ f for f in os.listdir(analysis_dir) if f[0]=='S']
sim_dirs.sort()

n_snapshots = 36

data_all = {}
for data_id, sim_dir in enumerate(sim_dirs):
  z_vals, T0_vals, gamma_vals = [], [], []
  for n_file in range(0,n_snapshots):
    input_dir = analysis_dir + sim_dir 
    file_name = input_dir + f'/{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    file_name = input_dir + f'/fit_mcmc_delta_0_1.0/fit_{n_file}.pkl'
    data = Load_Pickle_Directory( file_name )
    T0 = 10**(data['T0']['mean'])
    gamma = data['gamma']['mean']
    z_vals.append( z )
    T0_vals.append( T0 )
    gamma_vals.append( gamma ) 
  z_vals = np.array( z_vals )
  T0_vals = np.array( T0_vals )
  gamma_vals = np.array( gamma_vals )
  data_all[data_id] = { 'z':z_vals, 'T0':T0_vals, 'gamma':gamma_vals  }


Plot_T0_gamma_evolution(output_dir, data_sets=data_all, fig_name='fig_thermal_evolution.png'  )
