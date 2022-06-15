
def create_job_script_crusher( job_params, file_name='submit_job_crusher', save_file=True,  ):
  
  project = job_params['project']
  job_name = job_params['name']
  n_nodes = job_params['n_nodes']
  time = job_params['time']
  dir_work = job_params['dir_work']
  dir_bin = job_params['dir_bin']
  bin_name = job_params['bin_name']
  partition = job_params['partition']

  submit_str = f"""#!/bin/bash          
#SBATCH -A {project}
#SBATCH -J {job_name}
#SBATCH -o run_output.out
#SBATCH -e run_error.out
#SBATCH -t {time}
#SBATCH -p {partition}
#SBATCH -N {n_nodes}

module load rocm
module load craype-accel-amd-gfx90a
module load cray-hdf5 cray-fftw

export MPICH_GPU_SUPPORT_ENABLED=1
export LD_LIBRARY_PATH="$CRAY_LD_LIBRARY_PATH:$LD_LIBRARY_PATH"

export CHOLLA_HOME={dir_bin}
export WORK_DIR={dir_work}
cd $WORK_DIR

date
export OMP_NUM_THREADS=8
"""

  n_mpi_list = job_params['n_mpi_list']
  for n_mpi in n_mpi_list:
    param_file = f'param_files/param_{n_mpi}.txt' 
    sim_file   = f'sim_files/sim_output_{n_mpi}.log'
    # exec_line  = f'jsrun --smpiargs="-gpu" -n{n_mpi} -a1 -c7 -g1 --bind packed:7 $CHOLLA_HOME/{bin_name} $WORK_DIR/{param_file} > $WORK_DIR/{sim_file} |sort'
    exec_line    = f'srun -n {n_mpi} --ntasks-per-node=8 -c 8 --gpu-bind=closest --gpus-per-node=8 $CHOLLA_HOME/{bin_name} $WORK_DIR/{param_file} > $WORK_DIR/{sim_file} |sort'
    submit_str += exec_line + '\n\n'
    
  if save_file:  
    file = open( file_name, 'w' )
    file.write( submit_str )
    file.close()
    print(f' Saved File: {file_name}')

  return submit_str



def create_job_script_summit( job_params, file_name='submit_job_summit.lsf', save_file=True,  ):
  
  project = job_params['project']
  job_name = job_params['name']
  n_nodes = job_params['n_nodes']
  time = job_params['time']
  dir_work = job_params['dir_work']
  dir_bin = job_params['dir_bin']
  bin_name = job_params['bin_name']
  partition = job_params['partition']
  
  submit_str = f"""#!/bin/bash          
#BSUB -P {project}       
#BSUB -W {time}          
#BSUB -nnodes {n_nodes}               
#BSUB -J {job_name}    
#BSUB -o log_output.txt
#BSUB -e log_error.txt
#BSUB -alloc_flags "smt4"
#BSUB -q {partition}

module load gcc cuda fftw hdf5

export CHOLLA_HOME={dir_bin}
export WORK_DIR={dir_work}
cd $WORK_DIR

date
export OMP_NUM_THREADS=7
"""
  
  n_mpi_list = job_params['n_mpi_list']
  for n_mpi in n_mpi_list:
    param_file = f'param_files/param_{n_mpi}.txt' 
    sim_file   = f'sim_files/sim_output_{n_mpi}.log'
    exec_line  = f'jsrun --smpiargs="-gpu" -n{n_mpi} -a1 -c7 -g1 --bind packed:7 $CHOLLA_HOME/{bin_name} $WORK_DIR/{param_file} > $WORK_DIR/{sim_file} |sort'
    submit_str += exec_line + '\n\n'
    
  if save_file:  
    file = open( file_name, 'w' )
    file.write( submit_str )
    file.close()
    print(f' Saved File: {file_name}')

  return submit_str
