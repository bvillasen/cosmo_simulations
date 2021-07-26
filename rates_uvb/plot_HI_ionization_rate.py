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
from tools import *
from plot_uvb_rates import Plot_HI_Photoionization


output_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_modified_gamma/figures/'
create_directory( output_dir ) 


input_dir_0 = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc/'
input_dir_1 = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_modified_gamma/'

input_dirs = [ input_dir_0, input_dir_1 ]
# input_dirs = [ input_dir_0  ]


data_all = {}
for data_id, input_dir in enumerate(input_dirs):
  file_name = input_dir + f'UVB_rates.h5'
  file = h5.File( file_name, 'r' )
  rates = file['UVBRates']
  z = rates['z'][...]
  ionization = rates['Chemistry']['k24'][...]
  data_all[data_id] = { 'z':z, 'photoionization':ionization }
  
data_all[0]['label'] = 'Modified P19'
data_all[1]['label'] = 'Modified from Equilibrium to match HI '


Plot_HI_Photoionization( output_dir, rates_data=data_all, figure_name='fig_phothoionization_HI.png' )