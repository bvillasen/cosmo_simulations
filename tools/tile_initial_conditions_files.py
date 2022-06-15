import sys, os, time
import numpy as np
import time
import h5py as h5
from tools import *

L_box = 1 
N = 16
n_ext = 23
N_out = N * n_ext
L_out = L_box * n_ext


root_dir   = data_dir + 'tiled_ics/'
input_dir  = root_dir + f'ics_{N}/'
output_dir = root_dir + f'ics_{N_out}/' 
create_directory( output_dir )


in_file_name = input_dir + f'ics_{L_box}Mpc_{N}_particles.h5'
print( f'Loading File: {in_file_name}' )
in_file = h5.File( in_file_name, 'r' )

out_file_name = output_dir + f'ics_{L_out}Mpc_{N_out}_particles.h5'
print( f'Writing File: {out_file_name}' )
out_file = h5.File( out_file_name, 'w' )

for key in in_file.attrs:
  if key == 'n_particles_local': continue
  if key == 'n_particles_total': continue
  out_file.attrs[key] = in_file.attrs[key]


for field_key in in_file.keys():
  print( f' Tiling field: {field_key}' )
  field_0 = in_file[field_key][...]
  tiled_field = []
  for i in range(n_ext):
    for j in range(n_ext):
      for k in range(n_ext):
        field = field_0.copy()
        if field_key == 'pos_x': field += i * L_box * 1e3
        if field_key == 'pos_y': field += j * L_box * 1e3
        if field_key == 'pos_z': field += k * L_box * 1e3  
        tiled_field.append( field )
  tiled_field = np.array( tiled_field ).flatten()
  out_file.create_dataset( field_key, data=tiled_field )

n_particles_local = tiled_field.shape[0]
out_file.attrs['n_particles_local'] = n_particles_local
out_file.attrs['n_particles_total'] = n_particles_local
print( f'N particles local: {n_particles_local}' )
out_file.close()
print( f'Saved File: {out_file_name}' )

# 
# in_file_name = input_dir + f'ics_{L_box}Mpc_{N}.h5'
# print( f'Loading File: {in_file_name}' )
# in_file = h5.File( in_file_name, 'r' )
# 
# out_file_name = output_dir + f'ics_{L_out}Mpc_{N_out}.h5'
# print( f'Writing File: {out_file_name}' )
# out_file = h5.File( out_file_name, 'w' )
# 
# for key in in_file.attrs:
#   out_file.attrs[key] = in_file.attrs[key]
# 
# for field_key in in_file.keys():
#   if field_key not in [ 'density', 'momentum_x',  'momentum_y',  'momentum_z', 'Energy', 'GasEnergy' ]: continue
#   print( f' Tiling field: {field_key}' )
#   field = in_file[field_key][...]
#   nx, ny, nz = field.shape
#   tiled_field = np.zeros( [ n_ext*nx, n_ext*ny, n_ext*nz ])
#   for i in range(n_ext):
#     for j in range(n_ext):
#       for k in range(n_ext):
#         tiled_field[i*nx:(i+1)*nx, j*ny:(j+1)*ny, k*nz:(k+1)*nz ] = field
# 
#   out_file.create_dataset( field_key, data=tiled_field)
# 
# out_file.close()
# print( f'Saved File: {out_file_name}' )
