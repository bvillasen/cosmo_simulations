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
output_dir = proj_dir + 'data/density_distribution/'
create_directory( output_dir )

base_dir = data_dir + 'cosmo_sims/wdm_sims/50Mpc_boxes/'

axis_list = [ 'x', 'y', 'z' ]
n_skewers_list = [ 'all', 'all', 'all']
skewer_ids_list = [ 'all', 'all', 'all']
field_list = [ 'density',  ]

cosmo = Cosmology()

n_bins = 200

files = [ 25, 29, 33 ]
names = [ 'cdm', 'wdm_m1.0kev', 'wdm_m2.0kev', 'wdm_m3.0kev', 'wdm_m4.0kev' ]

for data_name in names:

  for n_file in files:

    sim_name = f'1024_50Mpc_{data_name}'
    input_dir = base_dir + sim_name + '/skewers_files/'
    skewer_dataset = Load_Skewers_File( n_file, input_dir, axis_list=axis_list, fields_to_load=field_list )
    z = skewer_dataset['current_z']
    density = skewer_dataset['density']

    overdensity = density / cosmo.rho_gas_mean

    v_min, v_max = 0.001, 2e4
    n_samples = 500
    bin_edges = np.logspace( np.log10(v_min), np.log10(v_max), n_samples )
    distribution, bin_centers = compute_distribution( overdensity, edges=bin_edges, normalize_to_interval=True )

    data_out = { 'z':z, 'distribution':distribution, 'bin_centers':bin_centers }
    file_name = output_dir + f'density_distribution_{data_name}_{n_file}.pkl'
    Write_Pickle_Directory( data_out, file_name )


