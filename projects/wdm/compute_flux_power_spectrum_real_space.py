import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import Load_Skewers_File, load_analysis_data
from calculus_functions import *
from stats_functions import compute_distribution
from data_optical_depth import data_optical_depth_Bosman_2021
from load_skewers import load_skewers_multiple_axis
from spectra_functions import Compute_Skewers_Transmitted_Flux
from flux_power_spectrum import Compute_Flux_Power_Spectrum

base_dir = data_dir + 'cosmo_sims/wdm_sims/new/'
input_dir = base_dir + 'transmitted_flux/'
output_dir = base_dir + 'flux_power_spectrum/'
create_directory( output_dir )

snap_ids = [ 25, 29, 33 ]
# snap_ids = [ 10, 11, 12, 13, 14, 15 ]

base_dir = data_dir

base_dir = data_dir + 'cosmo_sims/wdm_sims/compare_wdm/'

# data_name = 'zero_temp'

data_name = 'vmax_100'

# data_name = 'vmin_50'

# data_name = 'temp_10'


sim_name = '1024_25Mpc_cdm'
input_dir  = base_dir + f'{sim_name}/transmitted_flux_{data_name}/'
output_dir = base_dir + f'{sim_name}/flux_power_spectrum_{data_name}/'
create_directory( output_dir )

for space in [ 'redshift', 'real']:

  for snap_id in snap_ids:
    
    data_name = f'{space}_{snap_id:03}'
    # data_name = f'{space}_{snap_id:03}_rescaled_tau'
    
    
    in_file_name = input_dir + f'lya_flux_{data_name}.h5'
    out_file_name = output_dir + f'flux_ps_{data_name}.h5'

    print( f'Loading File: {in_file_name}')
    file = h5.File( in_file_name, 'r' )
    current_z = file.attrs['current_z']
    vel_Hubble = file['vel_Hubble'][...]
    skewers_Flux = file['skewers_Flux'][...]
    file.close()

    data_Flux = { 'vel_Hubble':vel_Hubble, 'skewers_Flux':skewers_Flux }

    data_ps = Compute_Flux_Power_Spectrum( data_Flux )
    k_vals = data_ps['k_vals']
    skewers_ps = data_ps['skewers_ps']
    ps_mean = data_ps['mean']

    file = h5.File( out_file_name, 'w' )
    file.attrs['current_z'] = current_z
    file.create_dataset( 'k_vals', data=data_ps['k_vals'] )
    file.create_dataset( 'ps_mean', data=data_ps['mean'] )
    file.create_dataset( 'skewers_ps', data=data_ps['skewers_ps'] )
    file.close()
    print( f'Saved File: {out_file_name}' )

