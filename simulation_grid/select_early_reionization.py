import os, sys
import numpy as np
import pickle
import pymc
import matplotlib.pyplot as plt
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_grid_parameters import Grid_Parameters
from simulation_grid import Simulation_Grid
from simulation_parameters import *


SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
SG.Load_Grid_Analysis_Data(  load_pd_fit=True, mcmc_fit_dir='fit_mcmc_delta_0_1.0', load_thermal=True )
sim_ids = SG.sim_ids

data_reion = {}
for sim_id in sim_ids:
  data_sim = SG.Grid[sim_id]['analysis']
  z_reion = data_sim['global_properties']['z_ion_H'] 
  data_reion[sim_id] = z_reion
  
output_dir = root_dir + 'global_properties/'
create_directory( output_dir )

file_name = output_dir + 'grid_z_reionization.pkl'
Write_Pickle_Directory( data_reion, file_name )