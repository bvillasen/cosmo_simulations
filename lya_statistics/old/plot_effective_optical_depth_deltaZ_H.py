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



root_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_deltaZ_H/'
output_dir = root_dir + 'figures/'
create_directory( output_dir ) 

n_sims = 5
n_files = 36

colors = [ 'C0', 'C2', 'C3', 'C1', 'C4' ]
deltaZ_H_vals = [ -1., -0.5, 0.0, 0.5, 1.0 ]


data_tau = {}
for sim_id in range(n_sims):
  input_dir = root_dir + f'sim_{sim_id}/analysis_files/'
  z_vals, F_vals = [], []
  for n_file in range(n_files):
    file_name = input_dir + f'{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    F_mean =file['lya_statistics'].attrs['Flux_mean_HI'][0]
    z_vals.append( z )
    F_vals.append( F_mean )
  z_vals = np.array( z_vals )
  F_vals = np.array( F_vals )
  tau_vals = -np.log( F_vals )
  label = r'$\Delta z_\mathrm{H} =$' + f' {deltaZ_H_vals[sim_id]:0.1f}'
  color = colors[sim_id]
  data_tau[sim_id] = { 'z':z_vals, 'tau':tau_vals, 'label':label, 'line_color':color  }


Plot_tau_HI(output_dir, samples_tau_HI=data_tau, labels='', black_background = False, figure_name='tau_deltaZ_H.png', z_max=7.2  )

