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

use_mpi = False
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

args = sys.argv[1:]
data_type = args[0]

n_cells = 1024
L_Mpc = 25

sim_name = f'{n_cells}_{L_Mpc}Mpc_fragmentation/cdm'

base_dir = data_dir + f'cosmo_sims/'
sim_dir  = base_dir + f'{sim_name}/'
input_dir = sim_dir + 'snapshot_files/'
output_dir = sim_dir + 'power_spectrum_files/'
if rank == 0: create_directory( output_dir )


Lbox = L_Mpc * 1e3    #kpc/h
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
precision = np.float64
fields = [ 'density', 'temperature' ]

n_bins = 25
Lbox = Lbox/1000    #Mpc/h
nx, ny, nz = grid_size
dx, dy, dz = Lbox/nx, Lbox/ny, Lbox/nz


delta_max_vals = np.array([ 1000  ])
delta_max_local = split_array_mpi( delta_max_vals, rank, n_procs )

print( f'rank: {rank}  delta_local:{delta_max_local}' )

snap_id = 6

for snap_id in [ 6, 7, 8]:

  snap_data = load_snapshot_data_distributed( data_type, fields,  snap_id, input_dir,  box_size, grid_size, precision  )
  z = snap_data['Current_z']
  density = snap_data['density']
  temperature = snap_data['temperature']
  rho_mean = density.mean()
  nx, ny, nz = density.shape
  n_total = nx * ny * nz


  for delta_max in delta_max_local:
    dens = density.copy()
    
    file_name = output_dir + f'power_spectrum_{data_type}_{snap_id}_dens_max_{delta_max}.pkl'
    if os.path.isfile( file_name ):
      print( f'Skipping File: {file_name}' )
      continue
    
    
    dens_max = delta_max * rho_mean
    indices = ( dens >= dens_max ) * ( temperature < 1e5 )
    fraction = indices.sum() / n_total
    print( f"Delta max: {delta_max}   fraction: {fraction}") 
    dens[indices] = dens_max


    print( f'Computing Power Spectrum  snap_id: {snap_id}  z:{z}' )
    power_spectrum, k_vals, n_in_bin = get_power_spectrum( dens, Lbox, nx, ny, nz, dx, dy, dz,  n_kSamples=n_bins, fft_shift=False )
    sim_data = { 'z':z, 'k_vals':k_vals, 'power_spectrum':power_spectrum, 'n_in_bin':n_in_bin }


    Write_Pickle_Directory( sim_data, file_name )

