import os, sys
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools')
from tools import *
#Append analysis directories to path
extend_path()
from load_grid_parameters import Grid_Parameters
from simulation_grid import Simulation_Grid
from simulation_parameters import *
from plot_uvb_rates import Plot_Grid_UVB_Rates

check_queue = True
if system == 'Shamrock': check_queue = False

SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
SG.Get_Grid_Status( check_queue=check_queue )

