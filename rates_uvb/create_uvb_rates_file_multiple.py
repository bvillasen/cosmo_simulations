import os, sys
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from uvb_functions import Reaplace_Gamma_Parttial, Load_Grackle_File, Modify_UVB_Rates, Extend_Rates_Redshift, Copy_Grakle_UVB_Rates, Modify_UVB_Rates, Write_Rates_Grackle_File
from plot_uvb_rates import Plot_UVB_Rates


# output_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_modified_gamma/'
output_dir = data_dir + 'thermal/modified_P19/'
create_directory( output_dir ) 





def Combine_Values_Lists( param_vals ):
  n_param = len( param_vals)
  indices_list = []
  for i in range(n_param):
    param_id = n_param - 1 - i
    n_vals =  len(param_vals[param_id]) 
    indices_list.append( [ x for x in range(n_vals)] )    
  param_indx_grid = indices_list[0]
  for i in range( n_param-1 ):
    param_indx_grid = Combine_List_Pair( indices_list[i+1], param_indx_grid )
  param_grid = []
  for indices in param_indx_grid:
    p_vals = [ param_vals[i][indices[i]] for i in range(n_param) ]
    param_grid.append( p_vals )
  return param_grid
  
param_vals = {}
param_vals[0] = [ 0.37, 0.50 ]
param_vals[1] = [ 0.77, 0.79 ]
param_vals[2] = [ 0.22, 0.33 ]
param_vals[3] = [ 0.02, 0.08 ]  


param_grid = Combine_Values_Lists( param_vals )
n_models = len( param_grid )

for model_id in range(n_models):
  p_vals = param_grid[model_id]
  parameter_values = { 'scale_He':  p_vals[0],
                       'scale_H':   p_vals[1],
                       'deltaZ_He': p_vals[2],
                       'deltaZ_H':  p_vals[3] }

  info = 'Rates for:'                     
  for p_name in parameter_values.keys():
    p_val = parameter_values[p_name]
    info += f' {p_name}:{p_val}' 

  # Load the Original Rates
  grackle_file_name = 'CloudyData_UVB_Puchwein2019_cloudy.h5'
  grackle_data = Load_Grackle_File( grackle_file_name )
  max_delta_z = 0.1
  rates_data = Extend_Rates_Redshift( max_delta_z, grackle_data )
  input_rates = Copy_Grakle_UVB_Rates( rates_data )
  rates_modified = Modify_UVB_Rates( parameter_values, input_rates )

  output_rates = {
    'UVBRates':{ 'z':rates_modified['z'], 
                 'Photoheating':{ 'piHI':rates_modified['photoheating_HI'], 'piHeI':rates_modified['photoheating_HeI'], 'piHeII':rates_modified['photoheating_HeII'] }, 
                 'Chemistry':{ 'k24':rates_modified['photoionization_HI'],  'k26':rates_modified['photoionization_HeI'],  'k25':rates_modified['photoionization_HeII'] },
                 'info':info } }

  out_file_name = output_dir + f'UVB_rates_{model_id}.h5'
  Write_Rates_Grackle_File( out_file_name, output_rates )
  # Plot_UVB_Rates( output_dir, rates=output_rates['UVBRates'] )
