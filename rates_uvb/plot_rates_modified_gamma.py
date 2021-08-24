import os, sys
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from plot_uvb_rates import Plot_UVB_Rates
from uvb_functions import Load_Grackle_File


input_dir = data_dir + 'cosmo_sims/rescaled_P19/modified_gamma/'
output_dir = data_dir + 'cosmo_sims/rescaled_P19/modified_gamma/'
create_directory( output_dir )


rates_data = {}
for sim_id in range(1,7):
  file_name = f'{input_dir}/UVB_rates_{sim_id}.h5'
  rates = Load_Grackle_File( file_name )
  rates_data[sim_id] = rates


Plot_UVB_Rates( output_dir, rates_data=rates_data, figure_name='UVB_rates_modified_gamma.png' )


