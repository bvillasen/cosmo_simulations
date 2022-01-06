import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *


output_dir = data_dir + 'cosmo_sims/rescaled_P19/wdm/figures/'
create_directory( output_dir )

simulation_dir = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_cdm/'
input_dir = simulation_dir + 'snapshot_files/'

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