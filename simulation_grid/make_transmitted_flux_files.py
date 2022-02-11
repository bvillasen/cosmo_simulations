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
sim_dirs = [ dir for dir is os.listdir(grid_dir) if os.path.isdir(dir) and dir[0]=='S' ]