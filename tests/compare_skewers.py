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
input_dir_0 = sim_dir + 'skewers_files_grackle/'
input_dir_1 = sim_dir + 'skewers_files_cholla/'
output_dir = sim_dir + 'figures/skewers/'
create_directory( output_dir ) 

input_dirs = [ input_dir_0, input_dir_1 ]

# Box parameters
Lbox = 50000.0 #kpc/h
box = {'Lbox':[ Lbox, Lbox, Lbox ] }

file_indices = [ 25, 35, 45, 55 ]

skewer_indices = np.array([ 100, 1024, 2048, 4096, 6000 ])

axis_list = [ 'x', 'y', 'z' ]
field_list = [ 'HI_density', 'temperature', 'los_velocity' ]

data_all = {}
for sim_id, input_dir in enumerate(input_dirs):

  data_sim = {}
  for snap_id, n_file in enumerate(file_indices):

    skewer_dataset = Load_Skewers_File( n_file, input_dir, axis_list=axis_list, fields_to_load=field_list )

    # Cosmology parameters
    cosmology = {}
    cosmology['H0'] = skewer_dataset['H0']
    cosmology['Omega_M'] = skewer_dataset['Omega_M']
    cosmology['Omega_L'] = skewer_dataset['Omega_L']
    cosmology['current_z'] = skewer_dataset['current_z']
    print( f'z: {cosmology["current_z"]}')
    skewers_data = { field:skewer_dataset[field][skewer_indices] for field in field_list }
    data_Flux = Compute_Skewers_Transmitted_Flux( skewers_data, cosmology, box )
    data_sim[snap_id] = data_Flux
  data_all[sim_id] = data_sim



import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'


label_size = 16
figure_text_size = 14
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
text_color = 'black'
legend_font_size = 11


ncols, nrows = 2, 5
ax_lenght = 6
figure_width = ncols * ax_lenght
figure_height = nrows * ax_lenght / 2


labels = [ 'Grackle', 'Cholla' ]

snap_id = 0
for snap_id in range(len(file_indices)):
  fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width,figure_height))
  plt.subplots_adjust( hspace = 0.15, wspace=0.2)

  data_snap_0 = data_all[0][snap_id]
  vel_Hubble_0   = data_snap_0['vel_Hubble']
  skewers_Flux_0 = data_snap_0['skewers_Flux']

  data_snap_1 = data_all[1][snap_id]
  vel_Hubble_1   = data_snap_1['vel_Hubble']
  skewers_Flux_1 = data_snap_1['skewers_Flux']


  flux_min = 1e-10

  for skewer_id in range(5):
    
    
    ax = ax_l[skewer_id][0]
    flux_0 = skewers_Flux_0[skewer_id]
    flux_1 = skewers_Flux_1[skewer_id]
    
    # flux_0[flux_0<flux_min] = flux_min
    # flux_1[flux_1<flux_min] = flux_min
    diff = ( flux_1 - flux_0 ) 
    diff *= 0.8
    
    xmin, xmax = vel_Hubble_0.min(), vel_Hubble_0.max()
    
    ax.plot( vel_Hubble_0, flux_0, ls='-',  label=labels[0] )
    ax.plot( vel_Hubble_1, flux_1, ls='--', label=labels[1] )
    ax.legend( frameon=False, fontsize=legend_font_size )
    ax.set_ylabel( r'$F_{\mathrm{Ly\alpha}}$', fontsize=label_size )
    if skewer_id == nrows-1: ax.set_xlabel( r'$v \,\, [\mathrm{km/s}]$', fontsize=label_size )
    ax.set_ylim( 0., 1.0 )
    ax.set_xlim( xmin, xmax )
    
    
    ax = ax_l[skewer_id][1]
    ax.axhline( y=0, c='C0')
    ax.plot( vel_Hubble_0, diff, ls='--', c='C1'  )
    ax.set_ylim( -0.05, 0.05 )
    ax.set_xlim( xmin, xmax )
    ax.set_ylabel( r'$\Delta F$' , fontsize=label_size )
    if skewer_id == nrows-1: ax.set_xlabel( r'$v \,\, [\mathrm{km/s}]$', fontsize=label_size )
    

  figure_name = output_dir + f'skewers_comparison_{snap_id}.png'
  fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
  print( f'Saved Figure: {figure_name}' )


