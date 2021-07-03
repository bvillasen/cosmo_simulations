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
import matplotlib
import matplotlib.pyplot as plt
from scipy import interpolate as interp 
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from data_thermal_history import *
from tools import *
from colors import *
from interpolation_functions import interp_line_cubic


def Plot_T0_evolution( output_dir, data_sets=None, system='Shamrock', label='', fig_name='fig_T0_evolution', black_background=False, interpolate_lines=True, n_samples_interp=10000 ):
  
    
  matplotlib.rcParams['mathtext.fontset'] = 'cm'
  matplotlib.rcParams['mathtext.rm'] = 'serif'



  tick_size_major, tick_size_minor = 6, 4
  tick_label_size_major, tick_label_size_minor = 12, 12
  tick_width_major, tick_width_minor = 1.5, 1

  font_size = 16
  legend_font_size = 12
  alpha = 0.6
  
  border_width = 1.5

  text_color  = 'black'
  color_line = 'C0'
  
  color_data_0 = orange
  color_data_1 = 'C3'
  
  if black_background:
    text_color = 'white'
    
  if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=legend_font_size )
  if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size )
  
  ymin, ymax = 0.6, 1.7  
  xmin, xmax = 1.95, 9  
  nrows, ncols = 1, 1
  plt.rcParams['xtick.top'] = True
  fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,6*nrows))
  
  if data_sets:
    for data_id in data_sets:
      data_set = data_sets[data_id]
      label = data_set['label']
      z = data_set['z']
      mean = data_set['line'] / 1e4
      high = data_set['high'] / 1e4
      low  = data_set['low'] / 1e4
      color = data_set['color']
      if interpolate_lines:
        z_interp = np.linspace( z[0], z[-1], n_samples_interp ) 
        mean = interp_line_cubic( z, z_interp, mean )
        high = interp_line_cubic( z, z_interp, high )
        low  = interp_line_cubic( z, z_interp, low )
        z = z_interp
      ax.plot( z, mean, color=color, zorder=1, label=label )
      ax.fill_between( z, high, low, color=color, alpha=alpha, zorder=1 )  
  # 
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
  #   ax.plot( z_interp, f_mean(z_interp) / 1e4, color=color_line, zorder=1, label=label )
  #   ax.fill_between( z_interp, f_high(z_interp) / 1e4, f_low(z_interp) / 1e4, color=color_bar, alpha=alpha, zorder=1 )  

  data_set = data_thermal_history_Gaikwad_2020a
  data_z = data_set['z']
  data_mean = data_set['T0'] 
  data_error = 0.5 * ( data_set['T0_sigma_plus'] + data_set['T0_sigma_minus'] )
  name = data_set['name']   
  ax.errorbar( data_z, data_mean/1e4, yerr=data_error/1e4, label=name, fmt='o', color= color_data_1, zorder=2)

  data_set = data_thermal_history_Gaikwad_2020b
  data_z = data_set['z']
  data_mean = data_set['T0'] 
  data_error = 0.5 * ( data_set['T0_sigma_plus'] + data_set['T0_sigma_minus'] )
  name = data_set['name']   
  ax.errorbar( data_z, data_mean/1e4, yerr=data_error/1e4, label=name, fmt='o', color= color_data_0, zorder=2)
  
  ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
  ax.set_ylabel( r'$T_0   \,\,\,\, [10^4 \,\,\,\mathrm{K}\,]$', fontsize=font_size, color=text_color  )
  ax.set_xlabel( r'$z$', fontsize=font_size, color=text_color )
  ax.set_xlim( xmin, xmax )
  ax.set_ylim( ymin, ymax)
  leg = ax.legend(loc=3, frameon=False, fontsize=22, prop=prop)
  for text in leg.get_texts():
    plt.setp(text, color = text_color)

  if black_background: 
    fig.patch.set_facecolor('black') 
    ax.set_facecolor('k')
    [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]
      
  [sp.set_linewidth(border_width) for sp in ax.spines.values()]
        
  figure_name = output_dir + f'{fig_name}'
  if black_background: figure_name += '_black'
  figure_name += '.png'
  fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
  print( f'Saved Figure: {figure_name}' )
  