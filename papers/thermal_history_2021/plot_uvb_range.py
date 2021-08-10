import os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
base_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from generate_grackle_uvb_file import Extend_Rates_Redshift, Modify_Rates_From_Grackle_File, Load_Grackle_File, Copy_Grakle_UVB_Rates
from colors import *

output_dir = data_dir + 'cosmo_sims/figures/nature/'
create_directory( output_dir ) 



param_vals = {}
param_vals[0] = [  0.1, 0.3, 0.53, 0.76, 1.0]
param_vals[1] = [ 0.6, 0.73, 0.86, 1.0 ]
param_vals[2] = [ -0.1, 0.2, 0.5, 0.8 ]
param_vals[3] = [ -0.6, -0.4, -0.2, 0.0, 0.2 ]

max_delta_z = 0.1

# Load the Original Rates
grackle_file_name = base_dir + 'rates_uvb/data/CloudyData_UVB_Puchwein2019_cloudy.h5'
rates_P19 = Load_Grackle_File( grackle_file_name )
rates_P19_ext = Extend_Rates_Redshift( max_delta_z, rates_P19 )
input_rates = Copy_Grakle_UVB_Rates( rates_P19_ext )
uvb_parameters = { 'scale_He':1, 'scale_H':0.78, 'deltaZ_He':0, 'deltaZ_H':0.05 }
rates_P19m = Modify_Rates_From_Grackle_File( uvb_parameters,  rates_data=input_rates, extrapolate='spline' )
  
param_combinations = Get_Parameters_Combination( param_vals )  
    
rates_all = {}
for id, p_vals in enumerate(param_combinations):
  rates_data = Copy_Grakle_UVB_Rates( rates_P19 )
  rates_data = Extend_Rates_Redshift( max_delta_z, rates_data )
  uvb_parameters = { 'scale_He':p_vals[0], 'scale_H':p_vals[1], 'deltaZ_He':p_vals[2], 'deltaZ_H':p_vals[3] }
  uvb_rates = Modify_Rates_From_Grackle_File( uvb_parameters,  rates_data=rates_data, extrapolate='spline' )
  rates_all[id] = uvb_rates

z = rates_all[0]['UVBRates']['z'] 
n_points = len(z)

keys = { 'Chemistry':[ 'k24', 'k26', 'k25' ], 'Photoheating':[ 'piHI', 'piHeI', 'piHeII' ] }

# rates_extreme = {}
# for root_key in keys:
#   rates_range[root_key] = {}
#   for key in keys[root_key]:



rates_range  = {}
for root_key in keys:
  rates_range[root_key] = {}
  for key in keys[root_key]:
    rates_max, rates_min = [], []
    for z_indx in range(n_points):
      vmax, vmin = -np.inf, np.inf
      for rates_id in rates_all:
        rate_val = rates_all[rates_id]['UVBRates'][root_key][key][z_indx]
        # print( rate_val )
        vmax = max( vmax, rate_val )
        vmin = min( vmin, rate_val )          
        
        # print( vmin, vmax)
      rates_max.append( vmax )
      rates_min.append( vmin )
    rates_range[root_key][key] = { 'max': np.array(rates_max), 'min':np.array(rates_min) }
         
  
for root_key in keys:
  for key in keys[root_key]:
    if key in  ['k24', '26', 'piHI', 'piHeI']:
      rate_P19ext = rates_P19_ext['UVBRates'][root_key][key]
      z_P19ext =  rates_P19_ext['UVBRates']['z']
      rate_max = rates_range[root_key][key]['max']
      n = len(z_P19ext)
      for i in range( n ):
        z_val = z_P19ext[i]
        if z_val > 6:
          rate_log = np.log10(rate_P19ext)
          delta_z = 0.05
          rate_interp = np.interp( z_val, z_P19ext+delta_z, rate_log  )
          rate_interp = 10**rate_interp
          # rate_max[i] = min( rate_max[i], rate_interp )
        

for indx in range(len(z)):
  for id in rates_all:
    rates = rates_all[id]['UVBRates']


tick_label_size_major = 16
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
font_size = 20
legend_font_size = 20




ylabels = {0:r'HI photoionization rate  $\Gamma_{\mathrm{HI}}$   [s$^{-1}$]',
           1:r'HeI photoionization rate  $\Gamma_{\mathrm{HeI}}$   [s$^{-1}$]',
           2:r'HeII photoionization rate  $\Gamma_{\mathrm{HeII}}$   [s$^{-1}$]',
           3:r'HI photoheating rate  $\mathcal{H}_{\mathrm{HI}}$   [eV s$^{-1}$]',
           4:r'HeI photoheating rate  $\mathcal{H}_{\mathrm{HeI}}$   [eV s$^{-1}$]',
           5:r'HeII photoheating rate  $\mathcal{H}_{\mathrm{HeII}}$   [eV s$^{-1}$]',
}


color_line = dark_purple
color_band = sky_blue

matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

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

    # for rates_id in rates_all:
    #   rates = rates_all[rates_id] 
    #   z = rates['UVBRates']['z']
    #   rate = rates['UVBRates'][root_key][key]
    #   ax.plot( z, rate,  )
    
    if key in [ 'piHeII', 'k25' ]: 
      rates = rates_P19
      delta_z = 0.8
      factor = 1
    else: 
      rates = rates_P19m
      delta_z = 0.2
      factor = 1/0.78
      
    z_P19 = rates['UVBRates']['z'] 
    rate_P19 = rates['UVBRates'][root_key][key] * factor
    ax.plot( z_P19, rate_P19, color=color_line, label='P19' )
    
    # z_P19 = rates['UVBRates']['z'] 
    # rate_P19 = rates['UVBRates'][root_key][key] * factor
    # ax.plot( z_P19+delta_z, rate_P19, color=color_line,  )
    # z_indices = z_P19 >=5.5
    # z_fill = z_P19[z_indices] + delta_z
    # max_fill = rate_P19[z_indices]
    # min_fill = max_fill * 0.6
    # ax.fill_between( z_fill, max_fill, min_fill , alpha=0.6, color=color_band, label='Simulated Range' )


    
    # 
    max = rates_range[root_key][key]['max']
    min = rates_range[root_key][key]['min']
    ax.fill_between( z, max, min , alpha=0.6, color=color_band, label='Simulated Range' )

    ylabel = ylabels[id]
    ax.set_ylabel( ylabel, fontsize=font_size  )
    ax.set_xlabel( r'$z$', fontsize=font_size+2 )     
    ax.set_yscale('log')
    ax.set_xlim( 0, 14 )
    ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
    
    ax.legend( loc=1, frameon=False, fontsize=font_size-3)

figure_name = output_dir + 'uvb_rates_range.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300 )
print( f'Saved Figure: {figure_name}' )
