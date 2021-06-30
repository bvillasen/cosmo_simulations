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
from plot_UVB_Rates import Plot_Grid_UVB_Rates


SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
SG.Create_Grid_Directory_Structure()
SG.Create_All_Parameter_Files( ics_type='wdm' )
SG.Create_UVB_Rates_Files( )

figures_dir = root_dir + 'figures/'
create_directory( figures_dir ) 

# Plot the generated UVB Rates
SG.Load_Grid_UVB_Rates()
Plot_Grid_UVB_Rates( SG, figures_dir )
