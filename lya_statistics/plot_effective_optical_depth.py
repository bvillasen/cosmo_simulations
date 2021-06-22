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

system = 'Shamrock'

# data_dir = '/home/bruno/Desktop/ssd_0/data/'
data_dir = '/raid/bruno/data/'
# data_dir = '/data/groups/comp-astro/bruno/'
input_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc/analysis_files/'
output_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc/figures/'
create_directory( output_dir ) 


z_vals, F_vals, F_high, F_low = [], [], [], []
for n_file in range(10,56):
  file_name = input_dir + f'{n_file}_analysis.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z'][0]
  F_mean =file['lya_statistics'].attrs['Flux_mean_HI'][0]
  F_los_snap = file['lya_statistics']['skewers_x']['los_transmitted_flux_HI'][...]
  F_mean_snap = []
  for F_los in F_los_snap:
    F_mean_snap.append( F_los.mean() )
  F_mean_snap = np.array( F_mean_snap )  
  F_mean_distribution, bin_centers = compute_distribution( F_mean_snap, 100, log=False )
  F_l, F_h, F_max, sum = get_highest_probability_interval( bin_centers, F_mean_distribution, 0.67, log=True )
  z_vals.append( z )
  F_vals.append( F_mean )
  F_high.append( F_h )
  F_low.append( F_l )
z_vals = np.array( z_vals )
F_vals = np.array( F_vals )
F_high = np.array( F_high )
F_low  = np.array( F_low )
tau_vals = -np.log( F_vals )
tau_high = -np.log( F_low )
tau_low = -np.log( F_high )




data_sets = [ data_optical_depth_Becker_2013, data_optical_depth_Bosman_2018, data_optical_depth_Bosman_2021 ]



data_colors = [ orange, greens[3], yellows[2] ]

font_size = 16
tick_size_major, tick_size_minor = 6, 4
tick_label_size_major, tick_label_size_minor = 14, 12
tick_width_major, tick_width_minor = 1.5, 1
border_width = 1.5


text_color = 'black'


black_background = True

color_line = 'C0'

if black_background:
  text_color = 'white'
  color_line = blues[4]

matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'
if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=12)
if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)


nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.1)


ax.plot( z_vals, tau_vals, c=color_line, zorder=1, label='This Work (Modified P19)' )
ax.fill_between( z_vals, tau_low, tau_high, color=color_line, zorder=1, alpha=0.5  )


for i, data_set in enumerate(data_sets):
  z = data_set['z']
  tau = data_set['tau']
  sigma_tau = data_set['tau_sigma']
  data_name = data_set['name']
  color = data_colors[i]
  ax.errorbar( z, tau, yerr=sigma_tau, fmt='o', color=color, label=data_name, zorder=2 )

ax.set_ylabel( r'$\mathrm{Ly\alpha} \,\,\tau_{eff}  $', fontsize=font_size, color=text_color  )
ax.set_xlabel( r'$z$', fontsize=font_size, color=text_color )

ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )

leg = ax.legend(loc=2, frameon=False, fontsize=22, prop=prop)
for text in leg.get_texts():
  plt.setp(text, color = text_color)

if black_background: 
  fig.patch.set_facecolor('black') 
  ax.set_facecolor('k')
  [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]

[sp.set_linewidth(border_width) for sp in ax.spines.values()]


ax.set_xlim(2.0, 6.3)
ax.set_ylim(0.1, 10)

ax.set_yscale('log')

figure_name = output_dir + f'fig_effective_optical_depth_HI.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )