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


output_dir = data_dir + 'modified_uvb_rates/zero_heat_ion/uvb_models/'
create_directory( output_dir ) 

# Load Modified P19 Rates
grackle_file_name = 'data/UVB_rates_P19m.h5'
input_rates = Load_Grackle_File( grackle_file_name )

input_rates['UVBRates']['info'] = f'Modified P19'
out_file_name = output_dir + f'UVB_rates_0.h5'
Write_Rates_Grackle_File( out_file_name, input_rates )

z = input_rates['UVBRates']['z']

z_lim = 6.1
indices = z <= z_lim
 
min_val = 0
zero_ion = True

for model_id in [1,2, 3]:
  

  if model_id in [1]: delta_z = 0
  if model_id in [2]: delta_z = 0.95
  if model_id in [3]: delta_z = 1.9

  rates = Copy_Grakle_UVB_Rates( input_rates )
  
  
  root_key = 'Chemistry'
  keys = [ 'k24',  'k25',  'k26' ]
  for key in keys:
    if zero_ion: rates['UVBRates'][root_key][key][indices] = min_val

  root_key = 'Photoheating'
  keys = [ 'piHI',  'piHeI',  'piHeII' ]
  for key in keys:
    rates['UVBRates'][root_key][key][indices] = min_val

  rates['UVBRates']['z'] = z + delta_z
  rates['UVBRates']['info'] = f'Modified P19: Z_lim:{z_lim}  Zero Photoheating ' + 'Zero Photoionization '* zero_ion + f'Delta_z:{delta_z}'

  out_file_name = output_dir + f'UVB_rates_{model_id}.h5'
  Write_Rates_Grackle_File( out_file_name, rates )


input_dir = output_dir 
rates_data = {}
for sim_id in range(4):
  file_name = f'{input_dir}/UVB_rates_{sim_id}.h5'
  rates = Load_Grackle_File( file_name )
  rates_data[sim_id] = rates

Plot_UVB_Rates( output_dir, rates_data=rates_data, figure_name='UVB_rates_all.png' )





