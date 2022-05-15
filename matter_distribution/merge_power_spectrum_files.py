import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *



type = 'hydro'

sim_name = '2048_25Mpc_cdm'
# sim_name = '2048_25Mpc_m3.0kev'
base_dir = data_dir + 'cosmo_sims/wdm_sims/'
sim_dir  = base_dir + f'{sim_name}/'
input_dir = sim_dir + 'power_spectrum_files/split/'
output_dir = sim_dir + 'power_spectrum_files/'

data_all = {}
for indx in range(6):
  file_name = input_dir + f'power_spectrum_{type}_{indx}.pkl'
  data = Load_Pickle_Directory( file_name )
  data_all[indx] = data


file_name = file_name = output_dir + f'power_spectrum_{type}.pkl'
Write_Pickle_Directory( data_all, file_name )