import os, sys
import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
import pylab
import matplotlib
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from uvb_functions import Modify_UVB_Rates, Reaplace_Gamma_Parttial, Load_Grackle_File, Copy_Grakle_UVB_Rates, Modify_UVB_Rates_sigmoid, Extend_Rates_Redshift, Modify_Rates_From_Grackle_File, Write_Rates_Grackle_File
from figure_functions import *
from plot_uvb_rates import Plot_UVB_Rates

  
proj_dir = data_dir + 'projects/thermal_history/'
output_dir = proj_dir + 'data/modified_gamma_sigmoid/'
create_directory( output_dir )

file_name = 'data/UVB_rates_V22.h5'
rates_V22 = Load_Grackle_File( file_name )
z_uvb_V22 = rates_V22['UVBRates']['z']
gamma_V22 = rates_V22['UVBRates']['Chemistry']['k24']


grackle_file_name = 'CloudyData_UVB_Puchwein2019_cloudy.h5'
grackle_data = Load_Grackle_File( grackle_file_name )
max_delta_z = 0.1
rates_P19 = Extend_Rates_Redshift( max_delta_z, grackle_data, log=True )
z_uvb_P19 = rates_P19['UVBRates']['z']
gamma_P19 = rates_P19['UVBRates']['Chemistry']['k24']

# file_name = sim_dir + 'rescale_tau_to_Bosman_2018.txt'
# rescale_data = np.loadtxt( file_name ).T
# z_vals, alpha_vals = rescale_data
# 
# gamma = gamma_V22
# z_uvb = z_uvb_V22
# gamma_mod_vals, z_mod_vals = [], []
# for z,alpha in zip(z_vals,alpha_vals):
#   z_diff = np.abs( z - z_uvb )
#   z_id = np.where( z_diff == z_diff.min() )[0][0]
#   z_mod_vals.append( z_uvb[z_id] )
#   gamma_mod_vals.append( gamma[z_id]/alpha )

rates_data_all =  { 0:rates_V22 }
alpha_vals = [ 2.0, 2.5, 3.0, 3.5, 4.0, 4.5 ]
for sim_id, alpha in enumerate(alpha_vals): 
  params_HL = { 'scale_He':0.45, 'scale_H':0.77, 'deltaZ_He':0.31, 'deltaZ_H':0.1 }
  rates_data = Copy_Grakle_UVB_Rates( rates_P19 )
  rates_HL = Modify_Rates_From_Grackle_File( params_HL,  rates_data=rates_data, extrapolate='spline' )
  x0 = 0
  z_range = ( 4.8, 6.1 )
  input_rates = Copy_Grakle_UVB_Rates( rates_HL )
  rates_sigmoid = Modify_UVB_Rates_sigmoid( input_rates, z_range, alpha, x0 )
  z_uvb_s = rates_sigmoid['UVBRates']['z']
  gamma_s = rates_sigmoid['UVBRates']['Chemistry']['k24']
  gamma_s_He = rates_sigmoid['UVBRates']['Chemistry']['k26']

  # # Villasenor et al. 2022 (revised
  z = z_uvb_V22
  z_l, z_r = 4.7, 6.1
  indices = ( z >= z_l ) * ( z <= z_r )
  indx = 76
  rates_mod = Copy_Grakle_UVB_Rates(rates_V22)
  for key in [ 'k24', 'k26' ]:
    indx = np.where(indices==True)[0][0]
    factor = rates_mod['UVBRates']['Chemistry'][key][indx] / rates_sigmoid['UVBRates']['Chemistry'][key][indx]
    rates_mod['UVBRates']['Chemistry'][key][indices] = rates_sigmoid['UVBRates']['Chemistry'][key][indices] * factor  
    rate = rates_mod['UVBRates']['Chemistry'][key] 
    rate[indx] = 10**( 0.5 * (np.log10(rate[indx-1]) + np.log10(rate[indx+1]) ))
    
  for key in [ 'piHI', 'piHeI' ]:
    indx = np.where(indices==True)[0][0]
    factor = rates_mod['UVBRates']['Photoheating'][key][indx] / rates_sigmoid['UVBRates']['Photoheating'][key][indx]
    rates_mod['UVBRates']['Photoheating'][key][indices] = rates_sigmoid['UVBRates']['Photoheating'][key][indices] * factor  
    rate = rates_mod['UVBRates']['Photoheating'][key]
    rate[indx] = 10**( 0.5 * (np.log10(rate[indx-1]) + np.log10(rate[indx+1]) ))

  rates_mod['UVBRates']['info'] = f'Modified V22 '
  out_file_name = output_dir + f'UVB_rates_V22_modified_sigmoid_{sim_id}.h5'
  Write_Rates_Grackle_File( out_file_name, rates_mod )
  
  rates_data_all[sim_id+1] = rates_mod

# rates_data =  {0:rates_P19, 1:rates_V22, 2:rates_new}
Plot_UVB_Rates( output_dir, rates_data=rates_data_all, figure_name='UVB_rates_all_sigmoid.png' )
# 
# font_size = 16
# 
# ncols, nrows = 1, 1
# fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))
# 
# ax.plot(z_uvb_V22, gamma_V22)
# ax.plot(z_uvb_P19, gamma_P19)
# # ax.plot(z_uvb_s, gamma_s )
# ax.plot(z_uvb_V22, gamma_new, ls='--'  )
# 
# 
# 
# ax.set_yscale('log')
# # ax.set_xlim(4, 7)
# # ax.set_ylim(1e-16, 1e-12)
# 
# file_name = output_dir + 'Gamma_HI_modified.png'
# fig.savefig( file_name,  pad_inches=0.1, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor())
# print('Saved Image: ', file_name)
# 
