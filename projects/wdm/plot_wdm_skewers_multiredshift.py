import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab

cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
sys.path.append( cosmo_dir + 'lya_statistics/data' )
from tools import *
from colors import * 
from figure_functions import *


dir_cdm = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc/analysis_files/'
dir_wdm_0 = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m3.0kev/analysis_files/'
dir_wdm_1 = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m1.0kev/analysis_files/'
dir_wdm_2 = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m0.5kev/analysis_files/'
output_dir = data_dir + 'cosmo_sims/rescaled_P19/wdm/figures/skewers/'
create_directory( output_dir ) 

input_dirs = [ dir_cdm, dir_wdm_0, dir_wdm_1, dir_wdm_2 ]
n_sims = len( input_dirs )


labels = [ r'$\mathrm{CDM}$', r'$\mathrm{WDM\,\,\, m = 3.0 keV}$', r'$\mathrm{WDM\,\,\, m = 1.0 \,keV}$', r'$\mathrm{WDM\,\,\, m = 0.5 \,keV}$', ]

skewers_ids = [ 13, 789, 2089, 3257, 4078  ]

files =  [ 25, 35, 45 ]
# files =  [ 25 ]


Flux_skewers_all = {}

for z_id, n_file in enumerate( files ):
  Flux_skewers = {}
  for sim_id in range(n_sims):
    input_dir = input_dirs[sim_id]
    file_name = input_dir + f'{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    F_mean =file['lya_statistics'].attrs['Flux_mean_HI'][0]
    F_los_snap = file['lya_statistics']['skewers_x']['los_transmitted_flux_HI'][...]
    F_skewers = [ F_los_snap[skewer_id] for skewer_id in skewers_ids ]
    Flux_skewers[sim_id] = { 'F_skewers': F_skewers }
  Flux_skewers_all[z_id] = Flux_skewers


font_size = 16
tick_size_major, tick_size_minor = 6, 4
tick_label_size_major, tick_label_size_minor = 14, 12
tick_width_major, tick_width_minor = 1.5, 1
border_width = 1.5


blue = blues[4]
yellow = yellows[2]
green = greens[5]
lw_list = [3, 1.5, 1.5, 1.5]

text_color = 'black'
# colors = [ sky_blue, ocean_green, ocean_blue, dark_purple  ]    
colors = [ ocean_blue, 'C1', ocean_green,  dark_purple  ]    


colors  = [ ]


black_background = True
if black_background:
  text_color = 'white'
  # colors = [ 'C0', 'C1', green,    yellow  ]
  colors = [ yellow,  orange, light_green, 'C0'  ][::-1] 

matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'
if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=16)
if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=16)

nrows, ncols = 3, 1
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15*ncols,3.*nrows), sharex=True)
plt.subplots_adjust( hspace = 0.07, wspace=0.1 )

skewers_ids = [ 2, 1, 3]

z_vals = [ 5, 4, 3 ]

bbox_props = dict(boxstyle="round", fc="gray", ec="0.5", alpha=0.3)

for i in range( nrows ):
  ax = ax_l[i]
    
  Flux_skewers = Flux_skewers_all[i]
  for sim_id in range(n_sims):
    F_skewers = Flux_skewers[sim_id]['F_skewers']
    F = F_skewers[skewers_ids[i]]
    x = np.linspace( 0, 50, len(F) )
    ax.plot( x,  F, color=colors[sim_id], lw=lw_list[sim_id], label=labels[sim_id] )
  
  
  current_z = z_vals[i]
  text_pos_x = 0.93
  text_pos_y = 0.85
  if i == nrows - 1: text_pos_y = 0.15
  ax.text(text_pos_x, text_pos_y, r'$z={0:.1f}$'.format(current_z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=20, color='white', bbox=bbox_props) 

  
  ax.set_xlim(  0, 50 )  
  ax.set_ylim( -0.01, 1.01 )  
  
  # ax.set_ylabel( r'$\mathrm{Ly\alpha} \,\,F  $', fontsize=font_size, color=text_color  )
  ax.set_ylabel( r'Transmitted Flux', fontsize=font_size, color=text_color  )
  if i == nrows-1: ax.set_xlabel( r'$x \,\,\, [\,h^{-1}\mathrm{Mpc}\,]$', fontsize=font_size, color=text_color )

  ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )


  if i == 0:
    leg = ax.legend(bbox_to_anchor=(0.05, 1.2), loc='upper left', frameon=False, fontsize=16, ncol=4,)
    for text in leg.get_texts():
      plt.setp(text, color = text_color)

  if black_background: 
    fig.patch.set_facecolor('black') 
    ax.set_facecolor('k')
    [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]

  [sp.set_linewidth(border_width) for sp in ax.spines.values()]


figure_name = output_dir + f'fig_wdm_skewers_flux.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
