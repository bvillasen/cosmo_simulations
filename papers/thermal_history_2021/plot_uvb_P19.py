import os, sys
import numpy as np
root_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from generate_grackle_uvb_file import Reaplace_Gamma_Parttial, Load_Grackle_File, Modify_UVB_Rates, Extend_Rates_Redshift, Copy_Grakle_UVB_Rates, Modify_UVB_Rates, Write_Rates_Grackle_File
from plot_uvb_rates import Plot_UVB_Rates


# output_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_modified_gamma/'
# output_dir = data_dir + 'thermal/'
output_dir = data_dir + 'cosmo_sims/figures/nature/'
create_directory( output_dir ) 


# Load the Original Rates
grackle_file_name = root_dir + 'rates_uvb/data/CloudyData_UVB_Puchwein2019_cloudy.h5'
rates_P19 = Load_Grackle_File( grackle_file_name )

rates_data = { 0: rates_P19  }


Plot_UVB_Rates( output_dir, rates_data=rates_data, figure_name='uvb_rates_P19.png')