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


root_dir = data_dir + 'cosmo_sims/sim_grid/1024_np5_nsim16/'
analysis_dir = root_dir + 'analysis_files/'
output_dir = root_dir + 'figures/'
create_directory( output_dir ) 

sim_dirs = [ f for f in os.listdir(analysis_dir) if f[0]=='S']
sim_dirs.sort()

# 
data_ps = {}
for data_id, sim_dir in enumerate(sim_dirs):
  sim_data = {}
  for n_file in range(0,56):
    input_dir = analysis_dir + sim_dir 
    file_name = input_dir + f'/{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    ps_data = file['lya_statistics']['power_spectrum']
    k  = ps_data['k_vals'][...] 
    ps = ps_data['p(k)'][...]
    indx = ps > 0
    snap_data = {  'z':z, 'k_vals': k[indx], 'ps_mean':ps[indx] }
    sim_data[n_file] = snap_data
  sim_data['z_vals'] = np.array([ sim_data[i]['z'] for i in sim_data ])
  data_ps[data_id] = sim_data


Plot_Power_Spectrum_Grid( output_dir, ps_data=data_ps, scales='large', line_colors=None, sim_data_sets=None, )
Plot_Power_Spectrum_Grid( output_dir, ps_data=data_ps, scales='middle', line_colors=None, sim_data_sets=None, )
Plot_Power_Spectrum_Grid( output_dir, ps_data=data_ps, scales='small', line_colors=None, sim_data_sets=None, )
