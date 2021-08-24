import os, sys
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from uvb_functions import Reaplace_Gamma_Parttial, Load_Grackle_File, Modify_UVB_Rates, Extend_Rates_Redshift, Copy_Grakle_UVB_Rates, Modify_UVB_Rates, Write_Rates_Grackle_File
from plot_uvb_rates import Plot_UVB_Rates


# output_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_modified_gamma/'
# output_dir = data_dir + 'thermal/'
output_dir = 'data/'
# create_directory( output_dir ) 


# Load the Original Rates
grackle_file_name = 'CloudyData_UVB_Puchwein2019_cloudy.h5'
grackle_data = Load_Grackle_File( grackle_file_name )
max_delta_z = 0.1
rates_data = Extend_Rates_Redshift( max_delta_z, grackle_data )
input_rates = Copy_Grakle_UVB_Rates( rates_data )

parameter_values = { 'scale_He':  0.44,
                     'scale_H':   0.78,
                     'deltaZ_He': 0.27,
                     'deltaZ_H':  0.05 }

# parameter_values = { 'scale_He':  1.0,
#                      'scale_H':   1.0,
#                      'deltaZ_He': 0.0,
#                      'deltaZ_H':  0.0 }

info = 'Rates for:'                     
for p_name in parameter_values.keys():
  p_val = parameter_values[p_name]
  info += f' {p_name}:{p_val}' 
                    
rates_modified = Modify_UVB_Rates( parameter_values, input_rates )
z = rates_modified['z']
gamma = rates_modified['photoionization_HI']

# # Modigy Gamma_HI to match observed HI Optical Depth
# data = np.loadtxt( data_dir + 'rescale_gamma/solution_rescaled_P19/rescaled_gamma_rescaled_HI.txt' )
# z_rescaled, gamma_rescaled = data.T 
# gamma_new = Reaplace_Gamma_Parttial( z, gamma, z_rescaled, gamma_rescaled )
# rates_modified['photoionization_HI'] = gamma_new
# info += ' Modified Gamma HI'

output_rates = {
  'UVBRates':{ 'z':rates_modified['z'], 
               'Photoheating':{ 'piHI':rates_modified['photoheating_HI'], 'piHeI':rates_modified['photoheating_HeI'], 'piHeII':rates_modified['photoheating_HeII'] }, 
               'Chemistry':{ 'k24':rates_modified['photoionization_HI'],  'k26':rates_modified['photoionization_HeI'],  'k25':rates_modified['photoionization_HeII'] },
               'info':info } }
                
out_file_name = output_dir + 'UVB_rates_P19modified.h5'
Write_Rates_Grackle_File( out_file_name, output_rates )

# Plot_UVB_Rates( output_dir, rates=output_rates['UVBRates'] )
