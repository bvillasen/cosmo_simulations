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

output_dir = data_dir + f'cosmo_sims/1024_25Mpc_wdm/density_slices/'
create_directory( output_dir )

data_type = 'hydro'

snap_ids = [ 1, 2, 3]
print( snap_ids )

Lbox = 25000.0    #kpc/h
n_cells = 1024
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
precision = np.float64
fields = [ 'density' ]

slice_start = 0
slice_width = 256

data_names = [ 'cdm', 'm_2.0kev', 'm_3.0kev', 'm_4.0kev', 'm_5.0kev' ]

for data_name in data_names:

  simulation_dir = data_dir + f'cosmo_sims/1024_25Mpc_wdm/{data_name}/'
  input_dir = simulation_dir + 'snapshot_files/'

  for snap_id in snap_ids:
    snap_data = load_snapshot_data_distributed( data_type, fields,  snap_id, input_dir,  box_size, grid_size, precision  )
    z = snap_data['Current_z']
    temperature = snap_data['density']
    
    slice = temperature[slice_start:slice_start+slice_width,:,:]
    
    file_name = output_dir + f'slice_{data_name}_{snap_id}.h5' 
    file = h5.File( file_name, 'w' )
    file.attrs['current_z'] = z 
    file.create_dataset( 'slice', data=slice )
    file.close()
    print( f'Saved File: {file_name}')
    
    
    
    
