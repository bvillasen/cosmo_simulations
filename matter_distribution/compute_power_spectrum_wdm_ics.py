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
from power_spectrum_functions import get_power_spectrum


n_cells = 1024
L_Mpc = 10

# sim_name = f'{n_cells}_{L_Mpc}Mpc_dmo_cdm'
# sim_name = f'{n_cells}_{L_Mpc}Mpc_dmo_m3.0kev'

sim_name = f'2048_{L_Mpc}Mpc_dmo_cdm'
# sim_name = f'2048_{L_Mpc}Mpc_dmo_m3.0kev'


base_dir = data_dir + 'cosmo_sims/wdm_sims/'
sim_dir  = base_dir + f'{sim_name}/'
input_dir = sim_dir + 'density_files/'
output_dir = sim_dir + 'power_spectrum_files/'
create_directory( output_dir )

# data_type = 'hydro'
data_type = 'particles'


Lbox = L_Mpc * 1e3    #kpc/h
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
precision = np.float64
fields = [ 'density' ]

n_bins = 25
Lbox = Lbox/1000    #Mpc/h
nx, ny, nz = grid_size
dx, dy, dz = Lbox/nx, Lbox/ny, Lbox/nz

snap_id = 0

density_types = [ 'cic', 'tsc' ]

for density_type in density_types:

  file_name = input_dir + f'density_{density_type}_{snap_id}.h5'
  print( f'Loading File: {file_name}' )
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  density = file['density'][...]
  print( f'Computing Power Spectrum  snap_id: {snap_id}  z:{z}' )
  power_spectrum, k_vals, n_in_bin = get_power_spectrum( density, Lbox, nx, ny, nz, dx, dy, dz,  n_kSamples=n_bins, fft_shift=False )
  sim_data = { 'z':z, 'k_vals':k_vals, 'power_spectrum':power_spectrum, 'n_in_bin':n_in_bin }

  file_name = output_dir + f'power_spectrum_{data_type}_{density_type}_{snap_id}.pkl'
  Write_Pickle_Directory( sim_data, file_name )

