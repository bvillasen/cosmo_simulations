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
from load_tabulated_data import load_data_boera, load_data_irsic 
from matrix_functions import Normalize_Covariance_Matrix

import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

output_dir = data_dir + 'figures/thermal_history/cov_matrix_data/'
create_directory( output_dir )

ps_data_dir = cosmo_dir + 'lya_statistics/data/'
data_boera_dir = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_data_boera( data_boera_dir )

data_irsic_dir = ps_data_dir + 'data_power_spectrum_irsic_2017/'
data_irsic = load_data_irsic( data_irsic_dir )

print_out = True

data_boss_dir = ps_data_dir + 'data_power_spectrum_boss/'
file_name = data_boss_dir + 'Pk1D_data.dat'
if print_out : print(f'Loading File: {file_name}')
table = np.loadtxt( file_name )
z_vals_all =  np.round(table[:,0], decimals=1 )
z_vals = np.array(list(set(list(z_vals_all))))
z_vals.sort()
data_out = {}
data_out['z_vals'] = z_vals
k_vals_all = None
for i,z in enumerate(z_vals):
  indices = np.where(z_vals_all==z)[0]
  data_z =  table[indices]
  k_vals = data_z[:,1]
  if k_vals_all is None: k_vals_all = k_vals
  k_diff = np.abs( k_vals_all - k_vals ).sum()
  if k_diff > 1e-10:
    print('ERROR: Not the same k_vals for all redshifts')
    exit(-1)
  power = data_z[:,2]
  power_error = data_z[:,3]
  data_out[i] = {}
  data_out[i]['z'] = z
  data_out[i]['k_vals'] = k_vals
  data_out[i]['delta_power'] = power * k_vals / np.pi 
  data_out[i]['delta_power_error'] = power_error * k_vals / np.pi 
  data_out[i]['power_spectrum'] = power  
  data_out[i]['sigma_power_spectrum'] = power_error  
  

# 
# 
# 
# label_size = 16
# figure_text_size = 18
# tick_label_size_major = 15
# tick_label_size_minor = 13
# tick_size_major = 5
# tick_size_minor = 3
# tick_width_major = 1.5
# tick_width_minor = 1
# text_color = 'black'
# legend_font_size = 14
# ax_lenght = 6 
# 
# 
# ncols, nrows = 3, 1
# figure_width, figure_height = ncols * ax_lenght, nrows * ax_lenght
# fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width,figure_height))
# plt.subplots_adjust( hspace = 0.15, wspace=0.2)
# for data_id in data_boera:
#   if data_id in [ 'z_vals', 'full_cov_matrix']: continue
#   ax = ax_l[data_id]
#   data = data_boera[data_id]
#   z = data['z']
#   cov_matrix = data['covariance_matrix']
#   k_vals = data['k_vals']
#   k_min, k_max = np.log10(k_vals.min()), np.log10(k_vals.max())
#   im = ax.imshow( cov_matrix, cmap='turbo', extent=(k_min, k_max, k_max, k_min) )
#   ax.set_aspect('equal')
#   if data_id == 2:
#     cax = ax.inset_axes([1.04, 0.1, 0.05, 0.8], transform=ax.transAxes)
#     fig.colorbar(im, ax=ax, cax=cax)
#   ax.text(0.85, 0.92, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='white') 
#   ax.set_ylabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )
#   ax.set_xlabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )
#   ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
#   ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
#   ax.set_xticks( [ -2, -1.5, -1])
#   ax.set_yticks( [ -2, -1.5, -1])
# 
# figure_name = output_dir + 'covariance_matrix_boera'
# figure_name += '.png'
# fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
# print( f'Saved Figure: {figure_name}' )
