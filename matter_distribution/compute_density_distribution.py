import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *


output_dir = data_dir + 'cosmo_sims/rescaled_P19/wdm/figures/'
create_directory( output_dir )

simulation_dir = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_cdm/'
input_dir = simulation_dir + 'snapshot_files/'
