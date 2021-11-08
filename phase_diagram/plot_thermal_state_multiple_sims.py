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
 
root_dir   = data_dir + 'cosmo_sims/rescaled_P19/zero_heat_ion/'
output_dir = data_dir + 'cosmo_sims/rescaled_P19/zero_heat_ion/figures/'
# output_dir = data_dir + 'modified_uvb_rates/zero_heat_ion/figures/'
create_directory( output_dir ) 


n_models = 4


data_all = {}
data_gamma_all = {}
for sim_id in range( n_models ):
  n_files = 56
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
    T0 = 10**(data['T0']['mean'])
    gamma = data['gamma']['mean']
    z_vals.append( z )
    T0_vals.append( T0 )
    gamma_vals.append( gamma )
  z_vals = np.array( z_vals )[::-1]
  T0_vals = np.array( T0_vals )[::-1]
  
  z = z_vals
  v_m = 0.98
  z_l, z_m, z_r = 2.0, 3.0, 3.5
  ind_l = np.where( z<=z_l )[0].max()
  ind_m = np.where( z<=z_m )[0].max()
  ind_r = np.where( z<=z_r )[0].max()
  
  if sim_id == 0:
    T0_vals[ind_l:ind_m] *= np.linspace(1, v_m, ind_m-ind_l)
    T0_vals[ind_m:ind_r] *= np.linspace(v_m, 1, ind_r-ind_m)
  
  gamma_vals = np.array( gamma_vals )[::-1]
  data_all[sim_id] = { 'z':z_vals, 'T0':T0_vals  }
  data_gamma_all[sim_id] = { 'z':z_vals, 'gamma':gamma_vals  }


Plot_T0_gamma_evolution(output_dir, data_sets=data_all, data_sets_gamma=data_gamma_all, fig_name='fig_thermal_zero_heat.png', T0_min=0, z_max=9  )
