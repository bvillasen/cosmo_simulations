import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 



base_dir = data_dir + 'cosmo_sims/rescaled_P19/wdm/'

n_files = 56

sim_name = '1024_50Mpc_cdm'
input_dir = base_dir + f'{sim_name}/analysis_files/'

for n_file in range(n_files):
  
  file_name = input_dir + f'{n_file}_analysis.h5'
  print( f'Loading File: {file_name}' )
  file = h5.File( file_name, 'r')
  z = file.attrs['current_z'][0]
  file.close()
  
  file_name = input_dir + f'analysis_files/fit_mcmc_delta_0_1.0/fit_{n_file}.pkl'
  fit_data = Load_Pickle_Directory( file_name, 'r' )
  
  
  
  break 
  


