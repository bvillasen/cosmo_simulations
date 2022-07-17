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
from stats_functions import compute_distribution

# sim_dir = data_dir + 'cosmo_sims/wdm_sims/new/1024_25Mpc_cdm/'
sim_dir = data_dir + 'cosmo_sims/wdm_sims/new/1024_25Mpc_m4.0kev/'
input_dir = sim_dir + 'snapshot_files/'
output_dir = sim_dir + 'velocity_distribution/'
create_directory( output_dir )

Lbox = 25000.0    #kpc/h
n_cells = 1024
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
precision = np.float64
fields = [ 'density', 'momentum_x', 'momentum_y', 'momentum_z' ]
data_type = 'hydro'

# use_log = False
use_log = True

snap_ids = [ 6, 7, 8 ]
for snap_id in snap_ids:

  snap_data = load_snapshot_data_distributed( data_type, fields,  snap_id, input_dir,  box_size, grid_size, precision  )
  z = snap_data['Current_z']
  density = snap_data['density']
  vx = snap_data['momentum_x'] / density
  vy = snap_data['momentum_y'] / density
  vz = snap_data['momentum_z'] / density

  snap_data = None
  density = None

  velocity = np.sqrt( vx*vx + vy*vy + vz*vz )

  n_bins = 50
  distribution, centers = compute_distribution( velocity, n_bins=n_bins, log=use_log )
  data_out = { 'z':z, 'bin_centers':centers, 'distribution':distribution }

  file_name = output_dir + f'ps_velocity_{snap_id}'
  if use_log: file_name += '_log'
  file_name += '.pkl'
  Write_Pickle_Directory( data_out, file_name )




