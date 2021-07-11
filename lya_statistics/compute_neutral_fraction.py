import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
cwd = os.getcwd()
cosmo_dir = cwd[: cwd.find('simulation_analysis')] + 'simulation_analysis/'
tools_dir = cosmo_dir + 'tools'
sys.path.append( tools_dir )
from tools import *
#Append analysis directories to path
extend_path()
from constants_cosmo import G_COSMO

use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

# data_dir = '/home/bruno/Desktop/data/'
# data_dir = '/home/bruno/Desktop/ssd_0/data/'
# data_dir = '/raid/bruno/data/'
data_dir = '/data/groups/comp-astro/bruno/'
# data_dir = '/gpfs/alpine/csc434/scratch/bvilasen/'
input_dir  = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_high_z/snapshot_files/'
output_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_high_z/neutral_fraction/'
if rank == 0: create_directory( output_dir )


fields = ['density', 'HI_density']

n_file = 0 





