import os, sys
from os import listdir
from os.path import isfile, join
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import Load_Skewers_File
from spectra_functions import Compute_Skewers_Transmitted_Flux

sim_dir = data_dir + 'cosmo_sims/1024_50Mpc/'
input_dir_0 = sim_dir + 'analysis_files_grackle/'
input_dir_1 = sim_dir + 'analysis_files_cholla/'
output_dir = sim_dir + 'figures/'
create_directory( output_dir ) 

input_dirs = [ input_dir_0, input_dir_1 ]

# Box parameters
Lbox = 50000.0 #kpc/h
box = {'Lbox':[ Lbox, Lbox, Lbox ] }

file_indices = range( 13, 56 )

data_all = {}
for sim_id, input_dir in enumerate(input_dirs):

  z_vals, F_mean_vals = [], []
  for n_file in file_indices:
    
    file_name = input_dir + f'{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    lya_stats = file['lya_statistics']
    F_mean = lya_stats.attrs['Flux_mean_HI'][0]
    z_vals.append( z )
    F_mean_vals.append( F_mean )
    
    
  z_vals = np.array( z_vals )
  F_mean_vals = np.array( F_mean_vals )
  tau_vals = -np.log(F_mean_vals)
  data_all[sim_id] = { 'z_vals':z_vals, 'F_mean_vals':F_mean_vals, 'tau_vals':tau_vals }



import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'


label_size = 12
figure_text_size = 14
tick_label_size_major = 12
tick_label_size_minor = 11
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
text_color = 'black'
legend_font_size = 11

ncols, nrows = 1, 1.
ax_lenght = 6
fig_width = ncols * ax_lenght
fig_height = nrows * ax_lenght 
h_length = 4
main_length = 3

fig = plt.figure(0)
fig.set_size_inches(fig_width, fig_height )
fig.clf()

gs = plt.GridSpec(h_length, ncols)
gs.update(hspace=0.0, wspace=0.18, )


i = 0 
ax1 = plt.subplot(gs[0:main_length, i])
ax2 = plt.subplot(gs[main_length:h_length, i])

z_vals = data_all[0]['z_vals']
tau_0 = data_all[0]['tau_vals']
tau_1 = data_all[1]['tau_vals']

diff = ( tau_1 - tau_0 ) / tau_0

xmin, xmax = z_vals.min(), z_vals.max()
xmin, xmax = 2, 6

ax1.plot( z_vals, tau_0, ls='-',  c='C0', label='Grackle' )
ax1.plot( z_vals, tau_1, ls='--', c='C1', label='Cholla' )

ax1.legend( frameon=False, loc=2 )
ax1.set_yscale('log') 
ax1.set_xlim( xmin, xmax )
ax1.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax1.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax1.tick_params(axis='x', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=0, size=tick_size_major, width=tick_width_major  )

ax1.set_ylabel( r'$\tau$', fontsize=label_size )
 
ax2.axhline( y=0, c='C0')
ax2.plot( z_vals, diff, ls='--', c='C1', label='Cholla' )
ax2.set_ylim( -0.04, 0.04 )
ax2.set_xlim( xmin, xmax )
ax2.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax2.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
ax2.set_ylabel( r'$\Delta \tau / \tau$', fontsize=label_size )
ax2.set_xlabel( r'Redshift  $z$', fontsize=label_size )
 
figure_name = output_dir + f'tau_comparison.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


