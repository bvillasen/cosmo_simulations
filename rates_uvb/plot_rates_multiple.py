import os, sys
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from uvb_functions import Load_Grackle_File, Modify_Rates_From_Grackle_File, Extend_Rates_Redshift, Copy_Grakle_UVB_Rates
from plot_uvb_rates import Plot_UVB_Rates


base_dir   = data_dir + 'cosmo_sims/sim_grid/1024_np2_nsim16/simulation_files/'
output_dir = data_dir + 'cosmo_sims/sim_grid/1024_np2_nsim16/figures/' 

# Load the Original Rates
grackle_file_name = 'CloudyData_UVB_Puchwein2019_cloudy.h5'
grackle_data = Load_Grackle_File( grackle_file_name )
max_delta_z = 0.1
rates_P19 = Extend_Rates_Redshift( max_delta_z, grackle_data )
input_rates = Copy_Grakle_UVB_Rates( rates_P19 )

parameter_values = { 'scale_He': 0.44, 'scale_H': 0.78, 'deltaZ_He': 0.27, 'deltaZ_H':  0.05 }
rates_P19m = Modify_Rates_From_Grackle_File( parameter_values, rates_data=input_rates )

rates_data = {} 
# rates_data[0] = rates_P19
rates_data[1] = rates_P19m

sim_dirs = [ file for file in os.listdir(base_dir) if file[0]=='S' ]
sim_dirs.sort()

for sim_id, sim_dir in enumerate( sim_dirs ):
  input_dir = base_dir + sim_dir 
  file_name = f'{input_dir}/UVB_rates.h5'
  rates = Load_Grackle_File( file_name )
  rates_data[sim_id+2] = rates
  

Plot_UVB_Rates( output_dir, rates_data=rates_data, figure_name='UVB_rates_all_original.png' )


