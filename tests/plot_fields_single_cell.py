import os, sys
from os import listdir
from os.path import isfile, join
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from load_data import load_snapshot_data_distributed
from tools import *

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

input_dir_0 = data_dir + 'cosmo_sims/chemistry_test/output_files_grackle/'
input_dir_1 = data_dir + 'cosmo_sims/chemistry_test/output_files/'
output_dir  = data_dir + 'cosmo_sims/chemistry_test/figures/'
create_directory( output_dir ) 

input_dirs = [ input_dir_0, input_dir_1 ]

M_sun = 1.989e+30
MP = 1.6726219e-27
kpc = 3.086e+19 
h = 0.6766

n_snaps = 170
precision = np.float64
Lbox = 50000.0    #kpc/h
n_cells = 64
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
fields = [ 'density', 'temperature', 'HI_density', 'HII_density', 'HeI_density', 'HeII_density', 'HeIII_density', 'e_density' ]
# fields = [ 'temperature' ]

x_H  = 0.75984603480 + 1.53965115054e-4
x_He = 0.23999999997 


data_all = {}
for sim_id,input_dir in enumerate(input_dirs):
  data_sim = {} 
  for n_snapshot in range(n_snaps):
    data = load_snapshot_data_distributed( 'hydro', fields, n_snapshot, input_dir, box_size, grid_size,  precision, show_progess=False )
    z = data['Current_z']          
    if 'z_vals' not in data_sim: data_sim['z_vals'] = []
    data_sim['z_vals'].append(z)
    
    dens = data['density'][0,0,0]
    H_dens  = x_H * dens
    He_dens = x_He * dens
    HI_dens = data['HI_density'][0,0,0]
    HII_dens = data['HII_density'][0,0,0]
    HeI_dens = data['HeI_density'][0,0,0]
    HeII_dens = data['HeII_density'][0,0,0]
    HeIII_dens = data['HeIII_density'][0,0,0]
    x_HI = HI_dens / H_dens
    x_HII = HII_dens / H_dens
    x_HeI = HeI_dens / He_dens
    x_HeII = HeII_dens / He_dens
    x_HeIII = HeIII_dens / He_dens
    if 'x_HI' not in data_sim: data_sim['x_HI'] = []
    if 'x_HII' not in data_sim: data_sim['x_HII'] = []
    if 'x_HeI' not in data_sim: data_sim['x_HeI'] = []
    if 'x_HeII' not in data_sim: data_sim['x_HeII'] = []
    if 'x_HeIII' not in data_sim: data_sim['x_HeIII'] = []
    data_sim['x_HI'].append( x_HI )
    data_sim['x_HII'].append( x_HII )
    data_sim['x_HeI'].append( x_HeI )
    data_sim['x_HeII'].append( x_HeII )
    data_sim['x_HeIII'].append( x_HeIII )
    
    for field in fields:
      field_vals = data[field]
      val_min, val_max = field_vals.min(), field_vals.max()
      if np.abs(val_max - val_min) > 1e-12: print( f'WARNING: Large difference in field {field}:  min:{val_min}  max:{val_max} ')
      if field not in data_sim: data_sim[field] = []
      if field == 'e_density':
        val_min *= M_sun / (kpc**3) / MP * h * h
      data_sim[field].append( val_min )
    
  for key in data_sim:
    data_sim[key] = np.array(data_sim[key])

  data_all[sim_id] = data_sim



labels = [ 'Grackle', 'Cholla' ]

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

fields_to_plot = [ 'temperature', 'x_HI', 'x_HII', 'x_HeI', 'x_HeII', 'x_HeIII', 'e_density' ]

ncols, nrows = 2, 7
ax_lenght = 6
figure_width = ncols * ax_lenght
figure_height = nrows * ax_lenght / 2
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width,figure_height))
plt.subplots_adjust( hspace = 0.15, wspace=0.2)


ax_labels_0 = [ r'$T \,\,\, [\mathrm{K}]$ ', r'$x_\mathrm{HI}$', r'$x_\mathrm{HII}$', r'$x_\mathrm{HeI}$', r'$x_\mathrm{HeII}$',  r'$x_\mathrm{HeIII}$', r'$n_\mathrm{e} \,\,\, [\mathrm{m^{-3}}]$' ]
ax_labels_1 = [ r'$\Delta T / T$', r'$\Delta x_\mathrm{HI} / x_\mathrm{HI}$', r'$ \Delta x_\mathrm{HII} / x_\mathrm{HII}$', r'$\Delta x_\mathrm{HeI} / x_\mathrm{HeI}$', r'$ \Delta x_\mathrm{HeII} / x_\mathrm{HeII} $',  r'$\Delta x_\mathrm{HeIII} / x_\mathrm{HeIII}$', r'$\Delta n_\mathrm{e} / n_\mathrm{e}$' ]

xmin, xmax = 2, 12

for field_id, field in enumerate(fields_to_plot):

  z = data_all[0]['z_vals']  
  field_0 = data_all[0][field]
  field_1 = data_all[1][field]
  diff = ( field_1 - field_0 ) / field_0

  ax = ax_l[field_id][0]
  ax.plot( z, field_0, ls='-',  label=labels[0] )
  ax.plot( z, field_1, ls='--', label=labels[1] )
  ax.set_xlim( xmin, xmax )
  ax.legend( frameon=False, fontsize=legend_font_size )
  ax.set_ylabel( ax_labels_0[field_id], fontsize=label_size )
  if field_id == nrows-1: ax.set_xlabel( r'$z$', fontsize=label_size )
  

  ax = ax_l[field_id][1]
  ax.axhline( y=0, c='C0')
  ax.plot( z, diff, ls='--', c='C1'  )
  ax.set_ylim( -0.2, 0.2 )
  ax.set_xlim( xmin, xmax )
  ax.set_ylabel( ax_labels_1[field_id], fontsize=label_size )
  if field_id == nrows-1: ax.set_xlabel( r'$z$', fontsize=label_size )


figure_name = output_dir + 'single_cell_comparison.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )

