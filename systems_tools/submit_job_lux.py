import os, sys
from pathlib import Path
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools' )
from tools import *


job_name  = 'thermal_cdm' 
n_mpi_tasks = 320
n_nodes = 8
n_tasks_per_node = 40
time = '24:00:00'
command = 'python'

job_dir = home_dir + 'thermal_IGM/'
command_params = 'run_termal_wdm_chain.py'

# job_dir = home_dir + 'cosmo_simulations/lya_statistics/'
# command_params = f'compute_transmitted_flux_mpi_grid.py {data_dir}cosmo_sims/sim_grid/1024_wdmgrid_nsim200_deltaZ_n0p5'

# partition = 'comp-astro'
partition = 'gpuq'
work_directory = '/home/brvillas/jobs/'
output = work_directory + 'run_output'
create_directory( work_directory )

submit_str = f"""#!/bin/bash          
#SBATCH --job-name={job_name}    
#SBATCH --partition={partition}       
#SBATCH --ntasks={n_mpi_tasks}             
#SBATCH --nodes={n_nodes}               
#SBATCH --ntasks-per-node={n_tasks_per_node}     
#SBATCH --time={time}          
#SBATCH --output={output}.log   

module load hdf5/1.10.6
module load cuda10.2/10.2

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/brvillas/code/grackle/lib
cd {job_dir}

set OMP_NUM_THREADS=10
mpirun -N {n_mpi_tasks} --map-by ppr:{n_tasks_per_node}:node {command} {command_params} 
"""

print(submit_str)

if work_directory[-1] != '/': work_directory += '/'
file_name = 'submit_job_lux'
file_name = work_directory + file_name
file = open( file_name, 'w' )
file.write( submit_str )
file.close()
print(f'Saved File: {file_name}')

print(f'Changing dir: {work_directory}' )
os.chdir( job_dir )
if partition == 'comp-astro': partition_key = 'comp'
if partition == 'gpuq':       partition_key = 'gpu'
exclude_nodes = []
exclude_comand = '' 
for node in exclude_nodes:
  exclude_comand += node + ','
if exclude_comand != '': exclude_comand = exclude_comand[:-1]
command = f'submit_script {partition_key} {file_name} {exclude_comand}'
print( f' Submitting: {command}' )
os.system( command )

