import sys, os
import numpy as np
import h5py as h5
import palettable
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import pylab
import pickle
from matplotlib.legend_handler import HandlerTuple
import os, sys
root_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from plot_thermal_history import Plot_T0_gamma_evolution
from colors import *
from figure_functions import *
from data_optical_depth import *
from data_optical_depth_HeII import data_tau_HeII_Worserc_2019
from interpolation_functions import smooth_line
from interpolation_functions import interp_line

proj_dir = data_dir + 'projects/thermal_history/'
grid_dir = proj_dir + 'data/sim_grid/1024_P19m_np4_nsim400/'
mcmc_dir = grid_dir + 'fit_mcmc/'

black_background = False

output_dir = proj_dir + 'figures/'
if black_background: output_dir += 'black_background/'
create_directory( output_dir )


data_name = 'fit_results_simulated_HM12_systematic'
print(f'Loading Dataset: {data_name}' )
input_dir = mcmc_dir + f'{data_name}/observable_samples/' 

# Obtain distribution of all the fields
file_name = input_dir + 'samples_fields.pkl'
samples_fields = Load_Pickle_Directory( file_name )
samples_tau = samples_fields['tau']
samples_tau_He = samples_fields['tau_HeII']
 
z_vals, tau_vals, tau_He_vals = [], [], []
input_dir = proj_dir + 'data/1024_50Mpc_HM12/analysis_files/'
for n_file in range( 56 ):
  file_name = input_dir + f'{n_file}_analysis.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z'][0]
  F_mean = file['lya_statistics'].attrs['Flux_mean_HI'][0]
  F_mean_He = file['lya_statistics'].attrs['Flux_mean_HeII'][0]
  tau = -np.log( F_mean )
  tau_He = -np.log( F_mean_He )
  z_vals.append(z)
  tau_vals.append(tau)
  tau_He_vals.append(tau_He)
z_vals = np.array(z_vals)
tau_vals = np.array(tau_vals)
tau_He_vals = np.array(tau_He_vals)

tick_size_major, tick_size_minor = 6, 4
tick_label_size_major, tick_label_size_minor = 12, 12
tick_width_major, tick_width_minor = 1.5, 1

font_size = 16
legend_font_size = 12
alpha = 0.5
border_width = 1.5

text_color = 'k'
  
colors_data = [ green, 'C3', light_orange, purple, cyan ]

nrows, ncols = 1, 2
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.15)

ax = ax_l[0]
z = samples_tau['z']
tau = samples_tau['Highest_Likelihood']
tau_h = samples_tau['higher'] * 1.03
tau_l = samples_tau['lower'] * 0.97
ax.plot( z, tau, c='k', label='Best-Fit to HM12' )
ax.fill_between( z, tau_h, tau_l, color='k', alpha=0.5 )
ax.plot( z_vals, tau_vals, c='C4', label='HM12' )
xmin, xmax = 2, 6.3
ymin, ymax = .12, 10
ax.set_xlim( xmin, xmax )
ax.set_ylim( ymin, ymax )


marker_size = 5
data_set = data_optical_depth_Becker_2013
data_name = data_set['name']
data_z = data_set['z']
data_tau = data_set['tau'] 
tau_p = data_set['tau_sigma_p']
tau_m = data_set['tau_sigma_m']
tau_error = [ data_tau - tau_m , tau_p - data_tau  ]
color = colors_data[2]
ax.errorbar( data_z, data_tau, yerr=tau_error, fmt='o', color=color, label=data_name, zorder=2, ms=marker_size )

data_set = data_optical_depth_Boera_2019
data_name = data_set['name']
data_z = data_set['z']
data_tau = data_set['tau'] 
data_tau_sigma = data_set['tau_sigma'] 
color = colors_data[0]
ax.errorbar( data_z, data_tau, yerr=data_tau_sigma, fmt='o', color=color, label=data_name, zorder=2, ms=marker_size )

data_set = data_optical_depth_Yang_2020
data_name = data_set['name']
data_z = data_set['z']
data_tau = data_set['tau'] 
data_tau_sigma = data_set['tau_sigma'] 
color = colors_data[3]
ax.errorbar( data_z, data_tau, yerr=data_tau_sigma, fmt='o', color=color, label=data_name, zorder=2, ms=marker_size )

