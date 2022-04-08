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

proj_dir = data_dir + 'projects/thermal_history/'
output_dir = proj_dir + 'data/modified_gamma_sigmoid/'
create_directory( output_dir ) 

# Load the Original Rates
grackle_file_name = 'CloudyData_UVB_Puchwein2019_cloudy.h5'
grackle_data = Load_Grackle_File( grackle_file_name )
max_delta_z = 0.1
P19_rates = Extend_Rates_Redshift( max_delta_z, grackle_data, log=True )
input_rates = Copy_Grakle_UVB_Rates( P19_rates )


rates_data = {}
# rates_data[0] = P19_rates


parameter_values = { 'scale_He':  0.44,
                     'scale_H':   0.78,
                     'deltaZ_He': 0.27,
                     'deltaZ_H':  0.05 }
                     
                  

input_rates = Copy_Grakle_UVB_Rates( P19_rates )
modP19_rates = Modify_Rates_From_Grackle_File( parameter_values, rates_data=input_rates )
modP19_rates['UVBRates']['info'] = f'Modified P19 '
rates_data[1] = modP19_rates

id = 0
out_file_name = output_dir + f'UVB_rates_{id}.h5'
Write_Rates_Grackle_File( out_file_name, modP19_rates )


alpha_vals = [ 2, 2.5, 3, 3.5, 4, 4.5  ]
x0 = 0
z_range = ( 4.8, 6.0 )

for id, alpha in enumerate(alpha_vals):
  input_rates = Copy_Grakle_UVB_Rates( P19_rates )
  rates_sigmoid = Modify_UVB_Rates_sigmoid( input_rates, z_range, alpha, x0 )
  rates_modified = Modify_Rates_From_Grackle_File( parameter_values, rates_data=rates_sigmoid )
  rates_modified['UVBRates']['info'] = f'Modified P19 modified Gamma sigmoid alpha={alpha:.1f}'
  rates_data[id+2] = rates_modified
  out_file_name = output_dir + f'UVB_rates_{id+1}.h5'
  Write_Rates_Grackle_File( out_file_name, rates_modified )



Plot_UVB_Rates( output_dir, rates_data=rates_data, figure_name='rates_modified_sigmoid.png' )
