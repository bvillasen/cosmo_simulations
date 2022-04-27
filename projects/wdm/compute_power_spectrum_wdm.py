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

output_dir = data_dir + f'cosmo_sims/1024_25Mpc_wdm/power_spectrum_files/'
create_directory( output_dir )

# data_type = 'hydro'
data_type = 'particles'

snap_ids = [ 1, 2, 3]
print( snap_ids )
Lbox = 25000.0    #kpc/h
n_cells = 1024
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
precision = np.float64
fields = [ 'density' ]

n_bins = 25
Lbox = 25.0    #Mpc/h
nx, ny, nz = grid_size
dx, dy, dz = Lbox/nx, Lbox/ny, Lbox/nz


data_names = [ 'cdm', 'm_2.0kev', 'm_3.0kev', 'm_4.0kev', 'm_5.0kev' ]

for data_name in data_names:

  simulation_dir = data_dir + f'cosmo_sims/1024_25Mpc_wdm/{data_name}/'
  input_dir = simulation_dir + 'snapshot_files/'


  sim_data = {}

  for snap_id in snap_ids:
    snap_data = load_snapshot_data_distributed( data_type, fields,  snap_id, input_dir,  box_size, grid_size, precision  )
    z = snap_data['Current_z']
    density = snap_data['density']
    print( f'Computing Power Spectrum  snap_id: {snap_id}  z:{z}' )
    power_spectrum, k_vals, n_in_bin = get_power_spectrum( density, Lbox, nx, ny, nz, dx, dy, dz,  n_kSamples=n_bins )
    sim_data[snap_id] = { 'z':z, 'k_vals':k_vals, 'power_spectrum':power_spectrum, 'n_in_bin':n_in_bin }
    # break

  file_name = output_dir + f'power_spectrum_{data_type}_{data_name}.pkl'
  Write_Pickle_Directory( sim_data, file_name )

