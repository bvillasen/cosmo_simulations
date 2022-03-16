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


output_dir = data_dir + 'modified_uvb_rates/reduced_heating/uvb_models/'
create_directory( output_dir ) 

# Load Modified P19 Rates
# grackle_file_name = 'data/UVB_rates_P19m.h5'
# grackle_file_name = 'data/UVB_rates_P19modified.h5'
grackle_file_name = 'data/UVB_rates_V22.h5'
input_rates = Load_Grackle_File( grackle_file_name )
max_delta_z = 0.1
input_rates = Extend_Rates_Redshift( max_delta_z, input_rates, log=True )



z = input_rates['UVBRates']['z']

z_l, z_m, z_r = 4.2, 5.8, 6.6
indices_l = np.where( ( z >= z_l) * ( z <= z_m ) )[0] 
indices_r = np.where( ( z >= z_m) * ( z <= z_r ) )[0] 

n_l = len( indices_l ) 
n_r = len( indices_r ) 
factor_l = 1.0
factor_r = 1.0

factors_r = [ 1.0, 0.8, 0.6, 0.4, 0.2  ]
n_models = len( factors_r )

heating = []

for sim_id, factor_m in enumerate(factors_r): 
  rescale_vals_l = np.linspace( factor_l, factor_m, n_l )
  rescale_vals_r = np.linspace( factor_m, factor_r, n_r )

  rates = Copy_Grakle_UVB_Rates( input_rates )
  rates['UVBRates']['Photoheating']['piHI'][indices_l] *= rescale_vals_l
  rates['UVBRates']['Photoheating']['piHI'][indices_r] *= rescale_vals_r
  rates['UVBRates']['Photoheating']['piHeI'][indices_l] *= rescale_vals_l
  rates['UVBRates']['Photoheating']['piHeI'][indices_r] *= rescale_vals_r
  rates['UVBRates']['info'] = f'Modified  P19  z_rescaled:[ {z_l} - {z_r} ] rescale_vals: [ {factor_l} - {factor_r}]'
  z = rates['UVBRates']['z']
  heating.append( rates['UVBRates']['Photoheating']['piHI'] )
  
  out_file_name = output_dir + f'UVB_rates_{sim_id}.h5'
  Write_Rates_Grackle_File( out_file_name, rates )


z_val = 6.0
z_diff = np.abs( z - z_val )
indx = np.where( z_diff == z_diff.min() )[0][0]
heat_0 = heating[0][indx]
for sim_id, factor_r in enumerate(factors_r):
   print( f'Factor :{factor_r}  Heat Frac: {heating[sim_id][indx] / heat_0}' )

input_dir = output_dir 
rates_data = {}
for sim_id in range(n_models):
  file_name = f'{input_dir}/UVB_rates_{sim_id}.h5'
  rates = Load_Grackle_File( file_name )
  rates_data[sim_id] = rates

Plot_UVB_Rates( output_dir, rates_data=rates_data, figure_name='UVB_rates_all.png' )




