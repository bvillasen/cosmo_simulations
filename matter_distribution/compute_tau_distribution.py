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

output_dir = data_dir + f'cosmo_sims/rescaled_P19/wdm/tau_distribution_files/'
create_directory( output_dir )


snap_ids = [ 15, 25, 35, 45, 55 ]
print( snap_ids )
Lbox = 50000.0    #kpc/h
n_cells = 1024
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
precision = np.float32
fields = [ 'density' ]

dens_min, dens_max = -3, 4
n_bins = 200
data_type = 'hydro'

wdm_masses = [ 0.25, 0.5, 1.0, 2.0, 3.0 ]

# for wdm_mass in wdm_masses:

sim_name = 'cdm'
# sim_name = f'wdm_m{wdm_mass}kev'
simulation_dir = data_dir + f'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_{sim_name}/'
input_dir = simulation_dir + 'skewers_files/transmitted_flux/'

F_min, F_max, n_bins_F = 0, 1, 50
F_bins = np.linspace( F_min, F_max, n_bins_F  )

tau_min, tau_max, n_bins_tau = 0.1, 6, 50
tau_bins = np.linspace( tau_min, tau_max, n_bins_tau  )

sim_data = {}
flux_min = 1e-10

snap_id = snap_ids[0]
for snap_id in snap_ids:
  sim_data[snap_id] = {}
  file_name = input_dir + f'lya_flux_{snap_id:03}.h5'
  print( f'Loadig File: {file_name}' )
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  vel_hubble = file['vel_Hubble'][...]
  skewers_flux = file['skewers_Flux'][...]
  file.close()
  skewers_flux[skewers_flux < flux_min] = flux_min
  F_mean = skewers_flux.mean()
  sim_data[snap_id]['z'] = z
  
  hist, bin_edges = np.histogram( skewers_flux, bins=F_bins )
  bin_centers = ( bin_edges[1:] + bin_edges[:-1] ) / 2
  sim_data[snap_id]['flux'] = { 'bin_centers':bin_centers, 'distribution':hist, 'mean':F_mean }
  print( 'Saved mean Flux')
  
  skewers_tau = -np.log( skewers_flux )
  hist, bin_edges = np.histogram( skewers_tau, bins=tau_bins )
  bin_centers = ( bin_edges[1:] + bin_edges[:-1] ) / 2
  sim_data[snap_id]['tau'] = { 'bin_centers':bin_centers, 'distribution':hist }
  


file_name = output_dir + f'tau_distribution_{sim_name}.pkl'
Write_Pickle_Directory( sim_data, file_name )

