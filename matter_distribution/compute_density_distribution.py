import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import load_snapshot_data_distributed


wdm_masses = [ 0.25, 0.5, 1.0, 2.0, 3.0 ]

for wdm_mass in wdm_masses:

  # simulation_dir = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_cdm/'
  simulation_dir = data_dir + f'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m{wdm_mass}kev/'
  input_dir = simulation_dir + 'snapshot_files/'
  output_dir = simulation_dir


  snap_ids = np.arange( 1, 99, 1, dtype=int )
  snaps_z = []
  for snap_id in snap_ids:
    file_name = input_dir + f'{snap_id}.h5.0'
    file = h5.File( file_name, 'r' )
    z = file.attrs['Current_z'][0]
    snaps_z.append(z)
    file.close()
  snaps_z = np.array(snaps_z)

  z_vals = [ 6, 5, 4, 3, 2, 1 ]
  snap_indices = []
  for z in z_vals:
    z_diff = np.abs( snaps_z - z )
    z_diff_min = z_diff.min()
    if z_diff_min > 0.1: print( f'WARNING: Large z_diff_min: {z_diff_min}' )
    snap_id = np.where( z_diff == z_diff_min )[0][0]
    snap_indices.append( snap_id )
  snap_indices = np.array( snap_indices )

  snap_ids = snap_ids[snap_indices]

  Lbox = 50000.0    #kpc/h
  n_cells = 1024
  box_size = [ Lbox, Lbox, Lbox ]
  grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
  precision = np.float32
  fields = [ 'density' ]
  n_bins = 50

  data_type = 'hydro'

  sim_data = {}

  snap_id = snap_ids[0]
  for snap_id in snap_ids:
    snap_data = load_snapshot_data_distributed( data_type, fields,  snap_id, input_dir,  box_size, grid_size, precision  )
    z = snap_data['Current_z']
    density = snap_data['density']
    dens_mean = density.mean()
    log_density = np.log10(density/dens_mean)
    bin_edges = np.linspace( log_density.min(), log_density.max(), n_bins )
    hist, bin_edges = np.histogram( log_density, bins=bin_edges )
    distribution = hist / hist.sum()
    bin_centers = ( bin_edges[1:] - bin_edges[:-1] ) / 2
    sim_data[snap_id] = { 'z':z, 'bin_centers':bin_centers, 'distribution':distribution }

  file_name = output_dir + 'density_distribution.pkl'
  Write_Pickle_Directory( sim_data, file_name )

