import sys, os, time
import numpy as np
import time
import h5py as h5
from tools import *
from shutil import copyfile

input_dir  = data_dir + f'cosmo_sims/2048_50Mpc_V22/slices_temperature/'
output_dir = input_dir + 'selected_slices/'
create_directory( output_dir )

slice_start, slice_depth = 384, 128

snap_ids = range(170)
z_vals = []
for snap_id in snap_ids:
  file_name = input_dir + f'slice_hydro_{snap_id}_start{slice_start}_depth{slice_depth}.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  z_vals.append( z )
z_vals = np.array( z_vals )

selected_z = np.arange( 2, 10.1, 0.25 )
selected_snaps = []
for z in selected_z:
  diff = np.abs( z_vals - z )
  indx = np.where( diff == diff.min() )[0][0]
  selected_snaps.append( indx )

for indx, snap_id in enumerate(selected_snaps):
  print( f' {indx}  {len(selected_snaps)}' )
  src_file = input_dir  + f'slice_hydro_{snap_id}_start{slice_start}_depth{slice_depth}.h5'
  dst_file = output_dir + f'slice_hydro_{indx}.h5'
  copyfile( src_file, dst_file )
  











