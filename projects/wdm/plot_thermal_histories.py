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
from figure_functions import *
from data_optical_depth import *
from colors import * 
from stats_functions import compute_distribution, get_highest_probability_interval
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid
from load_tabulated_data import load_data_boera
from matrix_functions import Merge_Matrices
from plot_thermal_history import Plot_T0_gamma_evolution



proj_dir = data_dir + 'projects/wdm/'
sim_dir = data_dir + 'cosmo_sims/1024_25Mpc_wdm/'
output_dir = proj_dir + 'figures/'
create_directory( output_dir )


data_names = [ 'cdm', 'm_2.0kev', 'm_3.0kev', 'm_4.0kev', 'm_5.0kev' ]

labels = [ 'CDM', r'$m_\mathrm{WDM}=2 \, keV$', r'$m_\mathrm{WDM}=3 \, keV$', r'$m_\mathrm{WDM}=4 \, keV$', r'$m_\mathrm{WDM}=5 \, keV$']

z_id = 1

files = range( 34 )

data_all = {}
for data_id, data_name in enumerate(data_names):
  z_sim, T0_sim, gamma_sim = [], [], []
  for n_file in files:
    input_dir = sim_dir + f'{data_name}/analysis_files/'
    file_name = input_dir + f'{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    z_sim.append( z )
    input_dir = sim_dir + f'{data_name}/analysis_files/fit_mcmc_delta_0_1.0/'
    file_name = input_dir + f'fit_{n_file}.pkl'
    data = Load_Pickle_Directory( file_name )
    T0 = 10** data['T0']['mean']
    gamma = data['gamma']['mean']
    T0_sim.append( T0 )
    gamma_sim.append( gamma )
  z_sim = np.array( z_sim )
  T0_sim = np.array( T0_sim ) 
  gamma_sim = np.array( gamma_sim )  
  data_all[data_id] = { 'z':z_sim, 'T0':T0_sim, 'gamma':gamma_sim, 'label':labels[data_id]  }




Plot_T0_gamma_evolution(output_dir, data_sets=data_all, data_sets_gamma=data_all, fig_name='thermal_evolution.png', interpolate_lines=True, show_data=False, xlim=[4.2, 7.5]  )

