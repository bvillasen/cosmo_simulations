import os, sys
import numpy as np
import matplotlib.pyplot as plt
base_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from uvb_functions import Reaplace_Gamma_Parttial, Load_Grackle_File, Modify_UVB_Rates, Extend_Rates_Redshift, Copy_Grakle_UVB_Rates, Modify_UVB_Rates, Write_Rates_Grackle_File
from plot_uvb_rates import Plot_UVB_Rates
from figure_functions import *
from colors import *

# output_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_modified_gamma/'
# output_dir = data_dir + 'thermal/'
output_dir = data_dir + 'cosmo_sims/figures/nature/'
create_directory( output_dir ) 


# Load the Original Rates
grackle_file_name = base_dir + 'rates_uvb/data/CloudyData_UVB_Puchwein2019_cloudy.h5'
rates_P19 = Load_Grackle_File( grackle_file_name )

tick_label_size_major = 16
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
font_size = 20
legend_font_size = 20


colors = [ sky_blue, ocean_green, ocean_blue, dark_purple ]

scale_He_vals = [ 0.3, 0.5, 0.7, 0.9  ][::-1]
scale_H_vals = [ 0.4, 0.6, 0.8, 1.0  ][::-1]

ylabels = {0:r'HI photoionization rate  $\Gamma_{\mathrm{HI}}$   [s$^{-1}$]',
           1:r'HeI photoionization rate  $\Gamma_{\mathrm{HeI}}$   [s$^{-1}$]',
           2:r'HeII photoionization rate  $\Gamma_{\mathrm{HeII}}$   [s$^{-1}$]',
           3:r'HI photoheating rate  $\mathcal{H}_{\mathrm{HI}}$   [eV s$^{-1}$]',
           4:r'HeI photoheating rate  $\mathcal{H}_{\mathrm{HeI}}$   [eV s$^{-1}$]',
           5:r'HeII photoheating rate  $\mathcal{H}_{\mathrm{HeII}}$   [eV s$^{-1}$]',
}


nrows = 2
ncols = 3
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows), sharex='col')
plt.subplots_adjust( hspace = 0.0, wspace=0.15)

keys_ion  = [ 'k24', 'k26', 'k25' ]
keys_heat = [ 'piHI', 'piHeI', 'piHeII' ]

for i in range(nrows):
  for j in range(ncols):
    ax = ax_l[i][j]
    id = i*ncols + j
    if i == 0: 
      root_key = 'Chemistry'
      key = keys_ion[j]
    if i == 1: 
      root_key = 'Photoheating'
      key = keys_heat[j]
      
    z = rates_P19['UVBRates']['z']
    rate = rates_P19['UVBRates'][root_key][key]
    if j < 2: 
      scale_vals = scale_H_vals
      label_base = r'$\beta_\mathrm{H}\,=\,$' 
    else:     
      scale_vals = scale_He_vals
      label_base = r'$\beta_\mathrm{He}\,=\,$'
      
    
    for indx,scale in enumerate(scale_vals):
      label = label_base + r'${0:.1f}$'.format( scale)
      color = colors[indx]
      ax.plot( z, rate*scale, label=label, color=color )
    ax.legend( frameon=False, loc=3, fontsize=legend_font_size)
    
    ylabel = ylabels[id]
    ax.set_ylabel( ylabel, fontsize=font_size  )
    ax.set_xlabel( r'$z$', fontsize=font_size+2 )     
    ax.set_yscale('log')
    ax.set_xlim( -0.3, 15 )
    ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

    











figure_name = output_dir + 'uvb_rates_scale.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300 )
print( f'Saved Figure: {figure_name}' )
