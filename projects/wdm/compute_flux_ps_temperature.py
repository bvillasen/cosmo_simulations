import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import Load_Skewers_File, load_analysis_data
from calculus_functions import *
from stats_functions import compute_distribution
from data_optical_depth import data_optical_depth_Bosman_2021
from load_skewers import load_skewers_multiple_axis
from spectra_functions import Compute_Skewers_Transmitted_Flux
from flux_power_spectrum import Compute_Flux_Power_Spectrum

use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1
  
  
  
# sim_dir = data_dir + f'cosmo_sims/1024_25Mpc_wdm/cdm/'
sim_dir = data_dir + f'cosmo_sims/1024_25Mpc_wdm/m_2.0kev/'
input_dir = sim_dir + 'skewers_files/'
output_dir = sim_dir + 'flux_power_spectrum/'
if rank==0: create_directory( output_dir )

# Box parameters
Lbox = 25000.0 #kpc/h
box = {'Lbox':[ Lbox, Lbox, Lbox ] }


axis_list = [ 'x', 'y', 'z' ]
n_skewers_list = [ 'all', 'all', 'all']
skewer_ids_list = [ 'all', 'all', 'all']
field_list = [  'HI_density', 'los_velocity', 'temperature' ]

n_file = 25

temp_factors = [ 1.4, 1.2, 1.0, 0.8, 0.6 ]

temperature_factor = temp_factors[rank]
print( f'p_id: {rank}  temperature_factor: { temperature_factor}' )

skewer_dataset = Load_Skewers_File( n_file, input_dir, axis_list=axis_list, fields_to_load=field_list )

skewer_dataset['temperature'] *= temperature_factor

# Cosmology parameters
cosmology = {}
cosmology['H0'] = skewer_dataset['H0']
cosmology['Omega_M'] = skewer_dataset['Omega_M']
cosmology['Omega_L'] = skewer_dataset['Omega_L']
cosmology['current_z'] = skewer_dataset['current_z']


skewers_data = { field:skewer_dataset[field] for field in field_list }
data_Flux = Compute_Skewers_Transmitted_Flux( skewers_data, cosmology, box )

data_ps = Compute_Flux_Power_Spectrum( data_Flux )
k_vals = data_ps['k_vals']
skewers_ps = data_ps['skewers_ps']
ps_mean = data_ps['mean']

out_file_name = output_dir + f'ps_data_temperature_factor_{temperature_factor}.pkl'
Write_Pickle_Directory( data_ps, out_file_name )
