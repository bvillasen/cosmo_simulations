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
from load_data import load_snapshot_data_distributed
from power_spectrum_functions import get_power_spectrum


base_dir = data_dir + 'cosmo_sims/cholla_ics/'
output_dir = base_dir + 'figures/'
create_directory( output_dir ) 

python_dir = base_dir + 'ics_python/'


box_0 = { 'L_kpc':50000, 'n_grid':256 }
box_1 = { 'L_kpc':50000, 'n_grid':128 }
box_2 = { 'L_kpc':200000, 'n_grid':256 }
box_3 = { 'L_kpc':25000, 'n_grid':128 }
boxes = [ box_0, box_1, box_2, box_3 ]

data_python = {}
for data_id, box in enumerate(boxes):
  L_kpc = box['L_kpc']
  Lbox = int( L_kpc / 1e3 )
  n_grid = box['n_grid']
  dx = L_kpc / n_grid
  file_name = python_dir + f'ps_data_{n_grid}_{Lbox}.pkl'
  ps_data = Load_Pickle_Directory( file_name )
  label = f'L={Lbox} Mpc   N={n_grid}'
  ps_data['label'] = label
  # factor = ( 1 / dx ) **3
  factor = 1
  ps_data['ps_dm']  *= factor
  ps_data['ps_gas'] *= factor
  data_python[data_id] = ps_data
  
  

figure_width = 4
text_color = 'black'  
nrows = 1
ncols = 2
fig_height = 1 * figure_width
fig_width = ncols * figure_width
h_length = 4
main_length = 3
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_width, fig_height) )
plt.subplots_adjust( hspace = 0.0, wspace=0.27)


for i in range(2):
  
  if i == 0: ps_key = 'ps_dm'
  if i == 1: ps_key = 'ps_gas'
  
  ax = ax_l[i]

  for data_id in data_python:
    ps_data = data_python[data_id]
    k_vals = ps_data['k_vals']
    ps = ps_data[ps_key]
    label = ps_data['label']
    ax.plot( k_vals, ps, label=label )
     




    
  ax.set_xlabel(r'$k$  [$h\, \mathrm{Mpc^{-1}}$]')
  if i == 0: ax.set_ylabel(r'DM $P(k)$')
  if i == 1: ax.set_ylabel(r'Gas $P(k)$')
    
  ax.set_xscale('log')
  ax.set_yscale('log')

  ax.legend(frameon=False, loc=3, fontsize=8)

  
figure_name  = output_dir + f'ics_power_spectrum_comparison.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )



