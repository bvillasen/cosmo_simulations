import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 



base_dir = data_dir + 'rescaled_P19/wdm/'

sim_name = '1024_50Mpc_cdm'

input_dir = base_dir + f'{sim_name}/analysis_files/'


