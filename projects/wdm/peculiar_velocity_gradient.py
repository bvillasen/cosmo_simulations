import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from constants_cosmo import Mpc, kpc
from load_data import Load_Skewers_File, load_analysis_data
from calculus_functions import *
from stats_functions import compute_distribution
from data_optical_depth import data_optical_depth_Bosman_2021
from load_skewers import load_skewers_multiple_axis
from spectra_functions import Compute_Skewers_Transmitted_Flux
from flux_power_spectrum import Compute_Flux_Power_Spectrum
from cosmology import Cosmology
from spectra_functions import extend_periodic

use_mpi = False
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

base_dir = data_dir + 'cosmo_sims/wdm_sims/compare_wdm/'

# Box parameters
Lbox = 25000.0 #kpc/h
N = 1024
dx = Lbox / N
box = {'Lbox':[ Lbox, Lbox, Lbox ] }


axis_list = [ 'x', 'y', 'z' ]
n_skewers_list  = [ 'all', 'all', 'all']
skewer_ids_list = [ 'all', 'all', 'all']
field_list = [ 'HI_density', 'los_velocity', 'temperature' ]


sim_name = '1024_25Mpc_cdm'
sim_dir = base_dir + sim_name + '/'
input_dir  = sim_dir + 'skewers_files/'
output_dir = sim_dir + 'transmitted_flux_vel_grad/'
create_directory( output_dir )

snap_ids =  [ 25, 29, 33 ]
# for snap_id in snap_ids:
snap_id = 33

n_skewers = 1 
  
# for space in [ 'real', 'redshift']:
space = 'real'
space = 'redshift'

skewer_dataset = Load_Skewers_File( snap_id, input_dir, axis_list=axis_list, fields_to_load=field_list )
cosmology = {}
cosmology['H0'] = skewer_dataset['H0']
cosmology['Omega_M'] = skewer_dataset['Omega_M']
cosmology['Omega_L'] = skewer_dataset['Omega_L']
cosmology['current_z'] = skewer_dataset['current_z']
skewers_data = { field:skewer_dataset[field][:n_skewers] for field in field_list }
current_z = cosmology['current_z']
current_a = 1 / ( current_z + 1 )



cosmo = Cosmology()
H = cosmo.get_Hubble( current_a ) 
Mpc_km = Mpc / 1e3
kpc_km = kpc / 1e3

H /= Mpc_km

dr = dx * current_a / cosmo.h # proper in kpc
dr *= kpc_km 


skewers_vel_peculiar = skewer_dataset['los_velocity'] # km/s


skewer_id = 0 
vel_peculiar = skewers_vel_peculiar[skewer_id]

n_ghost = int( 0.1 * N )
vel_peculiar = extend_periodic( vel_peculiar, n_ghost )

grad_vpec = np.zeros_like( vel_peculiar )
grad_vpec[1:-1] = ( vel_peculiar[2:] - vel_peculiar[:-2] ) / ( 2 * dr )
grad_vpec[0]    = ( vel_peculiar[1]  - vel_peculiar[0]  ) / (  dr )
grad_vpec[-1]   = ( vel_peculiar[-1] - vel_peculiar[-2]  ) / ( dr )




# 
# out_file_name = output_dir + f'lya_flux_{space}_{snap_id:03}.h5'
# file = h5.File( out_file_name, 'w' )
# file.attrs['current_z'] = skewer_dataset['current_z']
# file.attrs['Flux_mean'] = data_Flux_cdm['Flux_mean']
# file.create_dataset( 'vel_Hubble', data=data_Flux_cdm['vel_Hubble'] )
# file.create_dataset( 'skewers_Flux', data=data_Flux_cdm['skewers_Flux'] )
# file.close()
# print( f'Saved File: {out_file_name}')
# 
