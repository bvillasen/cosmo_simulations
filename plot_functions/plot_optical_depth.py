import sys, os
import numpy as np
import h5py as h5
import matplotlib as mpl
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from colors import *
from interpolation_functions import interp_line_cubic
from data_optical_depth import *


import matplotlib
matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/fonts/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'


colors_data = [ green, purple, dark_blue, cyan ]
colors_data = [ green, purple, orange, cyan ]
colors_data = [ green, 'C3', light_orange, purple, cyan ]


colors_lines = [ 'C0', 'C1' ]

 
def Plot_tau_HI( output_dir,  points_tau=None, samples_tau_HI=None, labels='', black_background=False, figure_name='fig_tau_HI.png' ):

  if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=12)
  if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)
  if system == 'Tornado': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)
  if system == 'Eagle': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)

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
    
  fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8*ncols,6*nrows))
  colors_new = ['C0', 'C1']

  if samples_tau_HI:
    for data_id in samples_tau_HI:
      samples = samples_tau_HI[data_id]
      z = samples['z']
      tau = samples['tau']
      color_line = colors_lines[data_id]
      if 'line_color' in samples: color_line = samples['line_color']
      if 'label' in samples: label = samples['label']
      else: label = ''
      ls = '-'
      if 'ls' in samples: ls = samples['ls']
      lw = 1.5
      if 'lw' in samples: lw = samples['lw']
      ax.plot( z, tau, color=color_line, zorder=1, label=label, ls=ls, lw=lw )
      if 'high' in samples and 'low' in samples:
        high = samples['high']
        low  = samples['low']
        ax.fill_between( z, high, low, color=color_line, alpha=0.6 )
        
  if points_tau is not None:
    for data_id in points_tau:
      points = points_tau[data_id]
      z = points['z']
      mean = points['mean'] 
      high = points['higher'] 
      low = points['lower'] 
      yerr = [ mean-low, high-mean ]
      label = ''
      if 'label' in points: label = points['label']
      if 'color' in points: color = points['color']
      else: color = 'C0'
      ax.errorbar( z, mean, yerr=yerr, fmt='o', label=label, zorder=3, alpha=0.6, color=color )
  # data_set = data_optical_depth_Bosman_2020
  # data_name = data_set['name']
  # data_z = data_set['z']
  # data_tau = data_set['tau'] 
  # data_tau_sigma = data_set['tau_sigma'] 
  # color = colors_data[0]
  # ax.errorbar( data_z, data_tau, yerr=data_tau_sigma, fmt='o', color=color, label=data_name, zorder=2 )
  # 
  # data_set = data_optical_depth_Bosman_2021
  # data_name = data_set['name']
  # data_z = data_set['z']
  # data_tau = data_set['tau'] 
  # data_tau_sigma = data_set['tau_sigma'] 
  # color = colors_data[1]
  # ax.errorbar( data_z, data_tau, yerr=data_tau_sigma, fmt='o', color=color, label=data_name, zorder=2 )
  # 
  # 
  
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

  
  ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )

  ax.set_ylabel( r'HI $\tau_{\mathrm{eff}}$', fontsize=font_size, color=text_color  )
  ax.set_xlabel( r'Redshift  $z$', fontsize=font_size, color=text_color )
  ax.set_xlim( 2, 6.4 )
  ax.set_ylim( .1, 12 )
  ax.set_yscale('log')

  leg = ax.legend(loc=2, frameon=False, fontsize=22, prop=prop)
  for text in leg.get_texts():
    plt.setp(text, color = text_color)

  if black_background: 
    fig.patch.set_facecolor('black') 
    ax.set_facecolor('k')
    [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]
      
  [sp.set_linewidth(border_width) for sp in ax.spines.values()]

  figure_name = output_dir + figure_name
  fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
  print( f'Saved Figure: {figure_name}' )



    
  
