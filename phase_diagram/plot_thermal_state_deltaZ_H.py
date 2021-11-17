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
 
root_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_deltaZ_H/'
output_dir = root_dir + 'figures/'
create_directory( output_dir ) 


n_models = 5
n_files = 36

colors = [ 'C0', 'C2', 'C3', 'C1', 'C4' ]
deltaZ_H_vals = [ -1., -0.5, 0.0, 0.5, 1.0 ]

factor = 0.95 

data_all = {}
data_gamma_all = {}
for sim_id in range( n_models ):
  if sim_id == 5: n_files = 51
  z_vals, T0_vals, gamma_vals = [], [], []
  for n_file in range(0,n_files):
    sim_dir = root_dir + f'sim_{sim_id}'
    input_dir = sim_dir + '/analysis_files/'
    file_name = input_dir + f'{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    file.close()
    file_name = input_dir + f'/fit_mcmc_delta_0_1.0/fit_{n_file}.pkl'
    data = Load_Pickle_Directory( file_name )
    T0 = 10**(data['T0']['mean']) * factor
    gamma = data['gamma']['mean']
    z_vals.append( z )
    T0_vals.append( T0 )
    gamma_vals.append( gamma )
  z_vals = np.array( z_vals )[::-1]
  T0_vals = np.array( T0_vals )[::-1]
  gamma_vals = np.array( gamma_vals )[::-1]
  data_all[sim_id] = { 'z':z_vals, 'T0':T0_vals  }
  data_all[sim_id]['line_color'] = colors[sim_id]
  label = r'$\Delta z_\mathrm{H} =$' + f' {deltaZ_H_vals[sim_id]:0.1f}'
  data_all[sim_id]['label'] = label
  


Plot_T0_gamma_evolution(output_dir, data_sets=data_all, fig_name='T0_deltaZ_H.png',  z_max=9  )
