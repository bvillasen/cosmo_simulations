import sys, os
import numpy as np
import h5py as h5
import matplotlib as mpl
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from data_thermal_history import *
from tools import *
from colors import *
from interpolation_functions import interp_line_cubic
from data_optical_depth import *


import matplotlib
import matplotlib.font_manager
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

colors_data = [ orange, purple, dark_blue, cyan ]

def Plot_tau_HI( samples_tau_HI, output_dir, system='Shamrock', labels='', black_background = False ):

  if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=12)
  if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)

  nrows = 1
  ncols = 1
  
  tick_size_major, tick_size_minor = 6, 4
  tick_label_size_major, tick_label_size_minor = 14, 12
  tick_width_major, tick_width_minor = 1.5, 1

  font_size = 18
  label_size = 16
  alpha = 0.7
  
  line_width = 0.6
  
  border_width = 1.5

  text_color  = 'black'
  if black_background:  text_color = 'white'
    
  fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))
  colors_new = ['C0', 'C1']


  # for data_id in samples_tau_HI_multiple:
  #   colormap = color_map_list[data_id]
  #   colors = colormap.mpl_colors
  #   n_colors = len( colors )
  #   if use_color_from_colormap: color_line = colors[n_colors//2]
  #   else:color_line = color_lines_list[data_id]
  #   if black_background:
  #     colormap = color_map_list_balck[data_id]
  #     colors = colormap.mpl_colors
  #     color_line = colors[4]
  #     color_bar  = colors[4]
  # 
  # 
  #   label = labels_multiple[data_id]
  #   samples = samples_tau_HI_multiple[data_id]
  #   z = samples['z']
  #   mean = samples['mean']
  #   high = samples['higher']
  #   low = samples['lower']
  #   if 'Highest_Likelihood' in samples:
  #     print( 'Plotting Highest_Likelihood T0')
  #     mean = samples['Highest_Likelihood']
  #   # ax.plot( z, mean, color=color_line, zorder=1, label=label )
  #   # ax.fill_between( z, high, low, color=color_line, alpha=alpha, zorder=1 )  
  #   sort_indices = np.argsort( z )
  #   z = z[sort_indices]
  #   mean = mean[sort_indices]
  #   high = high[sort_indices]
  #   low  = low[sort_indices]
  #   n_samples_intgerp = 10000
  #   z_interp = np.linspace( z[0], z[-1], n_samples_intgerp )  
  #   f_mean = interp.interp1d( z, mean, kind='cubic' )
  #   f_high = interp.interp1d( z, high, kind='cubic' )
  #   f_low  = interp.interp1d( z, low,  kind='cubic' )
  #   color_line = colors_new[data_id]
  #   ax.plot( z_interp, f_mean(z_interp), color=color_line, zorder=1, label=label )
  #   ax.fill_between( z_interp, f_high(z_interp), f_low(z_interp), color=color_line, alpha=alpha, zorder=1 )  
  
  data_set = data_optical_depth_Bosman_2020
  data_name = data_set['name']
  data_z = data_set['z']
  data_tau = data_set['tau'] 
  data_tau_sigma = data_set['tau_sigma'] 
  color = colors_data[0]
  ax.errorbar( data_z, data_tau, yerr=data_tau_sigma, fmt='o', color=color, label=data_name, zorder=2 )
  
  data_set = data_optical_depth_Bosman_2021
  data_name = data_set['name']
  data_z = data_set['z']
  data_tau = data_set['tau'] 
  data_tau_sigma = data_set['tau_sigma'] 
  color = colors_data[1]
  ax.errorbar( data_z, data_tau, yerr=data_tau_sigma, fmt='o', color=color, label=data_name, zorder=2 )
  
  data_set = data_optical_depth_Becker_2013
  data_name = data_set['name']
  data_z = data_set['z']
  data_tau = data_set['tau'] 
  tau_p = data_set['tau_sigma_p']
  tau_m = data_set['tau_sigma_m']
  tau_error = [ data_tau - tau_m , tau_p - data_tau  ]
  color = colors_data[2]
  ax.errorbar( data_z, data_tau, yerr=tau_error, fmt='o', color=color, label=data_name, zorder=2 )
  
  data_set = data_optical_depth_Yang_2020
  data_name = data_set['name']
  data_z = data_set['z']
  data_tau = data_set['tau'] 
  data_tau_sigma = data_set['tau_sigma'] 
  color = colors_data[3]
  ax.errorbar( data_z, data_tau, yerr=data_tau_sigma, fmt='o', color=color, label=data_name, zorder=2 )

  ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )

  ax.set_ylabel( r'$\tau_{eff} \,\, \mathrm{HI}$', fontsize=font_size, color=text_color  )
  ax.set_xlabel( r'$z$', fontsize=font_size, color=text_color )
  ax.set_xlim( 2, 6.3 )
  ax.set_ylim( .1, 10 )
  ax.set_yscale('log')

  leg = ax.legend(loc=2, frameon=False, fontsize=22, prop=prop)
  for text in leg.get_texts():
    plt.setp(text, color = text_color)

  if black_background: 
    fig.patch.set_facecolor('black') 
    ax.set_facecolor('k')
    [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]
      
  [sp.set_linewidth(border_width) for sp in ax.spines.values()]

  figure_name = output_dir + f'fig_tau_HI_sampling.png'
  fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
  print( f'Saved Figure: {figure_name}' )



    
  
