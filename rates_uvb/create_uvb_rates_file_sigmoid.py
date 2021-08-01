import os, sys
import numpy as np
import matplotlib.pylab as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from generate_grackle_uvb_file import *
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


rates_data = {}
rates_data[0] = P19_rates


parameter_values = { 'scale_He':  0.44,
                     'scale_H':   0.78,
                     'deltaZ_He': 0.27,
                     'deltaZ_H':  0.05 }

input_rates = Copy_Grakle_UVB_Rates( P19_rates )
modP19_rates = Modify_Rates_From_Grackle_File( None, parameter_values, rates_data=input_rates )
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
  rates_modified = Modify_Rates_From_Grackle_File( None, parameter_values, rates_data=rates_sigmoid )
  rates_modified['UVBRates']['info'] = f'Modified P19 modified Gamma sigmoid alpha={alpha:.1f}'
  rates_data[id+2] = rates_modified
  out_file_name = output_dir + f'UVB_rates_{id+1}.h5'
  Write_Rates_Grackle_File( out_file_name, rates_modified )



Plot_UVB_Rates( output_dir, rates_data=rates_data )



# gamma = rates_sigma['UVBRates']['Chemistry']['k24']
# z_mod = z[indices_mod[0]-1:indices_mod[-1]+2]
# if z.shape != gamma_sigma.shape:  print( 'ERROR: Shape mismatch' ) 
# 
# 
# gamma_sigmas = []
# heat_sigmas = []
# for alpha in alpha_vals:
#   gamma_sigma = Modify_Rates_sigmoid( z, uvb_rates, ( 4.8, 6.0 ), alpha, 0 )
#   gamma_sigmas.append( gamma_sigma )
#   heat_sigma = gamma_sigma 
# 
# font_size = 16
# 
# ncols, nrows = 2, 1
# fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))
# 
# ax = ax_l[0]
# ax.plot( z, gamma * 1e12, )
# for alpha, gamma_sigma in zip( alpha_vals, gamma_sigmas ):
#   label = r'$\alpha = {0}$'.format(alpha)
#   ax.plot( z, gamma_sigma * 1e12, '--', label=label )
# # ax.plot( z, gamma_new * 1e12, )
# 
# ax.legend(loc=1, frameon=False, prop=prop)
# ax.set_yscale( 'log' )
# ax.set_xlim( 2, 6.5)
# ax.set_ylim( 9e-2, 2)
# ax.set_xlabel(r'$z$', fontsize=font_size )
# ax.set_ylabel(r'$\Gamma_{\mathrm{HI}}$', fontsize=font_size )
# 
# ax = ax_l[1]
# ax.plot( z, heat * 1e11, )
# # for alpha, gamma_sigma in zip( alpha_vals, gamma_sigmas ):
# #   label = r'$\alpha = {0}$'.format(alpha)
# #   ax.plot( z, gamma_sigma * 1e12, '--', label=label )
# # ax.plot( z, gamma_new * 1e12, )
# 
# ax.legend(loc=1, frameon=False, prop=prop)
# ax.set_yscale( 'log' )
# ax.set_xlim( 2, 6.5)
# ax.set_ylim( 9e-2, 2)
# ax.set_xlabel(r'$z$', fontsize=font_size )
# ax.set_ylabel(r'$\mathcal{H}_{\mathrm{HI}}$', fontsize=font_size )
# 
# 
# file_name = output_dir + 'HI_UVB_rates_sigmoid.png'
# fig.savefig( file_name,  pad_inches=0.1, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor())
# print('Saved Image: ', file_name)
# 
# 