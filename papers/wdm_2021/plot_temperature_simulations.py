import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 



base_dir = data_dir + 'cosmo_sims/rescaled_P19/wdm/'

wdm_masses = [ 0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0 ]
sim_names = []
for m_wdm in wdm_masses:
  sim_names.append( f'1024_50Mpc_wdm_m{m_wdm}kev')
sim_names.append('1024_50Mpc_cdm')


# n_files = 56
# sim_data_all = {}
# for sim_id, sim_name in sim_names:
#   sim_name = '1024_50Mpc_cdm'
#   input_dir = base_dir + f'{sim_name}/analysis_files/'
# 
#   z_vals, T0_vals = [], []
#   for n_file in range(n_files):
# 
#     file_name = input_dir + f'{n_file}_analysis.h5'
#     print( f'Loading File: {file_name}' )
#     file = h5.File( file_name, 'r')
#     z = file.attrs['current_z'][0]
#     file.close()
# 
#     file_name = input_dir + f'fit_mcmc_delta_0_1.0/fit_{n_file}.pkl'
#     fit_data = Load_Pickle_Directory( file_name, 'r' )
#     T0 = fit_data['T0']['mean']
#     z_vals.appens(z)
#     T0_vals.append(T0)
#   sim_data_all[sim_id] = {'z':z_vals, 'T0':T0_vals }
# 
# 


