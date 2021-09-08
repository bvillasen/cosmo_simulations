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

z_reion = 6.1

# root_dir = data_dir + 'cosmo_sims/sim_grid/1024_np4_nsim81/fit_mcmc/fit_results_P(k)+_Boera/'
root_dir = data_dir + f'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+z_ion_H_Boera_zreion{z_reion}/fit_redshift/'
output_dir = root_dir + 'figures/'
create_directory( output_dir ) 

data_all = {}

z_vals = [ 4.2, 4.6, 5.0 ] 
data_sim = {}
for z_indx, z_val in enumerate(z_vals):
  input_dir = root_dir + f'redshift_{z_indx}/observable_samples/'
  file_name = input_dir + 'samples_power_spectrum.pkl'
  data = Load_Pickle_Directory( file_name )
  data_sim[z_indx] = data[z_indx]
data_sim['z_vals'] = np.array([ data_sim[i]['z'] for i in data_sim ])


data_all[0] = data_sim
data_all[0]['line_color'] = 'C1'
# data_all[1]['label'] = 'WDM $m$=2 keV Individual Fit'
data_all[0]['label'] = r'$z_{99.9}$=' + f'{z_reion} Individual Fit'


Plot_Power_Spectrum_Grid( output_dir, ps_samples=data_all, fig_name='flux_ps.png', scales='small_highz', line_colors=None, sim_data_sets=None, )

