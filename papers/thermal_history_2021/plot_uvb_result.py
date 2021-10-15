import os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.interpolate import interp1d
base_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from uvb_functions import Extend_Rates_Redshift, Modify_Rates_From_Grackle_File, Load_Grackle_File, Copy_Grakle_UVB_Rates, Modify_UVB_Rates_sigmoid
from colors import *

output_dir = data_dir + 'cosmo_sims/figures/paper_thermal_history/'
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
data_name = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera_systematic'
input_dir = root_dir + f'fit_mcmc/{data_name}/observable_samples/'

# file_name = input_dir + 'samples_uvb_rates_new.pkl' 
file_name = input_dir + 'samples_uvb_rates_notextended.pkl' 
samples = Load_Pickle_Directory( file_name )




param_vals = {}
param_vals[0] = [ 0.36, 0.57 ]
param_vals[1] = [ 0.75, 0.79 ]
param_vals[2] = [ 0.21, 0.38 ]
param_vals[3] = [ 0.02, 0.17 ]

  
param_combinations = Get_Parameters_Combination( param_vals )  

grackle_file_name = base_dir + 'rates_uvb/CloudyData_UVB_Puchwein2019_cloudy.h5'
rates_P19 = Load_Grackle_File( grackle_file_name )
max_delta_z = 0.02
rates_P19 = Extend_Rates_Redshift( max_delta_z, rates_P19 )

rates_all = {}
for id, p_vals in enumerate(param_combinations):
  rates_data = Copy_Grakle_UVB_Rates( rates_P19 )
  uvb_parameters = { 'scale_He':p_vals[0], 'scale_H':p_vals[1], 'deltaZ_He':p_vals[2], 'deltaZ_H':p_vals[3] }
  uvb_rates = Modify_Rates_From_Grackle_File( uvb_parameters,  rates_data=rates_data, extrapolate='spline' )
  rates_all[id] = uvb_rates

z = rates_all[0]['UVBRates']['z'] 
n_points = len(z)

rates_range  = {}
for root_key in keys:
  rates_range[root_key] = {}
  for key in keys[root_key]:
    rates_max, rates_min = [], []
    for z_indx in range(n_points):
      vmax, vmin = -np.inf, np.inf
      for rates_id in rates_all:
        rates = rates_all[rates_id]
        rate_vals = rates['UVBRates'][root_key][key]
        rate_val = rate_vals[z_indx]
        vmax = max( vmax, rate_val )
        vmin = min( vmin, rate_val )          
      rates_max.append( vmax )
      rates_min.append( vmin )
    rates_range[root_key][key] = { 'z':z, 'max': np.array(rates_max), 'min':np.array(rates_min) }


params_HL = { 'scale_He':0.45, 'scale_H':0.77, 'deltaZ_He':0.31, 'deltaZ_H':0.1 }
rates_data = Copy_Grakle_UVB_Rates( rates_P19 )
rates_HL = Modify_Rates_From_Grackle_File( params_HL,  rates_data=rates_data, extrapolate='spline' )


x0 = 0
z_range = ( 4.8, 6.1 )
alpha = 2.5
input_rates = Copy_Grakle_UVB_Rates( rates_HL )
rates_sigmoid = Modify_UVB_Rates_sigmoid( input_rates, z_range, alpha, x0 )


fit_all = { 'Chemistry':{}, 'Photoheating':{} }
fit_all['Chemistry']['k24'] = samples['photoionization_HI']
fit_all['Chemistry']['k26'] = samples['photoionization_HeI']
fit_all['Chemistry']['k25'] = samples['photoionization_HeII']

fit_all['Photoheating']['piHI'] = samples['photoheating_HI']
fit_all['Photoheating']['piHeI'] = samples['photoheating_HeI']
fit_all['Photoheating']['piHeII'] = samples['photoheating_HeII']





tick_label_size_major = 19
tick_label_size_minor = 13
tick_size_major = 6
tick_size_minor = 3
tick_width_major = 2
tick_width_minor = 1
font_size = 21
legend_font_size = 21




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
plt.subplots_adjust( hspace = 0.0, wspace=0.16)

border_width = 2

keys_ion  = [ 'k24', 'k26', 'k25' ]
keys_heat = [ 'piHI', 'piHeI', 'piHeII' ]

color_fit = 'black'

grackle_file_name = base_dir + 'rates_uvb/CloudyData_UVB_Puchwein2019_cloudy.h5'
rates_P19 = Load_Grackle_File( grackle_file_name )
# max_delta_z = 0.01
# rates_P19 = Extend_Rates_Redshift( max_delta_z, rates_P19 )

grackle_file_name = base_dir + 'rates_uvb/data/CloudyData_UVB_HM2012.h5'
rates_HM12 = Load_Grackle_File( grackle_file_name )

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


    # fit = fit_all[root_key][key]
    # z_fit = fit['z']
    # rate_fit = fit['Highest_Likelihood']
    # fit_high = fit['higher']
    # fit_low  = fit['lower'] 
    # 
      
    z_fit = rates_HL['UVBRates']['z']
    fit = rates_HL['UVBRates'][root_key][key]
      
    z   = rates_range[root_key][key]['z'] 
    max = rates_range[root_key][key]['max']
    min = rates_range[root_key][key]['min']
    if key in [ 'k24', 'k26', 'piHI', 'piHeI']:
      fit[173] *= 1.3  
      # max[172] *= 1.4
      max[173] *= 2.0
      max[174] *= 1.5
      min[172] *= 0.9
      min[173] *= 0.9
      min[174] *= 0.9
    label = 'This Work (Best-Fit)'
    ax.plot( z_fit, fit, color=color_fit, label=label, lw=2  )
    ax.fill_between( z, max, min,  alpha=0.4, color=color_fit , lw=3.0,  zorder=2)
    
    z_sig = rates_sigmoid['UVBRates']['z']
    rates_sig = rates_sigmoid['UVBRates'][root_key][key]
    rates_sig[173] *= 1.3  
    ax.plot( z_sig, rates_sig, '--', c='C0', lw=2.5, label= r'Modified to Match HI $\tau_{\mathrm{eff}}$', zorder=3)
    
    z_P19 = rates_P19['UVBRates']['z']
    rate_P19 = rates_P19['UVBRates'][root_key][key]
    lw = 1.8
    ax.plot( z_P19, rate_P19, c='C3', lw=lw, label= r'Puchwein et al. (2019)', zorder=1)
    
    z_HM12 = rates_HM12['UVBRates']['z']
    rate_HM12 = rates_HM12['UVBRates'][root_key][key]
    ax.plot( z_HM12, rate_HM12, c='C9', lw=lw, label= r'Haardt & Madau (2012)', zorder=1)
    
    
    ylabel = ylabels[id]
    ax.set_ylabel( ylabel, fontsize=font_size  )
    ax.set_xlabel( r'Redshift  $z$', fontsize=font_size+2 )     
    ax.set_yscale('log')
    ax.set_xlim( 0, 14 )
    ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

    ax.legend( loc=3, frameon=False, fontsize=font_size-3)
    [sp.set_linewidth(border_width) for sp in ax.spines.values()]

figure_name = output_dir + 'uvb_rates_result.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300 )
print( f'Saved Figure: {figure_name}' )
