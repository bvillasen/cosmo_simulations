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
from figure_functions import *
from stats_functions import compute_distribution, get_highest_probability_interval
from cosmology import Cosmology

use_mpi = False
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + 'data/flux_distribution_25Mpc/'
create_directory( output_dir )

# base_dir = data_dir + 'cosmo_sims/wdm_sims/50Mpc_boxes/'
base_dir = data_dir + 'cosmo_sims/wdm_sims/compare_wdm/'

axis_list = [ 'x', 'y', 'z' ]
n_skewers_list = [ 'all', 'all', 'all']
skewer_ids_list = [ 'all', 'all', 'all']
field_list = [ 'HI_density',  ]

n_bins = 80

files = [ 25, 29, 33 ]
# files = [ 29 ]

# names = [ 'cdm', 'wdm_m1.0kev', 'wdm_m2.0kev', 'wdm_m3.0kev', 'wdm_m4.0kev' ]
names = [ 'cdm', 'm1.0kev', 'm2.0kev', 'm3.0kev', 'm4.0kev' ]


flux_min = 1e-20

space = 'redshift'

for data_name in names:

  for n_file in files:

    sim_name = f'1024_25Mpc_{data_name}'
    input_dir = base_dir + sim_name + '/transmitted_flux/'
    # file_name = input_dir + f'lya_flux_{n_file:03}.h5'
    file_name = input_dir + f'lya_flux_{space}_{n_file:03}.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z']
    
    skewers_Flux = file['skewers_Flux'][...].flatten()
    file.close()
    
    skewers_Flux[ skewers_Flux<flux_min ] = flux_min
    
    flux = skewers_Flux
     
    v_min, v_max = 1e-3, 1
    n_samples = 150
    bin_edges = np.logspace( np.log10(v_min), np.log10(v_max), n_samples )
    # bin_edges = np.linspace( v_min, v_max, n_samples )
    distribution, bin_centers = compute_distribution( flux, edges=bin_edges, normalize_to_interval=False )
    
    F_mean = flux.mean()
    print( sim_name, F_mean )
    data_out = { 'z':z, 'distribution':distribution, 'bin_centers':bin_centers, 'F_mean':F_mean }
    file_name = output_dir + f'flux_distribution_{data_name}_{n_file}.pkl'
    Write_Pickle_Directory( data_out, file_name )


