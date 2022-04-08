import os, sys, time
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools')
from tools import *

input_dir  = data_dir + 'cosmo_sims/2048_50Mpc_V22/slices_temperature/'
output_dir = input_dir

slice_width = 2048
slice_depth = 128

n_slices = 33
slices_ids = range( n_slices )
z_vals, slices = [], []
for slice_id in slices_ids:
  print( f' {slice_id} / {len(slices_ids)} ' )
  file_name = input_dir + f'slice_hydro_{slice_id}.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  slice = file['temperature'][0:slice_depth, :, :]
  slices.append( slice )
  z_vals.append( z )
z_vals = np.array( z_vals )  

  
image_heigth, image_width = 2048,  2048* 5
z_start, z_end = 2, 9
delta_z = ( z_end - z_start ) / image_width

image_data = np.zeros( (slice_depth, image_heigth, image_width ), dtype=np.float32 ) 
pixel_z = []
time_start = time.time()
for indx in range( image_width ):
  z = z_start + ( indx + 0.5 ) * delta_z
  id_l = np.where( z_vals <= z )[0][-1]
  id_r = id_l + 1
  slice_indx = indx % slice_width
  slice_l = slices[id_l][:, :, slice_indx]
  slice_r = slices[id_r][:, :, slice_indx]
  z_l = z_vals[id_l]
  z_r = z_vals[id_r]
  alpha = ( z - z_l ) / ( z_r - z_l )
  slice_local = slice_l + alpha * ( slice_r - slice_l )
  image_data[:, :, indx] = slice_local
  pixel_z.append( z )
  print_progress( indx+1, image_width, time_start )
pixel_z = np.array( pixel_z )


outfile_name = output_dir + f'interpolated_slice_ndepth{slice_depth}.h5'
outfile = h5.File( outfile_name, 'w' )
outfile.create_dataset( 'slice', data=image_data )
outfile.create_dataset( 'pixel_z', data=pixel_z )
outfile.close()
print( f'Saved File: {outfile_name}' )
  
nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,10*nrows))

proj2 = (image_data**2).sum(axis=0)
proj = image_data.sum(axis=0)
proj = np.log10( proj2/proj )
proj = np.log10( proj )
ax.imshow( proj, cmap= 'jet' )

figure_name = output_dir + f'fig_temperature_slice.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
   
  
