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
root_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from plot_thermal_history import Plot_T0_gamma_evolution
from colors import *
from interpolation_functions import smooth_line
from interpolation_functions import interp_line


proj_dir = data_dir + 'projects/thermal_history/'
grid_dir = proj_dir + 'data/sim_grid/1024_P19m_np4_nsim400/'
mcmc_dir = grid_dir + 'fit_mcmc/'

black_background = False

output_dir = proj_dir + 'figures/'
if black_background: output_dir += 'black_background/'
create_directory( output_dir )


data_name = 'fit_results_simulated_HM12_systematic'
print(f'Loading Dataset: {data_name}' )
input_dir = mcmc_dir + f'{data_name}/observable_samples/' 

# Obtain distribution of all the fields
file_name = input_dir + 'samples_fields.pkl'
samples_fields = Load_Pickle_Directory( file_name )
samples_T0 = samples_fields['T0']
samples_gamma = samples_fields['gamma']
z = samples_T0['z']
T0 = samples_T0['Highest_Likelihood']
T0_h = samples_T0['higher']
T0_l = samples_T0['lower']
# z_vals = z
# n_samples_interp = 10000
# z_interp = np.linspace( z_vals[0], z_vals[-1], n_samples_interp ) 
# kind = 'cubic'
# T0   = interp_line( z_vals, z_interp, T0,   kind=kind )
# T0_h = interp_line( z_vals, z_interp, T0_h, kind=kind )
# T0_l = interp_line( z_vals, z_interp, T0_l, kind=kind )
# z = z_interp
# z, T0 = smooth_line( T0, z_vals, log=False, n_neig=3, order=2, interpolate=False,  n_interp=1000 )
# z, T0 = smooth_line( T0, z_vals, log=False, n_neig=3, order=2, interpolate=False,  n_interp=1000 )
# z, T0 = smooth_line( T0, z_vals, log=False, n_neig=3, order=2, interpolate=False,  n_interp=1000 )
data_T0 = { 'z': z, 'T0':T0, 'high':T0_h, 'low':T0_l }
data_gamma = { 'z': samples_gamma['z'], 'gamma':samples_gamma['Highest_Likelihood'], 'high':samples_gamma['higher'], 'low':samples_gamma['lower'] }

color = 'k'

if black_background: color = purples[1]

data_to_plot = { 0: data_T0 }
data_to_plot[0]['label'] = 'Best-Fit to HM12'
data_to_plot[0]['line_color'] = color

data_to_plot_gamma = { 0: data_gamma }
data_to_plot_gamma[0]['label'] = 'Best-Fit to HM12'
data_to_plot_gamma[0]['line_color'] = color

T0_vals, gamma_vals = [], []
input_dir = proj_dir + 'data/1024_50Mpc_HM12/analysis_files/fit_mcmc_delta_0_1.0/'
for n_file in range( 56 ):
  file_name = input_dir + f'fit_{n_file}.pkl'
  fit_data = Load_Pickle_Directory( file_name )
  T0 = fit_data['T0']['mean']
  T0 = 10**T0 
  gamma = fit_data['gamma']['mean']
  T0_vals.append(T0)
  gamma_vals.append(gamma)
T0_vals = np.array(T0_vals)
gamma_vals = np.array(gamma_vals)  
# T0   = interp_line( z_vals, z_interp, T0,   kind=kind )
# T0_h = interp_line( z_vals, z_interp, T0_h, kind=kind )
# T0_l = interp_line( z_vals, z_interp, T0_l, kind=kind )


data_to_plot[1] = {'z':samples_T0['z'], 'T0':T0_vals, 'high':T0_vals, 'low':T0_vals} 
data_to_plot[1]['label'] = 'HM12'
data_to_plot[1]['line_color'] = 'C4'

data_to_plot_gamma[1] =  {'z':samples_T0['z'], 'gamma':gamma_vals, 'high':gamma_vals, 'low':gamma_vals} 
data_to_plot_gamma[1]['label'] = 'HM12'
data_to_plot_gamma[1]['line_color'] = 'C4'



# Plot_T0_gamma_evolution( output_dir, data_sets=data_to_plot, label='', fig_name='fig_T0_evolution.png', black_background=black_background, plot_interval=True, interpolate_lines=True,   )
Plot_T0_gamma_evolution( output_dir, data_sets=data_to_plot, data_sets_gamma=data_to_plot_gamma,  label='', fig_name='fig_T0_gamma_evolution_HM12.png', black_background=black_background, plot_interval=True, interpolate_lines=True, show_data=True)
