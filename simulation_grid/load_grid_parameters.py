import sys, os
sys.path.append('parameter_files')
from simulation_parameters import grid_name


# Select UVB parameters from file
if grid_name == '1024_np5_nsim16':  from parameters_np5_nsim16 import param_wdm_UVB_Rates as Grid_Parameters



\