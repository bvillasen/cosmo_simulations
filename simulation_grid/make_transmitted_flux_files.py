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

file_indx = 55
sim_dir = sim_dirs[0]
print(f'Dir: {sim_dir}')
file_name = grid_dir + sim_dir + f'/analysis_files/{file_indx}_analysis.h5'
file = h5.File( file_name, 'r' )
current_z = file.attrs['current_z'][0]
F_mean = file['lya_statistics'].attrs['Flux_mean_HI'][0]
vel_Hubble = None
axis = 'x'
key = f'skewers_{axis}'
skewers_data = file['lya_statistics'][key]
vel_Hubble_axis = skewers_data['vel_Hubble'][...]
los_flux_axis = skewers_data['los_transmitted_flux_HI'][...]


file_name = '/data/groups/comp-astro/bruno/cosmo_sims/sim_grid/1024_wdmgrid_nsim600/transmitted_flux/S000_A0_B0_C0_D0/lya_flux_033.h5'
file_0 = h5.File( file_name, 'r' )