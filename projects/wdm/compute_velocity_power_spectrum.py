import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import load_snapshot_data_distributed
from power_spectrum_functions import get_power_spectrum

use_mpi = False
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

# sim_dir = data_dir + 'cosmo_sims/wdm_sims/new/1024_25Mpc_cdm/'
sim_dir = data_dir + 'cosmo_sims/wdm_sims/new/1024_25Mpc_m4.0kev/'
input_dir = sim_dir + 'snapshot_files/'
output_dir = sim_dir + 'velocity_power_spectrum/'
create_directory( output_dir )

Lbox = 25000.0    #kpc/h
n_cells = 1024
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
precision = np.float64
fields = [ 'density', 'momentum_x', 'momentum_y', 'momentum_z' ]
data_type = 'hydro'

snap_ids = [ 6, 7, 8 ]

for snap_id in snap_ids:

  snap_data = load_snapshot_data_distributed( data_type, fields,  snap_id, input_dir,  box_size, grid_size, precision  )
  z = snap_data['Current_z']
  density = snap_data['density']
  vx = snap_data['momentum_x'] / density
  vy = snap_data['momentum_y'] / density
  vz = snap_data['momentum_z'] / density
  velocity = np.sqrt( vx*vx + vy*vy + vz*vz )

  L = Lbox / 1e3
  nx, ny, nz = n_cells, n_cells, n_cells
  dx, dy, dz = L/nx,  L/ny,  L/nz

  n_bins = 25
  print( f'Computing Power Spectrum  snap_id: {snap_id}  z:{z}' )
  power_spectrum, k_vals, n_in_bin = get_power_spectrum( velocity, Lbox, nx, ny, nz, dx, dy, dz,  n_kSamples=n_bins )
  sim_data = { 'z':z, 'k_vals':k_vals, 'power_spectrum':power_spectrum, 'n_in_bin':n_in_bin }

  file_name = output_dir + f'power_spectrum_velocity_{snap_id}.pkl'
  Write_Pickle_Directory( sim_data, file_name )

