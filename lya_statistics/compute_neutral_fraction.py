import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
#Append analysis directories to path
extend_path()
from constants_cosmo import G_COSMO
from load_data import load_snapshot_data_distributed

use_mpi = False
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

input_dir  = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_high_z/snapshot_files/'
output_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_high_z/neutral_fraction/'
if rank == 0: create_directory( output_dir )


# Box parameters
n_points = 1024
Lbox = 50000.0  #kpc/h
grid_size = [ n_points, n_points, n_points ]
box_size = [ Lbox, Lbox, Lbox ]

# Data parameters
data_type = 'hydro'
precision = np.float32
fields = ['density', 'HI_density']


H0 = 67.66
Omega_b =  0.0497 
h = H0 / 100
X = 0.75984603480
rho_crit =  3*(H0*1e-3)**2/(8*np.pi*G_COSMO)/ h**2
rho_gas_mean = rho_crit * Omega_b 
dens_max = 1.2 * rho_gas_mean
dens_min = 0.8 * rho_gas_mean

z_vals, HI_frac_mean = [], []

for n_file in range(2):
  n_snap = n_file + 1
  data = load_snapshot_data_distributed( data_type, fields,  n_snap, input_dir, box_size, grid_size, precision )
  z = data['Current_z']
  dens = data['density']
  HI_dens = data['HI_density']
  indices = ( dens > dens_min ) * ( dens < dens_max )
  dens = dens[indices]
  HI_dens = HI_dens[indices]
  H_dens  = dens * X
  HI_frac = HI_dens / H_dens
  z_vals.append( z )
  HI_frac_mean.append( HI_frac.mean() ) 
  
  
data_out = np.array( [ z_vals, HI_frac_mean ])  
file_name = output_dir + 'neutral_fraction_data.txt'
np.savetxt( file_name, data_out )
print( f'Saved File: {file_name}' )
 