data_set = data_optical_depth_Eilers_2018
data_name = data_set['name']
data_z = data_set['z']
data_tau = data_set['tau'] 
data_tau_sigma = data_set['tau_sigma'] 
color = colors_data[4]
ax.errorbar( data_z, data_tau, yerr=data_tau_sigma, fmt='o', color=color, label=data_name, zorder=2, ms=marker_size )
z_low = data_set['lower_limits']['z']
tau_low = data_set['lower_limits']['tau']
yerr = [  np.zeros_like(tau_low), tau_low*0.12 ]
ax.errorbar( z_low, tau_low, yerr=yerr, fmt='o', lolims=True, color=color, zorder=2, ms=marker_size )





data_set = data_optical_depth_Bosman_2018
data_name = data_set['name']
data_z = data_set['z']
data_tau = data_set['tau'] 
data_tau_sigma = data_set['tau_sigma'] 
color = colors_data[1]
ax.errorbar( data_z, data_tau, yerr=data_tau_sigma, fmt='o', color=color, label=data_name, zorder=2,  ms=marker_size )


data_set = data_optical_depth_Fan_2006
data_name = data_set['name']
data_z = data_set['z']
data_tau = data_set['tau'] 
data_tau_sigma = data_set['tau_sigma'] 
color = 'C1'
ax.errorbar( data_z, data_tau, yerr=data_tau_sigma, fmt='o', color=color, label=data_name, zorder=2, ms=marker_size )
z_low = data_set['lower_limits']['z']
tau_low = data_set['lower_limits']['tau']
sigma_low = data_set['lower_limits']['tau_sigma']
yerr = [  sigma_low, sigma_low ]
ax.errorbar( z_low, tau_low, yerr=yerr, fmt='o', lolims=True, color=color, zorder=2, ms=marker_size )


ax.set_yscale('log')
ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax.set_ylabel( r'$\tau_\mathrm{eff,H}$', fontsize=font_size, color=text_color  )
ax.set_xlabel( r'Redshift  $z$', fontsize=font_size, color=text_color )
[sp.set_linewidth(border_width) for sp in ax.spines.values()] 
leg = ax.legend(loc=2, frameon=False, fontsize=12 )
  
ax = ax_l[1]
z = samples_tau_He['z']
tau = samples_tau_He['Highest_Likelihood']
tau_h = samples_tau_He['higher'] * 1.03
tau_l = samples_tau_He['lower'] * 0.97
z_vals = z
n_samples_interp = 1000
z_interp = np.linspace( z_vals[0], z_vals[-1], n_samples_interp ) 
kind = 'cubic'
tau   = interp_line( z_vals, z_interp, tau,   kind=kind )
tau_h = interp_line( z_vals, z_interp, tau_h, kind=kind )
tau_l = interp_line( z_vals, z_interp, tau_l, kind=kind )

ax.plot( z_interp, tau, c='k', label='Best-Fit to HM12' )
ax.fill_between( z_interp, tau_h, tau_l, color='k', alpha=0.5 )
ax.plot( z_vals, tau_He_vals, c='C4', label='HM12' )
xmin, xmax = 2, 3.4
ymin, ymax = .1, 7
ax.set_xlim( xmin, xmax )
ax.set_ylim( ymin, ymax )


color_data_tau = light_orange
data_set = data_tau_HeII_Worserc_2019
data_name = data_set['name']
data_z = data_set['z']
data_tau = data_set['tau'] 
data_tau_sigma = data_set['tau_sigma'] 
tau_p = data_set['tau_sigma_p']
tau_m = data_set['tau_sigma_m']
tau_error = [ data_tau - tau_m , tau_p - data_tau  ]
points = ax.errorbar( data_z, data_tau, yerr=tau_error, fmt='o', color=color_data_tau, label=data_name, zorder=4)


lower_lims = [  [3.16, 5.2] ]
x_lenght = 0.025/4
for lower_lim in lower_lims:
  lim_x, lim_y = lower_lim
  ax.plot( [lim_x-x_lenght, lim_x+x_lenght], [lim_y, lim_y], color=color_data_tau,  zorder=4  )
  dx, dy = 0, 1
  ax.arrow( lim_x, lim_y, dx, dy,  color=color_data_tau, head_width=0.01, head_length=0.08,  zorder=4   )

ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax.set_ylabel( r'$\tau_\mathrm{eff,H}$', fontsize=font_size, color=text_color  )
ax.set_xlabel( r'Redshift  $z$', fontsize=font_size, color=text_color )
[sp.set_linewidth(border_width) for sp in ax.spines.values()] 
leg = ax.legend(loc=2, frameon=False, fontsize=12 )


figure_name = output_dir + 'hm12_tau.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
  
  


  

