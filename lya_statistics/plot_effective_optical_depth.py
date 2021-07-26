import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
cosmo_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
sys.path.append( cosmo_dir + 'lya_statistics/data' )
from tools import *
from data_optical_depth import *
from colors import * 
from stats_functions import compute_distribution, get_highest_probability_interval
from plot_optical_depth import Plot_tau_HI


input_dir_0 = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc/analysis_files/'
input_dir_1 = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_modified_gamma/analysis_files/'
output_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_modified_gamma/figures/'
create_directory( output_dir ) 

input_dirs = [ input_dir_0, input_dir_1 ]

data_tau = {}
for data_id, input_dir in enumerate(input_dirs):
  z_vals, F_vals = [], []
  for n_file in range(10,56):
    file_name = input_dir + f'{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    F_mean =file['lya_statistics'].attrs['Flux_mean_HI'][0]
    z_vals.append( z )
    F_vals.append( F_mean )
  z_vals = np.array( z_vals )
  F_vals = np.array( F_vals )
  tau_vals = -np.log( F_vals )
  data_tau[data_id] = { 'z':z_vals, 'tau_vals':tau_vals  }

data_tau[0]['label'] = 'Modified P19'
data_tau[1]['label'] = 'Modified from Equilibrium to match HI '


Plot_tau_HI(output_dir, samples_tau_HI=data_tau, labels='', black_background = False, figure_name='fig_HI_tau_modified_gamma.png'  )


# 
# data_sets = [ data_optical_depth_Becker_2013, data_optical_depth_Bosman_2018, data_optical_depth_Bosman_2021 ]
# 
# 
# 
# data_colors = [ orange, greens[3], yellows[2] ]
# 
# font_size = 16
# tick_size_major, tick_size_minor = 6, 4
# tick_label_size_major, tick_label_size_minor = 14, 12
# tick_width_major, tick_width_minor = 1.5, 1
# border_width = 1.5
# 
# 
# text_color = 'black'
# 
# 
# black_background = True
# 
# color_line = 'C0'
# 
# if black_background:
#   text_color = 'white'
#   color_line = blues[4]
# 
# matplotlib.rcParams['mathtext.fontset'] = 'cm'
# matplotlib.rcParams['mathtext.rm'] = 'serif'
# if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=12)
# if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)
# 
# 
# nrows, ncols = 1, 1
# fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))
# plt.subplots_adjust( hspace = 0.1, wspace=0.1)
# 
# 
# ax.plot( z_vals, tau_vals, c=color_line, zorder=1, label='This Work (Modified P19)' )
# ax.fill_between( z_vals, tau_low, tau_high, color=color_line, zorder=1, alpha=0.5  )
# 
# 
# for i, data_set in enumerate(data_sets):
#   z = data_set['z']
#   tau = data_set['tau']
#   sigma_tau = data_set['tau_sigma']
#   data_name = data_set['name']
#   color = data_colors[i]
#   ax.errorbar( z, tau, yerr=sigma_tau, fmt='o', color=color, label=data_name, zorder=2 )
# 
# ax.set_ylabel( r'$\mathrm{Ly\alpha} \,\,\tau_{eff}  $', fontsize=font_size, color=text_color  )
# ax.set_xlabel( r'$z$', fontsize=font_size, color=text_color )
# 
# ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
# ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
# 
# leg = ax.legend(loc=2, frameon=False, fontsize=22, prop=prop)
# for text in leg.get_texts():
#   plt.setp(text, color = text_color)
# 
# if black_background: 
#   fig.patch.set_facecolor('black') 
#   ax.set_facecolor('k')
#   [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]
# 
# [sp.set_linewidth(border_width) for sp in ax.spines.values()]
# 
# 
# ax.set_xlim(2.0, 6.3)
# ax.set_ylim(0.1, 10)
# 
# ax.set_yscale('log')
# 
# figure_name = output_dir + f'fig_effective_optical_depth_HI.png'
# fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
# print( f'Saved Figure: {figure_name}' )