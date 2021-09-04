import sys, os
import numpy as np
import h5py as h5
import palettable
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import pylab
import pickle
from matplotlib.legend_handler import HandlerTuple
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from colors import *
from plot_optical_depth import Plot_tau_HI

root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera/'
input_dir_0 = root_dir + 'observable_samples/'

root_dir = data_dir + 'cosmo_sims/sim_grid/1024_np4_nsim81/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera_Walther/'
# root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+_Boera/'
input_dir_1 = root_dir + 'observable_samples/'

output_dir = data_dir + 'cosmo_sims/sim_grid/figures/'
create_directory( output_dir ) 

input_dirs = [ input_dir_0, input_dir_1 ]

field_name = 'tau'

data_all = {}
for data_id, input_dir in enumerate(input_dirs):
  file_name = input_dir + 'samples_fields.pkl'
  data = Load_Pickle_Directory( file_name )
  data_field = data[field_name]
  z = data_field['z']
  field = data_field['mean']
  field_h = data_field['higher']
  field_l = data_field['lower']
  data_all[data_id] = { 'z':z, 'tau':field, 'high':field_h, 'low':field_l }

data_all[0]['line_color'] = 'black'
data_all[1]['line_color'] = 'C1'

data_all[0]['label'] = 'Original Best-Fit'
data_all[1]['label'] = r'Fit including Walther $P\,(k)$'


Plot_tau_HI( output_dir,  samples_tau_HI=data_all, labels='', black_background=False, figure_name='fig_tau_HI_separate_heat_ion.png', plot_interval=True )

