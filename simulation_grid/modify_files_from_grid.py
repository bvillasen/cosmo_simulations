import sys, os, time
import numpy
from filecmp import dircmp
from shutil import copyfile, copytree, move, rmtree
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from transfer_grid_functions import *

grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_nsim900/'
dirs_in_grid = [ d for d in os.listdir(grid_dir) if os.path.isdir(grid_dir+d) ]


