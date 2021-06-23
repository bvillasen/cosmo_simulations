import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import palettable
import pylab
import pickle
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from colors import *
from plot_flux_power_spectrum import plot_power_spectrum_grid

ps_data_dir = root_dir + 'lya_statistics/data/'

data_dir = '/raid/bruno/data/'
input_dir_0  = data_dir + f'cosmo_sims/rescaled_P19/1024_50Mpc/analysis_files/'
input_dir_1  = data_dir + f'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m3.0kev/analysis_files/'
input_dir_2  = data_dir + f'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m1.0kev/analysis_files/'
input_dir_3  = data_dir + f'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m0.5kev/analysis_files/'
output_dir = data_dir + f'cosmo_sims/rescaled_P19/wdm/figures/'
create_directory( output_dir )

input_dir_list = [ input_dir_0, input_dir_1, input_dir_2, input_dir_3 ]
# labels = ['CDM', 'WDM m = 0.5 keV', 'WDM m = 1.0 keV', 'WDM m = 3.0 keV' ]
labels = [ r'$\mathrm{CDM}$', r'$\mathrm{WDM\,\,\, m = 3.0 keV}$', r'$\mathrm{WDM\,\,\, m = 1.0 \,keV}$', r'$\mathrm{WDM\,\,\, m = 0.5 \,keV}$', ]


n_sims = len(input_dir_list)
n_files = 56

data_ps = {}
for sim_id in range(n_sims):
  input_dir = input_dir_list[sim_id]
  data_sim = {}
  for n_file in range(n_files):
    file_name = input_dir + f'{n_file}_analysis.h5'
    infile = h5.File( file_name, 'r' )
    current_z = infile.attrs['current_z'][0]
    ps_data = infile['lya_statistics']['power_spectrum']
    k_vals = ps_data['k_vals'][...]
    ps_mean = ps_data['p(k)'][...]
    indices = np.where( ps_mean > 0 )
    ps_mean = ps_mean[indices]
    k_vals = k_vals[indices]
    data_sim[n_file] = { 'z':current_z, 'k_vals':k_vals, 'ps_mean':ps_mean  }
  sim_z_vals = np.array([ data_sim[i]['z'] for i in range(n_files) ])
  data_sim['label'] = labels[sim_id]
  data_sim['z_vals'] = sim_z_vals
  data_ps[sim_id] = data_sim
  

blue = blues[4]
yellow = yellows[2]
green = greens[5]
colors = [ 'C0', 'C1', green,    yellow  ]


plot_power_spectrum_grid( ps_data_dir, output_dir, ps_data=data_ps, scales='large_middle', sim_data_sets=None, system='Shamrock', black_background=True, line_colors=colors  )
plot_power_spectrum_grid( ps_data_dir, output_dir, ps_data=data_ps, scales='small_reduced', sim_data_sets=None, system='Shamrock', black_background=True, line_colors=colors  )

