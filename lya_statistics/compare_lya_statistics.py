import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools')
from tools import *

data_dir = '/raid/bruno/data/'
input_dir_0 = data_dir + f'cosmo_sims/rescaled_P19/1024_50Mpc/'
input_dir_1 = data_dir + f'cosmo_sims/rescaled_P19/1024_50Mpc_new/'

for n_file in  range( 56 ): 

  in_file_name = input_dir_0 + f'analysis_files/{n_file}_analysis.h5'
  in_file = h5.File( in_file_name, 'r' )
  k_vals_0  = in_file['lya_statistics']['power_spectrum']['k_vals'][...]
  ps_mean_0 = in_file['lya_statistics']['power_spectrum']['p(k)'][...] 

  in_file_name = input_dir_1 + f'analysis_files/{n_file}_analysis.h5'
  in_file = h5.File( in_file_name, 'r' )
  k_vals_1  = in_file['lya_statistics']['power_spectrum']['k_vals'][...]
  ps_mean_1 = in_file['lya_statistics']['power_spectrum']['p(k)'][...] 

  diff_k = np.abs( k_vals_1 - k_vals_0 ) / k_vals_0
  ps_mean_0 = ps_mean_0[ ps_mean_0 > 0 ]
  ps_mean_1 = ps_mean_1[ ps_mean_1 > 0 ]
  
  print( f'Diff    K: {diff_k.max()}  ' )
  if len(ps_mean_0) > 0:
    diff_ps = np.abs( ps_mean_1 - ps_mean_0 ) / ps_mean_0 
    print( f'Diff    K: {diff_k.max()}     ps: {diff_ps.mean()}'  )
