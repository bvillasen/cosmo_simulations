import os, sys, time
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools')
from tools import *

input_dir  = data_dir + 'render_images/wdm_slice/slices/'
output_dir = data_dir + 'render_images/wdm_slice/slices/'
create_directory( output_dir )

slice_start, slice_depth = 512, 512

m_wdm_vals = [ 0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0 ]
file_names = [ f'interpolated_slice_mwdm{m_wdm}_start{slice_start}_ndepth{slice_depth}.h5' for m_wdm in m_wdm_vals  ]
file_names.append( f'interpolated_slice_cdm_start{slice_start}_ndepth{slice_depth}.h5' )

m_cdm = 5 
m_wdm_vals.append( m_cdm )
m_wdm_vals = np.array( m_wdm_vals )
inv_mass = 1 / m_wdm_vals


slices = []
for file_name in file_names: 
  file_name = input_dir + file_name
  print( f'Loading: {file_name}' )
  file = h5.File( file_name, 'r' ) 
  pixel_z = file['pixel_z'][...]
  slice = file['slice']
  slice_shape = slice.shape
  print( f'shape: {slice_shape}' )
  slices.append( file['slice'][...] )
  file.close()


nz, ny, nx = slice_shape
image_width = nx
image_depth = nz
image_heigth =  2048 + 256 + 128 + 128
image_data = np.zeros( (image_depth, image_heigth, image_width ), dtype=np.float32 )

m_vals = inv_mass
m_start = m_vals[0]
m_end = m_vals[-1]
delta_m = ( m_end - m_start ) / image_heigth

print( 'Merging slices' )
y_offset = -128
time_start = time.time()
for indx in range( image_heigth ):
  slice_indx = (indx + y_offset) % ny
  m = m_start + (indx + 0.5) * delta_m
  id_l = np.where( m_vals >= m )[0][-1]
  id_r = id_l + 1
  m_l = m_vals[id_l]
  m_r = m_vals[id_r]
  alpha = ( m - m_l ) / ( m_r - m_l )

  # print( f'indx: {indx} id_l: {id_l}  id_r: {id_r}  m: {m:.2f}  m_l: {m_l:.2f}  m_r: {m_r:.2f}  alpha: {alpha}' )
  # time.sleep(0.01)

  slice_l = slices[id_l][:, slice_indx, :]
  slice_r = slices[id_r][:, slice_indx, :]
  image_data[:, indx, :] = slice_l + alpha * ( slice_r - slice_l )

  print_progress( indx+1, image_heigth, time_start )

# image_data = np.flip( image)

print('')

outfile_name = output_dir + f'interpolated_slice_wdm_extended_new.h5'
outfile = h5.File( outfile_name, 'w' )
outfile.create_dataset( 'slice', data=image_data )
outfile.create_dataset( 'pixel_z', data=pixel_z )
outfile.close()
print( f'Saved File: {outfile_name}' )
