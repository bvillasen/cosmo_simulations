import sys, os
from shutil import copyfile, copytree
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *


root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
sim_dirs = [ dir for dir in os.listdir(root_dir+'simulation_files') if dir[0]=='S' ]
sim_dirs.sort()

out_base_dir = root_dir + 'analysis_files/'
create_directory( out_base_dir )

for sim_dir in sim_dirs:
  output_dir = out_base_dir + sim_dir +'/'
  create_directory( output_dir )

  input_dir = root_dir + f'simulation_files/{sim_dir}/analysis_files/'
  files_to_move = [ f for f in os.listdir(input_dir) if os.path.isfile(input_dir+f)  ]
  dirs_to_move  = [ d for d in os.listdir(input_dir) if os.path.isdir(input_dir+d)  ]
  files_to_move.sort()
  dirs_to_move.sort()

  print( f'Moving {input_dir} -> {output_dir}' )

  dir_name = 'fit_mcmc_delta_0_1.0'
  src = input_dir + dir_name
  dst = output_dir + dir_name
  copytree(src, dst)


  for file_name in files_to_move:
    src = input_dir + file_name
    dst = output_dir + file_name
    copyfile(src, dst)















