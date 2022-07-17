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
from figure_functions import *
from data_optical_depth import *
from colors import * 
from stats_functions import compute_distribution, get_highest_probability_interval
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid
from load_tabulated_data import load_data_boera
from matrix_functions import Merge_Matrices


proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + 'figures/power_spectrum_delta_max/'
create_directory( output_dir )

sim_dir = data_dir + 'cosmo_sims/1024_25Mpc_fragmentation/cdm/'
input_dir = sim_dir + 'power_spectrum_files/'

snap_ids = [ 6, 7, 8 ]
data_names = [ '', '_delta_max_1000' ]
data_ps_all = {}
for data_id, data_name in enumerate( data_names ):
  data_ps_all[data_id] = {}
  for snap_id, n_snap in enumerate(snap_ids):
    file_name = input_dir + f'power_spectrum_hydro_{n_snap}{data_name}.pkl'
    data = Load_Pickle_Directory( file_name )
    data_ps_all[data_id][snap_id] = data

input_dir = sim_dir + 'flux_power_spectrum/'

delta_max = 10
snap_ids = [ 25, 29, 33 ]
data_names = [ '', f'_delta_max_{delta_max}' ]
data_fps_all = {}
for data_id, data_name in enumerate( data_names ):
  data_fps_all[data_id] = {}
  for snap_id, n_snap in enumerate(snap_ids):
    file_name = input_dir + f'flux_ps_{n_snap:03}{data_name}.h5'
    file = h5.File( file_name, 'r' )
    k_vals = file['k_vals'][...]
    ps = file['ps_mean'][...]
    ps *= k_vals / np.pi
    file.close()
    data_fps_all[data_id][snap_id] = { 'k_vals': k_vals, 'power_spectrum':ps }

import matplotlib
import matplotlib.font_manager
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

fig_width = 3 * figure_width
fig_height = 1.* figure_width
nrows = 2
ncols = 2
h_length = 4
main_length = 3

label_size = 18
figure_text_size = 18
legend_font_size = 13
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 6
tick_size_minor = 4
tick_width_major = 2
tick_width_minor = 1.5
border_width = 1.5
text_color = 'black'
linewidth = 2
bars_alpha = [ 0.7, 0.5 ]

z_vals  = [ 5.0, 4.6, 4.2 ]
for snap_id in range(3):
  
  
  fig = plt.figure(0)
  fig.set_size_inches(fig_width, fig_height )
  fig.clf()
  
  gs = plt.GridSpec(h_length, ncols)
  gs.update(hspace=0.0, wspace=0.18, )
  
  z = z_vals[snap_id]
  for i in range( ncols ):

    ax1 = plt.subplot(gs[0:main_length, i])
    ax2 = plt.subplot(gs[main_length:h_length, i])

    if i == 0: data_all = data_ps_all
    if i == 1: data_all = data_fps_all

    data_0 = data_all[0][snap_id]
    data_1 = data_all[1][snap_id]

    k_0 = data_0['k_vals']
    k_1 = data_1['k_vals']
    ps_0 = data_0['power_spectrum']
    ps_1 = data_1['power_spectrum']  
    diff = ps_1 / ps_0 - 1

    ax1.plot( k_0, ps_0 )
    ax1.plot( k_0, ps_1 )

    ax2.axhline( y=0, ls='--', c='C3')
    ax2.plot( k_0, diff, c="C1" )

    ax1.text(0.89, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax1.transAxes, fontsize=figure_text_size, color=text_color) 

    if i == 0: ax1.set_ylabel( r'$P_\mathrm{gas}(k)$', fontsize=label_size, color= text_color )  
    if i == 1: ax1.set_ylabel( r'$\pi^{\mathregular{-1}} \,k \,P_\mathrm{flux}(k)$', fontsize=label_size, color= text_color )  
    ax1.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax1.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    [sp.set_linewidth(border_width) for sp in ax1.spines.values()]


    ax2.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax2.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
    ax2.set_ylabel( r'$ \Delta P\,(k) / P\,(k)$', fontsize=label_size, color= text_color )  
    ax2.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size, color=text_color )
    ax2.set_xscale('log')
    [sp.set_linewidth(border_width) for sp in ax2.spines.values()]


  # figure_name = output_dir + f'flux_ps_wdm.png'
  figure_name = output_dir + f'ps_{snap_id}_delta_max_{delta_max}.png'
  fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
  print( f'Saved Figure: {figure_name}' )

