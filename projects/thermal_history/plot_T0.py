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


proj_dir = data_dir + 'projects/thermal_history/'
grid_dir = proj_dir + 'data/sim_grid/1024_P19m_np4_nsim400/'
mcmc_dir = grid_dir + 'fit_mcmc/'

data_boss_irsic_boera = 'fit_results_covariance_systematic'

black_background = False

output_dir = proj_dir + 'figures/'
if black_background: output_dir += 'black_background/'
create_directory( output_dir )


data_name = data_boss_irsic_boera
print(f'Loading Dataset: {data_name}' )
input_dir = mcmc_dir + f'{data_name}/observable_samples/' 

# Obtain distribution of all the fields
file_name = input_dir + 'samples_fields.pkl'
samples_fields = Load_Pickle_Directory( file_name )
samples_T0 = samples_fields['T0']
samples_gamma = samples_fields['gamma']

data_T0 = { 'z': samples_T0['z'], 'T0':samples_T0['Highest_Likelihood'], 'high':samples_T0['higher'], 'low':samples_T0['lower'] }
data_gamma = { 'z': samples_gamma['z'], 'gamma':samples_gamma['Highest_Likelihood'], 'high':samples_gamma['higher'], 'low':samples_gamma['lower'] }

color = 'k'

if black_background: color = purples[1]

data_to_plot = { 0: data_T0 }
data_to_plot[0]['label'] = 'This Work (Best-Fit)'
data_to_plot[0]['line_color'] = color

data_to_plot_gamma = { 0: data_gamma }
data_to_plot_gamma[0]['label'] = 'This Work (Best-Fit)'
data_to_plot_gamma[0]['line_color'] = color

# Plot_T0_gamma_evolution( output_dir, data_sets=data_to_plot, label='', fig_name='fig_T0_evolution.png', black_background=black_background, plot_interval=True, interpolate_lines=True,   )
Plot_T0_gamma_evolution( output_dir, data_sets=data_to_plot, data_sets_gamma=data_to_plot_gamma,  label='', fig_name='fig_T0_gamma_evolution.png', black_background=black_background, plot_interval=True, interpolate_lines=True )
