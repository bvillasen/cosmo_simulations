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
from plot_thermal_history import Plot_T0_evolution

data_dir = '/raid/bruno/data/'
grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
mcmc_dir = grid_dir + 'fit_mcmc/'

data_boss = 'fit_results_P(k)+tau_HeII_Boss'
data_boss_irsic = 'fit_results_P(k)+tau_HeII_Boss_Irsic'
data_boss_boera = 'fit_results_P(k)+tau_HeII_Boss_Boera'
data_boss_irsic_boera = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera'

output_dir = grid_dir + 'figures/'
create_directory( output_dir )

data_name = data_boss_irsic_boera

print(f'Loading Dataset: {data_name}' )
input_dir = mcmc_dir + f'{data_name}/observable_samples/' 

# Obtain distribution of all the fields
file_name = input_dir + 'samples_fields.pkl'
samples_fields = Load_Pickle_Directory( file_name )
samples_T0 = samples_fields['T0']

data_T0 = { 'z': samples_T0['z'], 'line':samples_T0['Highest_Likelihood'], 'high':samples_T0['higher'], 'low':samples_T0['lower'] }

data_to_plot = { 0: data_T0 }
data_to_plot[0]['label'] = 'This Work'
data_to_plot[0]['color'] = 'C0'


Plot_T0_evolution( output_dir, data_sets=data_to_plot, system='Shamrock', label='', fig_name='fig_T0_evolution_nature', black_background=False )
