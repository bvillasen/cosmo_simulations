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
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid
from load_tabulated_data import load_data_boera 
from matrix_functions import Normalize_Covariance_Matrix

import matplotlib
matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/fonts/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'


ps_data_dir = cosmo_dir + 'lya_statistics/data/'
data_boera_dir = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_data_boera( data_boera_dir )
data_z_b = data_boera['z_vals']

base_dir = data_dir + 'cosmo_sims/sim_grid/'
output_dir = base_dir + 'figures_wdm/covariance_matrix/'
create_directory( output_dir )


z_vals = [ 4.2, 4.6, 5.0 ]

data_all = {}
for data_id, z in enumerate(z_vals):

  file_name = data_boera_dir + f'Cov_Matrixz={z}.dat'
  print( f'Loading File: {file_name}') 
  file = open( file_name, 'rb' )
  cov_matrix = np.load( file )
  nx, ny = cov_matrix.shape
  diagonal = np.array([ cov_matrix[i,i] for i in range(nx) ])
  data = data_boera[data_id]
  z_ps = data['z']
  k_vals = data['k_vals']
  delta_ps = data['delta_power']
  delta_ps_sigma = data['delta_power_error']
  ps = delta_ps / k_vals * np.pi
  ps_sigma = delta_ps_sigma / k_vals * np.pi
  diff = ( ps_sigma - np.sqrt( diagonal ) ) / np.sqrt( diagonal )
  print( f'data_id: {data_id}  z:{z}  {z_ps}' )
  print( f'Diff min: {diff.min()}  max: {diff.max()} ')
  cov_matrix_norm = Normalize_Covariance_Matrix( cov_matrix )
  data_all[data_id] = { 'z':z, 'cov_matrix':cov_matrix, 'diagonal':diagonal, 'cov_matrix_norm':cov_matrix_norm, 'k_vals':k_vals }


# Merge cov matrices into a single one
n_total = 0  
for data_id in data_all:
  cov_matrix = data_all[data_id]['cov_matrix']
  ny, nx = cov_matrix.shape
  n_total += nx

cov_matrix_merge = np.zeros((n_total, n_total))
cov_matrix_merge_norm = np.zeros((n_total, n_total))
offset = 0
for data_id in data_all:
  cov_matrix = data_all[data_id]['cov_matrix']
  cov_matrix_norm = data_all[data_id]['cov_matrix_norm']
  ny, nx = cov_matrix.shape
  cov_matrix_merge[offset:offset+ny,offset:offset+nx] = cov_matrix
  cov_matrix_merge_norm[offset:offset+ny,offset:offset+nx] = cov_matrix_norm
  offset += ny
  

plot_normalized = False

label_size = 16
figure_text_size = 18
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
text_color = 'black'
legend_font_size = 14

# 
# ncols, nrows = 1, 1
# ax_lenght = 6 
# figure_width, figure_height = ncols * ax_lenght, nrows * ax_lenght
# fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width,figure_height))
# plt.subplots_adjust( hspace = 0.15, wspace=0.2)
# 
# if plot_normalized: cov_matrix_merge = cov_matrix_merge_norm
# inv = np.linalg.inv(cov_matrix_merge)
# 
# ax.imshow( np.log10(inv), cmap='turbo' )
# ax.set_aspect('equal')
# 
# 
# 
# ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
# ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
# 
# 
# figure_name = output_dir + 'covariance_matrix_merge_inv'
# if plot_normalized: figure_name += '_normalized'
# figure_name += '.png'
# fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
# print( f'Saved Figure: {figure_name}' )
# 




ncols, nrows = 3, 1
ax_lenght = 6 
figure_width, figure_height = ncols * ax_lenght, nrows * ax_lenght
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width,figure_height))
plt.subplots_adjust( hspace = 0.15, wspace=0.2)

for data_id in data_all:

  ax = ax_l[data_id]


  data = data_all[data_id]
  z = data['z']
  cov_matrix = data['cov_matrix']
  if plot_normalized: cov_matrix = data['cov_matrix_norm']
  k_vals = data['k_vals']
  k_min, k_max = np.log10(k_vals.min()), np.log10(k_vals.max())
  im = ax.imshow( cov_matrix, cmap='turbo', extent=(k_min, k_max, k_max, k_min) )
  ax.set_aspect('equal')

  if data_id == 2:
    cax = ax.inset_axes([1.04, 0.1, 0.05, 0.8], transform=ax.transAxes)
    fig.colorbar(im, ax=ax, cax=cax)
  
  ax.text(0.85, 0.92, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='white') 

  ax.set_ylabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )
  ax.set_xlabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )


  ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
  ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

  ax.set_xticks( [ -2, -1.5, -1])
  ax.set_yticks( [ -2, -1.5, -1])

figure_name = output_dir + 'covariance_matrix'
if plot_normalized: figure_name += '_normalized'
figure_name += '.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )




# 
# 
