import os, sys
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from uvb_functions import convert_grackle_file, Reaplace_Gamma_Parttial, Load_Grackle_File, Modify_UVB_Rates, Extend_Rates_Redshift, Copy_Grakle_UVB_Rates, Modify_UVB_Rates, Write_Rates_Grackle_File, Modify_Rates_From_Grackle_File
from plot_uvb_rates import Plot_UVB_Rates

base_dir = data_dir + 'cosmo_sims/wdm_sims/compare_alpha/'

alpha_vals = [ 1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.4 ]

rates_data_all = {}
for sim_id, alpha_val in enumerate(alpha_vals):
  
  output_dir = base_dir + f'sim_{sim_id}/'
  create_directory( output_dir ) 

  # Load the Original Rates
  grackle_file_name = 'data/UVB_rates_V22.h5'
  grackle_data = Load_Grackle_File( grackle_file_name )
  max_delta_z = 0.1
  rates_data = Extend_Rates_Redshift( max_delta_z, grackle_data )
  input_rates = Copy_Grakle_UVB_Rates( rates_data )

  parameter_values = { 'scale_H_heat':alpha_val }

  info = 'Rates for V22 Modified:'                     
  for p_name in parameter_values.keys():
    p_val = parameter_values[p_name]
    info += f' {p_name}:{p_val}' 
    

  modified_rates = Modify_Rates_From_Grackle_File(  parameter_values, max_delta_z = 0.1, rates_data=input_rates, extrapolate='constant', extend_rates_z=False, print_out=True )
  rates_data_all[sim_id] = modified_rates

  # grackle_file_name = output_dir + f'UVB_rates_V22_alpha_{alpha_val}.h5'
  grackle_file_name = output_dir + f'UVB_rates.h5'
  Write_Rates_Grackle_File( grackle_file_name, modified_rates )
  
  # out_file_name = output_dir + f'UVB_rates_V22_alpha_{alpha_val}.txt'
  
  out_file_name = output_dir + f'UVB_rates.txt'
  convert_grackle_file( grackle_file_name, out_file_name )
  

Plot_UVB_Rates( output_dir, rates_data=rates_data_all, figure_name='UVB_rates_all.png' )

  
