import sys, os, time
import numpy
from filecmp import dircmp
from shutil import copyfile, copytree, move, rmtree
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from transfer_grid_functions import *

grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_extended_beta/'
dirs_in_grid = [ d for d in os.listdir(grid_dir) if os.path.isdir(grid_dir+d) ]

base_dir = grid_dir + 'simulation_files/'
sim_dirs = [ d for d in os.listdir(base_dir) if os.path.isdir(base_dir+d) ]

files_to_delete = []
for sim_dir in sim_dirs:
  src_dir = base_dir + f'{sim_dir}/'
  files = [ f for f in os.listdir(src_dir) if os.path.isfile(src_dir+f) and f.find('core')==0 ]
  if len(files) > 0:
    for file in files:
      file_name = src_dir + file
      files_to_delete.append(file_name)
      
print(f'Files to delete: {files_to_delete}' )
print( f'N to delete: {len(files_to_delete)}' )      
for file_name in files_to_delete:
  os.remove(file_name)
