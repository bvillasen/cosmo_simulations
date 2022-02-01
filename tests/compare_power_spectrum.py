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

file_indices = [ 25, 35, 45, 55 ]

data_all = {}
for sim_id, input_dir in enumerate(input_dirs):
  data_sim ={}
  for snap_id, n_file in enumerate(file_indices):
    
    file_name = input_dir + f'{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    lya_stats = file['lya_statistics']
    power_spectrum = lya_stats['power_spectrum']
    k_vals = power_spectrum['k_vals'][...]
    ps_mean = power_spectrum['p(k)'][...]
    indices = ps_mean > 0
    k_vals = k_vals[indices]
    ps_mean = ps_mean[indices]
    ps_mean = ps_mean * k_vals / np.pi
    data_sim[snap_id] = { 'z':z, 'k_vals':k_vals, 'ps_mean':ps_mean }
  
  data_all[sim_id] = data_sim



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

ncols, nrows = 2, 2
ax_lenght = 6
fig_width = ncols * ax_lenght
fig_height = nrows * ax_lenght 
h_length = 4*2
main_length = 3*2
full_lenght = h_length + 1

fig = plt.figure(0)
fig.set_size_inches(fig_width, fig_height )
fig.clf()

gs = plt.GridSpec(full_lenght*nrows, ncols)
gs.update(hspace=0., wspace=0.18, )


for i in range(nrows):
  for j in range(ncols):
     
    fig_id = i*ncols + j
    
    data_sim_0 = data_all[0][fig_id]
    z = data_sim_0['z']
    k_vals_0 = data_sim_0['k_vals']
    ps_mean_0 = data_sim_0['ps_mean']
    
    data_sim_1 = data_all[1][fig_id]
    k_vals_1 = data_sim_1['k_vals']
    ps_mean_1 = data_sim_1['ps_mean']
     
    diff = ( ps_mean_1 - ps_mean_0 ) / ps_mean_0  
 
    ax1 = plt.subplot(gs[i*full_lenght:i*full_lenght+main_length, j])
    ax2 = plt.subplot(gs[i*full_lenght+main_length:i*full_lenght+h_length, j])
    
    ax1.plot( k_vals, ps_mean_0, c='C0', ls='-',  label='Grackle' )
    ax1.plot( k_vals, ps_mean_1, c='C1', ls='--', label='Cholla' )
    
    ax1.text(0.9, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax1.transAxes, fontsize=figure_text_size, color=text_color) 

    
    ax1.set_xscale('log') 
    ax1.set_yscale('log') 
    # ax1.set_xlim( xmin, xmax )
    ax1.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
    ax1.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
    ax1.tick_params(axis='x', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=0, size=tick_size_major, width=tick_width_major  )
    
    ax1.legend( frameon=False, loc=3 )    
    ax1.set_ylabel( r'$P\, (k)$', fontsize=label_size )


    ax2.axhline( y=0, c='C0')
    ax2.plot( k_vals, diff, ls='--', c='C1', label='Cholla' )
    ax2.set_ylim( -0.1, 0.1 )
    ax2.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
    ax2.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
    ax2.set_ylabel( r'$\Delta P\,(k) / P\, (k)$', fontsize=label_size )
    ax2.set_xlabel( r'$k \,\, [\mathrm{s \, km^{-1}}]$', fontsize=label_size )
    ax2.set_xscale('log') 

figure_name = output_dir + f'ps_comparison.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


