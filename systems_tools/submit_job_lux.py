import os, sys
from pathlib import Path
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools' )
from tools import *


job_name  = 'python' 
n_mpi_tasks = 320
n_nodes = 8
n_tasks_per_node = 40
time = '24:00:00'
command = 'python'
command_params = '1024_wdmgrid_nsim200_deltaZ_0p0'


partition = 'comp-astro'
output = 'run_output.log'
work_directory = '/home/brvillas/jobs'
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
cd {work_directory}

set OMP_NUM_THREADS=10
mpirun -N {n_mpi_tasks} --map-by ppr:{n_tasks_per_node}:node {command} {command_params} 
"""

if work_directory[-1] != '/': work_directory += '/'
file_name = 'submit_job_lux'
file_name = work_directory + file_name
file = open( file_name, 'w' )
file.write( submit_str )
file.close()
print(f' Saved File: {file_name}')