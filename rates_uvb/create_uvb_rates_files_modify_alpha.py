import os, sys
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from uvb_functions import Reaplace_Gamma_Parttial, Load_Grackle_File, Modify_UVB_Rates, Extend_Rates_Redshift, Copy_Grakle_UVB_Rates, Modify_UVB_Rates, Write_Rates_Grackle_File, Write_Cholla_UVB_file_from_Grackle
from plot_uvb_rates import Plot_UVB_Rates

proj_dir = data_dir + 'projects/wdm/data/'
output_dir  = proj_dir + 'modified_alpha/'
figures_dir = proj_dir + 'modified_alpha/figures/' 
create_directory( output_dir ) 
create_directory( figures_dir )

alpha_vals = [ 0.6, 0.8, 1.0, 1.2, 1.4 ]
n_models = len( alpha_vals )

for model_id,alpha in enumerate(alpha_vals):

  # Load the Original Rates
  grackle_file_name =  root_dir + 'rates_uvb/data/UVB_rates_P19m.h5' 
  grackle_data = Load_Grackle_File( grackle_file_name )
  input_rates = Copy_Grakle_UVB_Rates( grackle_data )

  parameter_values = { 'scale_H_ion':  1.0,
                       'scale_H_Eheat':  alpha,
                       'deltaZ_H': 0 }

  info = 'Rates for V21 and :'                     
  for p_name in parameter_values.keys():
    p_val = parameter_values[p_name]
    info += f' {p_name}:{p_val}' 

  rates_modified = Modify_UVB_Rates( parameter_values, input_rates )
  output_rates = { 'UVBRates':{ 'z':rates_modified['z'], 'info':info ,
                 'Photoheating':{ 'piHI':rates_modified['photoheating_HI'], 'piHeI':rates_modified['photoheating_HeI'], 'piHeII':rates_modified['photoheating_HeII'] }, 
                 'Chemistry':{ 'k24':rates_modified['photoionization_HI'],  'k26':rates_modified['photoionization_HeI'],  'k25':rates_modified['photoionization_HeII'] } } }

  grackle_file_name = output_dir + f'UVB_rates_{model_id}.h5'
  out_file_name     = output_dir + f'UVB_rates_{model_id}.txt'
  Write_Rates_Grackle_File( grackle_file_name, output_rates )
  Write_Cholla_UVB_file_from_Grackle( grackle_file_name, out_file_name )
  

grackle_UVB_file_name =  root_dir + 'rates_uvb/data/UVB_rates_P19m.h5' 
rates_P19m = Load_Grackle_File( grackle_UVB_file_name )

rates_all = {}
rates_all[0] = rates_P19m 
for model_id in range(n_models):
  file_name = output_dir + f'UVB_rates_{model_id}.h5'
  rates = Load_Grackle_File( file_name )
  rates_all[model_id+1] = rates
  rates_all[model_id+1]['line_style'] = '--'
Plot_UVB_Rates( figures_dir, rates_data=rates_all, figure_name='UVB_rates_all.png' )
