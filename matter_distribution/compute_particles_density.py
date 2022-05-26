import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
import pycuda
import pycuda.driver as cuda
from pycuda.compiler import SourceModule
import pycuda.gpuarray as gpuarray
from cudaTools import setCudaDevice


n_grid = 1024
L_Mpc = 10

# sim_name = f'{n_grid}_{L_Mpc}Mpc_dmo_cdm'
# sim_name = f'{n_grid}_{L_Mpc}Mpc_dmo_m3.0kev'

sim_name = f'2048_{L_Mpc}Mpc_dmo_cdm'
# sim_name = f'2048_{L_Mpc}Mpc_dmo_m3.0kev'

input_dir = data_dir + f'cosmo_sims/wdm_sims/{sim_name}/snapshot_files/'
output_dir = data_dir + f'cosmo_sims/wdm_sims/{sim_name}/density_files/'
create_directory( output_dir )

snap_id = 0


#Grid parameters
L_box = L_Mpc * 1e3
dx = L_box / n_grid

# n_boxes = 128
n_boxes = 1024
box_ids = range(n_boxes) 

#Select CUDA Device
useDevice = 0
#initialize pyCUDA context
cudaDevice = setCudaDevice( devN=useDevice, usingAnimation=False )

cudaCodeFile = open( 'cuda_kernels.cu', 'r')
cudaCodeString = cudaCodeFile.read()
cudaCodeStringComplete = cudaCodeString
cudaCode = SourceModule(cudaCodeStringComplete, no_extern_c=True, include_dirs=[] )
get_density_CIC_kernel = cudaCode.get_function("Get_Density_CIC_Kernel")
get_density_TSC_kernel = cudaCode.get_function("Get_Density_TSC_Kernel")

nx , ny, nz = n_grid, n_grid, n_grid
dx = L_box / nx
dy, dz = dx, dx
xMin, yMin, zMin = 0, 0, 0
xMax, yMax, zMax = L_box, L_box, L_box

density_types = [ 'cic', 'tsc' ]

for density_type in density_types:

  if density_type == 'cic': get_density_kernel = get_density_CIC_kernel
  if density_type == 'tsc': get_density_kernel = get_density_TSC_kernel



  n_ghost = 1
  n_total = n_grid + 2*n_ghost  
  density = np.zeros( [n_total, n_total, n_total])
  d_density = gpuarray.to_gpu( density.astype(np.float64) )

  start = time.time()
  for box_id in box_ids:
    
    file_name = input_dir + f'{snap_id}_particles.h5.{box_id}'
    file = h5.File( file_name, 'r' )
    current_z = file.attrs['current_z'][0]
    particle_mass = file.attrs['particle_mass'][0]
    pos_x = file['pos_x'][...]
    pos_y = file['pos_y'][...]
    pos_z = file['pos_z'][...]
    file.close()
    N_particles = len(pos_x)
    
    #set thread grid for CUDA kernels
    block_size = 512
    block1D = ( block_size, 1,  1)
    grid_size = ( N_particles - 1 ) // block_size + 1
    grid1D = ( grid_size, 1, 1 )

    dev_free, dev_total = pycuda.driver.mem_get_info()
    # print( f'Box id: {box_id}   GPU memory: {dev_free} / {dev_total}')

    d_pos_x = gpuarray.to_gpu( pos_x.astype(np.float64) )
    d_pos_y = gpuarray.to_gpu( pos_y.astype(np.float64) )
    d_pos_z = gpuarray.to_gpu( pos_z.astype(np.float64) )

    get_density_kernel( np.int32( N_particles),  np.float64(particle_mass), d_density, d_pos_x, d_pos_y, d_pos_z,
                        np.float64(xMin), np.float64(yMin), np.float64(zMin),
                        np.float64(xMax), np.float64(yMax), np.float64(zMax), 
                        np.float64(dx), np.float64(dy), np.float64(dz),
                        np.int32(nx), np.int32(ny), np.int32(nz), np.int32(n_ghost),  grid=grid1D, block=block1D )
                        
    print_progress( box_id+1, n_boxes, start)


  density = d_density.get()
  density[1,:,:] += density[-1,:,:]
  density[-2,:,:] += density[0,:,:]
  density[:,1,:] += density[:,-1,:]
  density[:,-2,:] += density[:,0,:]
  density[:,:,1] += density[:,:,-1]
  density[:,:,-2] += density[:,:,0]
  density = density[1:-1,1:-1,1:-1]

  print( f'Density  mean: {density.mean()}    min: {density.min()}    max: {density.max()} ')

  out_file_name = output_dir + f'density_{density_type}_{snap_id}.h5'
  file = h5.File( out_file_name, 'w' )
  file.attrs['current_z'] = current_z
  file.create_dataset( 'density', data=density )
  file.close()

  print( f'Saved File: {out_file_name}' )


