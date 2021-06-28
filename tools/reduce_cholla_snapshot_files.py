import sys, os, time
import numpy as np
import time
import h5py as h5
from tools import *

use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

data_type = 'hydro'
# data_type = 'particles'

data_dir = '/gpfs/alpine/csc434/proj-shared/cholla/'
root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim256/'
output_dir = data_dir + 'cosmo_sims/rescaled_P19/2048_50Mpc/reduced_snapshot_files/'
if rank == 0: create_directory( output_dir )

input_dir = root_dir + f'snapshot_files_{data_type}/'
snapshot_dirs = os.listdir( input_dir ) 


