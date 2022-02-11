import os, sys
import numpy as np
import pickle
import pymc
import matplotlib.pyplot as plt
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *

grid_dir = data_dir + 'cosmo_sims/sim_grid/grid_thermal/1024_P19m_np4_nsim400/'
sim_dirs = [ dir for dir in os.listdir(grid_dir) if os.path.isdir(grid_dir+dir) and dir[0]=='S' ]
sim_dirs.sort()

file_indx = 56
sim_dir = sim_dirs[0]
print(f'Dir: {sim_dir}')
file_name = grid_dir + sim_dir + f'analysis_files/{file_indx}_analysis.h5'
file = h5.File( file_name, 'r' )
