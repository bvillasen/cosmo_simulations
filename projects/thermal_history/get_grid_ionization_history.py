import os, sys
import numpy as np
import h5py as h5
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *


grid_name = '1024_P19m_np4_nsim400'
grid_dir = data_dir + f'cosmo_sims/sim_grid/{grid_name}/' 
thermal_dir = grid_dir + 'thermal/'
output_dir = grid_dir + 'properties/'
create_directory( output_dir )

sim_dirs = [ dir for dir in os.listdir(thermal_dir) if dir[0]=='S' ]
sim_dirs.sort()

data_all = {}
for sim_id, sim_dir in enumerate( sim_dirs ):
  input_dir = thermal_dir + f'{sim_dir}/'
  file_name = input_dir + 'solution.h5'
  print(f'Loading File: {file_name}' )
  file = h5.File( file_name, 'r')
  z = file['z'][...]
  n_H = file['n_H'][...]
  n_HI = file['n_HI'][...]
  n_He = file['n_He'][...]
  n_HeII = file['n_HeII'][...]
  x_HI = n_HI / n_H
  x_HeII = n_HeII / n_He
  data_sim = {'z':z, 'x_HI':x_HI, 'x_HeII':x_HeII }
  data_all[sim_id] = data_sim
  
file_name = output_dir + 'grid_ionization_fraction.pkl'
Write_Pickle_Directory( data_all, file_name )