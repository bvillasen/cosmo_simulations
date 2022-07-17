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
output_dir = proj_dir + 'figures/power_spectrum_HI_density/'
create_directory( output_dir )

for snap_id in [ 6, 7, 8 ]: 

  sim_dir = data_dir + 'cosmo_sims/wdm_sims/new/1024_25Mpc_cdm/'
  input_dir = sim_dir + 'power_spectrum_files/'

  file_name = input_dir + f'ps_HI_density_{snap_id}.pkl'
  data_HI_cdm = Load_Pickle_Directory( file_name )

  file_name = input_dir + f'ps_dm_density_{snap_id}.pkl'
  data_dm_cdm = Load_Pickle_Directory( file_name )

  
  sim_dir = data_dir + 'cosmo_sims/wdm_sims/new/1024_25Mpc_m4.0kev/'
  input_dir = sim_dir + 'power_spectrum_files/'

  file_name = input_dir + f'ps_HI_density_{snap_id}.pkl'
  data_HI_wdm = Load_Pickle_Directory( file_name )

  file_name = input_dir + f'ps_dm_density_{snap_id}.pkl'
  data_dm_wdm = Load_Pickle_Directory( file_name )


  import matplotlib
  import matplotlib.font_manager
  matplotlib.rcParams['mathtext.fontset'] = 'cm'
  matplotlib.rcParams['mathtext.rm'] = 'serif'

  nrows = 2
  ncols = 1
  fig_width = ncols * figure_width
  fig_height = 1.* figure_width
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


  fig = plt.figure(0)
  fig.set_size_inches(fig_width, fig_height )
  fig.clf()

  gs = plt.GridSpec(h_length, ncols)
  gs.update(hspace=0.0, wspace=0.18, )


  # z = z_vals[snap_id]
  for i in range( ncols ):

    ax1 = plt.subplot(gs[0:main_length, i])
    ax2 = plt.subplot(gs[main_length:h_length, i])

    z = data_dm_cdm['z']
    k_0 = data_HI_cdm['k_vals']
    k_1 = data_dm_cdm['k_vals']
    ps_HI_cdm = data_HI_cdm['power_spectrum']
    ps_dm_cdm = data_dm_cdm['power_spectrum']
    ps_HI_wdm = data_HI_wdm['power_spectrum']
    ps_dm_wdm = data_dm_wdm['power_spectrum']
    
    diff = ps_HI_wdm / ps_HI_cdm 

    ax1.plot( k_0, ps_dm_cdm, c='C0', label='DM CDM' )
    ax1.plot( k_0, ps_HI_cdm, c='C1', label='HI CDM' )
    ax1.plot( k_0, ps_dm_wdm, c='k', ls='--', label='WDM' )
    ax1.plot( k_0, ps_HI_wdm, c='k', ls='--', label='' )
    ax1.legend( loc=3, frameon=False, fontsize=12)
    
    ax2.axhline( y=1, ls='--', c='C3')
    ax2.plot( k_0, diff, c='k', ls='--' )

    ax1.text(0.89, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax1.transAxes, fontsize=figure_text_size, color=text_color) 

    if i == 0: ax1.set_ylabel( r'$P(k)$', fontsize=label_size, color= text_color )  
    ax1.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax1.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    [sp.set_linewidth(border_width) for sp in ax1.spines.values()]


    ax2.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax2.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
    ax2.set_ylabel( r'$P_\mathrm{HI,WDM}(k) / P_\mathrm{HI,CDM}(k)$', fontsize=label_size, color= text_color )  
    ax2.set_xlabel( r'$k$  [$h \,/ \, \mathrm{Mpc}$]', fontsize=label_size, color=text_color )
    ax2.set_xscale('log')
    [sp.set_linewidth(border_width) for sp in ax2.spines.values()]


  # figure_name = output_dir + f'flux_ps_wdm.png'
  figure_name = output_dir + f'ps_HI_{snap_id}.png'
  fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
  print( f'Saved Figure: {figure_name}' )

