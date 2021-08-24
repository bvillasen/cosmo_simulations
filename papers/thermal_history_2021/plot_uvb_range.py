import os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.interpolate import interp1d
base_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from uvb_functions import Extend_Rates_Redshift, Modify_Rates_From_Grackle_File, Load_Grackle_File, Copy_Grakle_UVB_Rates
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

# Obtain distribution of the UVBRates
root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
data_name = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera'
input_dir = root_dir + f'fit_mcmc/{data_name}/observable_samples/'
file_name = input_dir + 'samples_uvb_rates_new.pkl' 
samples = Load_Pickle_Directory( file_name )

# keys_rate = [ 'Highest_Likelihood', 'higher', 'lower' ]
keys_rate = ['lower' ]

name = 'photoheating_HeII'
for name in [ 'photoionization_HeII', 'photoheating_HeII']:
  rate_data = samples[name]
  z_vals = rate_data['z']
  z_min =  0.275
  indices_l = z_vals < z_min
  indices_r = z_vals >= z_min
  # for key in keys_rate:
  key = 'Highest_Likelihood'
  rate = rate_data[key]
  rate_log = np.log10(rate)
  interp_func = interp1d( z_vals[indices_r], rate_log[indices_r], fill_value='extrapolate' )
  rate_extrap = interp_func(z_vals[indices_l])
  rate[indices_l] = 10**rate_extrap
  samples[name][key] = rate
  delta = 0.3
  samples[name]['higher'][indices_l] = 10**rate_extrap *( 1 + delta +0.05) 
  samples[name]['lower'][indices_l] = 10**rate_extrap *( 1 - delta ) 



fit_all = { 'Chemistry':{}, 'Photoheating':{} }
fit_all['Chemistry']['k24'] = samples['photoionization_HI']
fit_all['Chemistry']['k26'] = samples['photoionization_HeI']
fit_all['Chemistry']['k25'] = samples['photoionization_HeII']

fit_all['Photoheating']['piHI'] = samples['photoheating_HI']
fit_all['Photoheating']['piHeI'] = samples['photoheating_HeI']
fit_all['Photoheating']['piHeII'] = samples['photoheating_HeII']



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




ylabels = {0:r'HI photoionization rate  $\Gamma_{\mathrm{HI}}$   [s$^{\mathregular{-1}}$]',
           1:r'HeI photoionization rate  $\Gamma_{\mathrm{HeI}}$   [s$^\mathregular{-1}$]',
           2:r'HeII photoionization rate  $\Gamma_{\mathrm{HeII}}$   [s$^\mathregular{-1}$]',
           3:r'HI photoheating rate  $\mathcal{H}_{\mathrm{HI}}$   [eV s$^\mathregular{-1}$]',
           4:r'HeI photoheating rate  $\mathcal{H}_{\mathrm{HeI}}$   [eV s$^\mathregular{-1}$]',
           5:r'HeII photoheating rate  $\mathcal{H}_{\mathrm{HeII}}$   [eV s$^\mathregular{-1}$]',
}


color_line = dark_purple
color_band = sky_blue

matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

prop_bold = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica_bold.ttf"), size=legend_font_size)

fig_labels = [ ['a','b','c'], [ 'd', 'e', 'f'] ]

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
    ax.plot( z_P19, rate_P19, '--', color=color_line, label='P19' )


    fit = fit_all[root_key][key]
    z_fit = fit['z']
    rate_fit = fit['Highest_Likelihood']
    fit_high = fit['higher']
    fit_low  = fit['lower'] 
    color_fit = 'black'
    label = 'This Work (Best-Fit)'
    ax.plot( z_fit, rate_fit, color=color_fit, label=label  )
    ax.fill_between( z_fit, fit_high, fit_low, alpha=0.6, color=color_fit  )


    fig_label_pos_x = j * 0.27 + 0.095
    fig_label_pos_y = 0.76 - i * 0.385 + 0.1
    fig.text( fig_label_pos_x, fig_label_pos_y,  fig_labels[i][j],  fontproperties=prop_bold )
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

figure_name = output_dir + 'uvb_rates_range_new.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300 )
print( f'Saved Figure: {figure_name}' )
