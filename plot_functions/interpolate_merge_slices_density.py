import os, sys, time
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools')
from tools import *


input_dir  = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m0.5kev/slices_gas_density/'
output_dir = input_dir + 'interpolated/'
create_directory( output_dir )

slice_width = 1024
slice_depth = 256
slice_id = 1
slice_start = slice_id * slice_depth

print( 'Loading slices' )
slice_ids = range( 1, 97 )
n_slices = len(slice_ids)
z_vals, slices = [], []
time_start = time.time()
for n_slice,slice_id in enumerate( slice_ids ):
  file_name = input_dir + f'slice_{slice_id}_start{slice_start}_depth{slice_depth}.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  z_vals.append( z )
  slice = file['density'][0:slice_depth, :, :]
  slices.append( slice )
  file.close()
  print_progress( n_slice+1, n_slices, time_start )
print( '' )
  
z_vals = np.array( z_vals )  
a_vals = 1 / ( z_vals + 1 )

# z_vals

image_heigth, image_width = 1024,  1024*3
z_start, z_end = z_vals.max(), z_vals.min()
a_start, a_end = a_vals.min(), a_vals.max()
delta_z = ( z_end - z_start ) / image_width
delta_a = ( a_end - a_start ) / image_width
print( f'z_start: {z_start}  z_end: {z_end}  delta_z: {delta_z}')
# print( f'a_start: {a_start}  a_end: {a_end}  delta_a: {delta_a}')

image_data = np.zeros( (slice_depth, image_heigth, image_width ), dtype=np.float32 ) 
pixel_a, pixel_z = [], []
print( 'Merging slices' )
time_start = time.time()
for indx in range( image_width ):
  slice_indx = indx % slice_width
  a = a_start + ( indx + 0.5 ) * delta_a

  # id_l = np.where( a_vals <= a )[0][-1]
  # id_r = id_l + 1
  # a_l = a_vals[id_l]
  # a_r = a_vals[id_r]
  # alpha = ( a - a_l ) / ( a_r - a_l )
  # print( f'indx: {indx}  id_l: {id_l}  id_r: {id_r}  a: {a:.3f}   a_l: {a_l:.3f}   a_r: {a_r:.3f}   alpha:{alpha}    '    )

  z = z_start + ( indx + 0.5 ) * delta_z
  id_l = np.where( z_vals >= z )[0][-1]
  id_r = id_l + 1
  z_l = z_vals[id_l]
  z_r = z_vals[id_r]
  alpha = ( z - z_l ) / ( z_r - z_l )
  
  # print( f'indx: {indx}  id_l: {id_l}  id_r: {id_r}  z: {z:.3f}   z_l: {z_l:.3f}   z_r: {z_r:.3f}   alpha:{alpha}    '    )
  # time.sleep(0.05)

  pixel_a.append( a )
  pixel_z.append( z )

  slice_l = slices[id_l][:, :, slice_indx]
  slice_r = slices[id_r][:, :, slice_indx]
  slice_local = slice_l + alpha * ( slice_r - slice_l )
  image_data[:, :, indx] = slice_local

  print_progress( indx+1, image_width, time_start )

pixel_a = np.array( pixel_a )
pixel_z = np.array( pixel_z )
print('')


outfile_name = output_dir + f'interpolated_slice_start{slice_start}_ndepth{slice_depth}.h5'
outfile = h5.File( outfile_name, 'w' )
outfile.create_dataset( 'slice', data=image_data )
outfile.create_dataset( 'pixel_a', data=pixel_a )
outfile.create_dataset( 'pixel_z', data=pixel_z )
outfile.close()
print( f'Saved File: {outfile_name}' )


output_dir = output_dir + 'figures/'
create_directory( output_dir )


nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,10*nrows))

proj2 = (image_data**2).sum(axis=0)
proj = image_data.sum(axis=0)
proj = np.log10( proj2/proj )
# proj = np.log10( proj )
ax.imshow( proj, cmap='inferno' )

figure_name = output_dir + f'fig_density_slice_start{slice_start}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )

# 
