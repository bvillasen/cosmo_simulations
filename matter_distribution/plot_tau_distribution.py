import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import load_snapshot_data_distributed


wdm_masses = [ 0.25, 0.5, 1.0, 2.0, 3.0 ]

input_dir  = data_dir + f'cosmo_sims/rescaled_P19/wdm/tau_distribution_files/'
output_dir = data_dir + f'cosmo_sims/rescaled_P19/wdm/figures_wdm_new/'
create_directory( output_dir )

snap_ids = [25, 35, 45, 55 ]

colors = [ 'C0', 'C1', 'C2', 'C3', 'C4', 'C6']


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
legend_font_size = 14

ncols, nrows = 2, 2
figure_width = 6
figure_height = 12
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*figure_width,figure_height))
plt.subplots_adjust( hspace = 0.15, wspace=0.2)

wdm_masses = [ 0.25, 0.5, 1.0, 2.0, 3.0 ]

pos_label_y = [ 0.95, 0.95, 0.95, 0.95 ]
pos_label_x = [ 0.5, 0.5, 0.5, 0.5 ]

dist_max = [ 0.055, 0.12, 0.4, 0.6 ]

x_max = [ 6, 6, 2, 2]

sim_names = [ ]
for wdm_mass in wdm_masses:
  sim_names.append( f'wdm_m{wdm_mass}kev' )
sim_names.append('cdm')

key = 'tau'



for i in range(nrows):
  for j in range(ncols):
    fig_id = j + i*ncols
    
    if fig_id >=5: continue
    
    snap_id = snap_ids[fig_id]
    ax = ax_l[i][j]
    
    for sim_id,sim_name in enumerate(sim_names):
      file_name = input_dir + f'tau_distribution_{sim_name}.pkl'
      sim_data = Load_Pickle_Directory( file_name )

      snap_data = sim_data[snap_id]
      z = snap_data['z']
      bin_centers = snap_data[key]['bin_centers']
      hist = snap_data[key]['distribution']
      # bin_centers = snap_data['bin_centers']
      
      F_mean = snap_data['flux']['mean']
      tau_eff = -np.log( F_mean )
      
      
      distribution = hist / hist.sum()
      cum_dist = hist.cumsum() / hist.sum()
      
      # cum_dist = np.concatenate( ( [0], cum_dist ))
      # bin_centers = np.concatenate( ( [0], bin_centers ))
      
      

      if sim_name == 'cdm': label = 'CDM'
      else:
        wdm_mass = wdm_masses[sim_id]
        label = f'WDM {wdm_mass} keV'
        
      color = colors[sim_id]
      ax.plot( bin_centers, distribution, label=label, c=color )
      # ax.plot( bin_centers, cum_dist, label=label, c=color )
      
      x = [ tau_eff, tau_eff]
      y = [ 0, dist_max[fig_id] ]   
      ax.plot( x, y, '--', c=color, alpha=0.5 )

    ax.text( 0.9, 0.5, r'$z=${0:.1f}'.format(np.round(z)), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 

    leg = ax.legend(  loc=0, frameon=False, fontsize=legend_font_size    )

    # 
    ax.set_xlim( 0.15, x_max[fig_id] )
    ax.set_ylim( 0, dist_max[fig_id] )

    # ax.set_ylim( 10**-8, 1 )
    # ax.set_yscale('log')

    ax.set_ylabel( r' $f\,(\tau)$', fontsize=label_size, color= text_color )
    ax.set_xlabel( r'$ \tau$', fontsize=label_size, color= text_color )

    ax.set_xscale('log')

    ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')





figure_name = output_dir + 'tau_distribution.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )

