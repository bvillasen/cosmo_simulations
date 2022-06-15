import os, sys
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from cholla_parameter_file import write_parameter_file
from system_job_scripts import create_job_script_crusher

root_dir =  data_dir + 'scaling/cruser_368/'
params_dir = root_dir + 'param_files/'
create_directory( root_dir )
create_directory( params_dir )

tile_size = 368
tile_length = 23000.0 #kpc/h
work_dir = '/gpfs/alpine/csc380/proj-shared/cholla/scaling/crusher_368/'
dir_ics  = work_dir + 'ics/'
dir_snap = work_dir + 'snapshot_files/'
outputs_file = '/ccs/home/bvilasen/cholla_scaling/scale_output_files/outputs_single_output_z5.txt'
uvb_file = work_dir + 'uvb_rates_V22.txt'

# n_procs_list = [ 8, 16, 32 ]
n_procs_list = [ 8, 16, 32, 64, 128, 256, 512 ]
time = '00:20:00'

n_sims = len( n_procs_list)
n_nodes = int( ( max(n_procs_list) - 1 ) / 8 ) + 1 

job_params = {}
job_params['project'] = 'CSC380'
job_params['name'] = 'scaling_test'
job_params['n_nodes'] = n_nodes 
job_params['time'] = time
job_params['n_mpi_list'] = n_procs_list
job_params['dir_work'] = work_dir 
job_params['dir_bin'] = work_dir + 'bin'
job_params['bin_name'] = 'cholla.cosmology.frontier'
job_params['partition'] = 'batch'


job_file_name = root_dir + 'submit_job_crusher'
job_script = create_job_script_crusher( job_params, file_name=job_file_name  )

for n_procs in n_procs_list:
  file_name = params_dir + f'param_{n_procs}.txt'

  if n_procs == 8: proc_grid = [ 2, 2, 2 ]
  elif n_procs == 16: proc_grid = [ 4, 2, 2 ]
  elif n_procs == 32: proc_grid = [ 4, 4, 2 ]
  elif n_procs == 64: proc_grid = [ 4, 4, 4 ]
  elif n_procs == 128: proc_grid = [ 8, 4, 4 ]
  elif n_procs == 256: proc_grid = [ 8, 8, 4 ]
  elif n_procs == 512: proc_grid = [ 8, 8, 8 ]
  elif n_procs == 1024: proc_grid = [ 16, 8, 8 ]
  elif n_procs == 2048: proc_grid = [ 16, 16, 8 ]
  elif n_procs == 4096: proc_grid = [ 16, 16, 16 ]
  elif n_procs == 8192: proc_grid = [ 32, 16, 16 ]
  elif n_procs == 16384: proc_grid = [ 32, 32, 16 ]
  else: 
    f'Invalid n_procs {n_procs}'
    exit(-1)
    

  write_parameter_file( file_name, proc_grid, tile_size, tile_length, dir_ics, dir_snap, outputs_file, uvb_file )
