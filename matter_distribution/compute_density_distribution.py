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

output_dir = data_dir + f'cosmo_sims/rescaled_P19/wdm/density_distribution_files/'
create_directory( output_dir )


snap_ids = [ 1, 4, 8, 13, 23, 42 ]
print( snap_ids )
Lbox = 50000.0    #kpc/h
n_cells = 1024
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
precision = np.float32
fields = [ 'density' ]

dens_min, dens_max = -3, 4
n_bins = 100
data_type = 'hydro'

wdm_masses = [ 0.25, 0.5, 1.0, 2.0, 3.0 ]

for wdm_mass in wdm_masses:

  # sim_name = 'cdm'
  sim_name = f'wdm_{wdm_mass}kev'
  simulation_dir = data_dir + f'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_{sim_name}/'
  input_dir = simulation_dir + 'snapshot_files/'


  sim_data = {}

  snap_id = snap_ids[0]
  for snap_id in snap_ids:
    snap_data = load_snapshot_data_distributed( data_type, fields,  snap_id, input_dir,  box_size, grid_size, precision  )
    z = snap_data['Current_z']
    density = snap_data['density']
    dens_mean = density.mean()
    log_density = np.log10(density/dens_mean)
    # bin_edges = np.linspace( log_density.min(), log_density.max(), n_bins )
    bin_edges = np.linspace( dens_min, dens_max, n_bins )
    hist, bin_edges = np.histogram( log_density, bins=bin_edges )
    distribution = hist / hist.sum()
    bin_centers = ( bin_edges[1:] + bin_edges[:-1] ) / 2
    sim_data[snap_id] = { 'z':z, 'bin_centers':bin_centers, 'distribution':distribution }
    # break
    
  file_name = output_dir + f'density_distribution_{sim_name}.pkl'
  Write_Pickle_Directory( sim_data, file_name )

