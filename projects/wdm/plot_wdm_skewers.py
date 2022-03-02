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


dir_cdm = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc/analysis_files/'
dir_wdm_0 = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m3.0kev/analysis_files/'
dir_wdm_1 = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m1.0kev/analysis_files/'
dir_wdm_2 = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m0.5kev/analysis_files/'
output_dir = data_dir + 'cosmo_sims/rescaled_P19/wdm/figures/skewers/'
create_directory( output_dir ) 

input_dirs = [ dir_cdm, dir_wdm_0, dir_wdm_1, dir_wdm_2 ]
n_sims = len( input_dirs )


labels = [ r'$\mathrm{CDM}$', r'$\mathrm{WDM\,\,\, m = 3.0 keV}$', r'$\mathrm{WDM\,\,\, m = 1.0 \,keV}$', r'$\mathrm{WDM\,\,\, m = 0.5 \,keV}$', ]


n_file = 25

skewers_ids = [ 13, 789, 2089, 3257, 4078  ]

F_skewers_all = {}
for sim_id in range(n_sims):
  input_dir = input_dirs[sim_id]
  file_name = input_dir + f'{n_file}_analysis.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z'][0]
  F_mean =file['lya_statistics'].attrs['Flux_mean_HI'][0]
  F_los_snap = file['lya_statistics']['skewers_x']['los_transmitted_flux_HI'][...]
  F_skewers = [ F_los_snap[skewer_id] for skewer_id in skewers_ids ]
  F_skewers_all[sim_id] = { 'F_skewers': F_skewers }



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


black_background = False
if black_background:
  text_color = 'white'
  colors = [ 'C0', 'C1', green,    yellow  ]

matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'
if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=16)
if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=16)

nrows, ncols = 5, 1
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15*ncols,2*nrows), sharex=True)
plt.subplots_adjust( hspace = 0.05, wspace=0.1 )


for i in range( nrows ):
  ax = ax_l[i]
  
  for sim_id in range(n_sims):
    F_skewers = F_skewers_all[sim_id]['F_skewers']
    F = F_skewers[i]
    x = np.linspace( 0, 50, len(F) )
    
    ax.plot( x,  F, color=colors[sim_id], lw=lw_list[sim_id], label=labels[sim_id] )
  
  
  
  ax.set_xlim(  0, 50 )  
  ax.set_ylim( -0.01, 1.01 )  
  
  
  ax.set_ylabel( r'$\mathrm{Ly\alpha} \,\,F  $', fontsize=font_size, color=text_color  )
  ax.set_xlabel( r'$x \,\,\, [\,h^{-1}\mathrm{Mpc}\,]$', fontsize=font_size, color=text_color )

  ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )


  if i == 0:
    leg = ax.legend(bbox_to_anchor=(0.07, 1.3), loc='upper left', frameon=False, fontsize=22, prop=prop, ncol=nrows,)
    for text in leg.get_texts():
      plt.setp(text, color = text_color)

  if black_background: 
    fig.patch.set_facecolor('black') 
    ax.set_facecolor('k')
    [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]

  [sp.set_linewidth(border_width) for sp in ax.spines.values()]


figure_name = output_dir + f'fig_wdm_skewers_flux_z{z:.1f}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
