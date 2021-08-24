import os, sys
import numpy as np
import matplotlib.pylab as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from uvb_functions import *
from plot_uvb_rates import Plot_UVB_Rates
from figure_functions import *


output_dir = data_dir + 'cosmo_sims/rescaled_P19/modified_gamma/'
create_directory( output_dir ) 

# Load the Original Rates
grackle_file_name = 'CloudyData_UVB_Puchwein2019_cloudy.h5'
grackle_data = Load_Grackle_File( grackle_file_name )
max_delta_z = 0.1
P19_rates = Extend_Rates_Redshift( max_delta_z, grackle_data )
input_rates = Copy_Grakle_UVB_Rates( P19_rates )

