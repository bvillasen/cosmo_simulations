import sys, os, time
import numpy as np
import time
import h5py as h5
from tools import *

data_dir = '/data/groups/comp-astro/bruno/'
input_dir  = data_dir + 'cosmo_sims/rescaled_P19/2048_50Mpc/slices_temperature/'
output_dir = input_dir + 'selected_slices/'
create_directory( output_dir )

slice_start, slice_depth = 384, 128

snap_ids = np.range(170)
z_vals = []
for snap_id in snap_ids:
  file_name = input_dir + f'slice_hydro_{snap_id}_start{slice_start}_depth{slice_depth}.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  z_vals.append( z )
z_vals = np.array( z_vals )