import sys, os, time
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *

use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

# grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_nsim600/'
grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_cdm/'
fit_name = 'fit_results_P(k)+_Boera_covmatrix'
input_dir = grid_dir + f'fit_mcmc/{fit_name}/temperature_evolution/'
output_dir = grid_dir + f'fit_mcmc/{fit_name}/temperature_evolution/merged_files/'
if rank == 0: create_directory( output_dir )

# files = [ f for f in os.listdir(input_dir) if f[0] == 's' ]
# files.sort()
# n_files = len(files)
n_files = 4500000
if rank == 0:print( f'N files: {n_files}')

ids_global = np.arange(0, n_files, 1, dtype=int)
ids_local = split_array_mpi( ids_global, rank, n_procs )
n_local = len( ids_local )
print( f'proc_id: {rank}  n_local: {n_local}' )
selected_files = ids_local
n_samples = len( selected_files )


# 
# z_vals = None
# T0_vals = []
# time_start = time.time()
# for sim_id,file_id in enumerate(selected_files):
#   file_name = input_dir + f'solution_{file_id}.h5'
#   file = h5.File( file_name, 'r' )
#   if z_vals is None: z_vals = file['z'][...]
#   T0 = file['temperature'][...]
#   file.close()
#   T0_vals.append( T0 )
#   if sim_id %100 == 0: print_progress( sim_id, n_samples, time_start )
# print('\n')
# T0_vals = np.array( T0_vals )
# 
# out_file_name = output_dir + f'samples_T0_evolution_id_{rank}.h5'
# out_file = h5.File( out_file_name, 'w' )
# out_file.create_dataset('selected_files', data=selected_files )
# out_file.create_dataset( 'z', data=z_vals )
# out_file.create_dataset( 'T0', data=T0_vals )
# out_file.close()
# print( f'Saved File: {out_file_name}' )
# 
