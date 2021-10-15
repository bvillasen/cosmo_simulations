import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
import pylab
import palettable
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from colors import *


base_dir = data_dir + 'cosmo_sims/rescaled_P19/'
output_dir = data_dir + 'cosmo_sims/figures/paper_thermal_history/'
create_directory( output_dir )

file_name = root_dir + 'lya_statistics/data/FPS_resolution_correction_1024_50Mpc.pkl'
ps_diff_data = Load_Pickle_Directory(  file_name )
ps_diff_z_vals = ps_diff_data['z_vals']

files_to_load = [ 25, 35, 45, 55 ][::-1]

sim_name = '1024_50Mpc'

sim_names = ['512_50Mpc', '1024_50Mpc', '2048_50Mpc', ]

colors = [  ocean_green, orange, dark_blue ]

linestyles = ['--', '--', '-']
linewidths = [ 2, 2, 2.5]

id_0 = 2

n_sims = len( sim_names )

data_all = {}
for sim_id, sim_name in enumerate(sim_names): 
  name_vals, extra = sim_name.split('Mpc')
  n_cells, Lbox_Mpc = name_vals.split('_')
  n_cells = int( n_cells )
  Lbox_Mpc = int( Lbox_Mpc )
  
  data_all[sim_id] = { 'n_cells': n_cells, 'Lbox_Mpc': Lbox_Mpc }
  input_dir = base_dir + f'{sim_name}/analysis_files/'
  data_sim = {}
  for z_id, n_file in enumerate( files_to_load ):
    file_name = input_dir + f'{n_file}_analysis.h5'
    print( f'Loading File: {file_name}' )
    file = h5.File( file_name )
    Lbox = file.attrs['Lbox']
    current_z = file.attrs['current_z'][0]
    ps_mean = file['lya_statistics']['power_spectrum']['p(k)'][...]
    k_vals  = file['lya_statistics']['power_spectrum']['k_vals'][...]
    indices = ps_mean > 0
    ps_mean = ps_mean[indices]
    k_vals  = k_vals[indices]
    
    if sim_id == 1:
      z_diff = np.abs( ps_diff_z_vals - current_z )
      if z_diff.min() > 0.1: 
        print( 'ERROR: Large z difference')
        exit(-1)
      z_indx = np.where( z_diff == z_diff.min() )[0][0]
      ps_diff = ps_diff_data[z_indx]
      diff_k_vals = ps_diff['k_vals']
      diff_ps_factor = ps_diff['delta_factor'] 
      k_diff = np.abs(k_vals - diff_k_vals)
      if k_diff.sum() > 1e-6:
        print( 'ERROR: Large k_vals difference')
        exit(-1)
      # ps_mean = ps_mean / diff_ps_factor
      
    ps_mean = ps_mean[:-1]
    k_vals = k_vals[:-1]
    
    
    
    data_sim[z_id] = { 'z':current_z, 'k_vals':k_vals, 'ps_mean':ps_mean }
  data_all[sim_id]['data_ps'] = data_sim


import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"


fig_dpi = 300
fig_width = 8

l_fig_data = 8
l_fig_error = 3
l_sep = 2

label_size = 12

n_rows, n_cols = 2, 2

group_length = l_fig_data + l_fig_error + l_sep
h_length = n_rows*( l_fig_data + l_fig_error ) + n_cols*l_sep


tick_label_size_major = 11
tick_label_size_minor = 10
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.3
tick_width_minor = 1
figure_text_size = 14

fig = plt.figure(0)
fig.set_size_inches(10, 10)
fig.clf()

gs = plt.GridSpec(h_length, n_cols)
gs.update(hspace=0.0, wspace=0.25, )

kmin, kmax = 1e-3, 8e-1

for i in range( n_rows ):
  for j in range( n_cols ):
    
    
    fig_id = i * n_cols + j
    
    h_start = i*(group_length)
    ax1 = plt.subplot(gs[h_start:h_start+l_fig_data, j])
    h_start += l_fig_data
    ax2 = plt.subplot(gs[h_start:h_start+l_fig_error, j])
    h_start += l_fig_error
    ax3 = plt.subplot(gs[h_start:h_start+l_sep, j])
    for sim_id in range(n_sims):
      sim_name = sim_names[sim_id]
      sim_data = data_all[sim_id]
      
      data_ps = sim_data['data_ps'][fig_id]
      z = data_ps['z']
      k_vals  = data_ps['k_vals']
      ps_mean = data_ps['ps_mean']
      delta_ps = ps_mean * k_vals / np.pi
      
      color = colors[sim_id]
      zorder = 3-sim_id
      ls = linestyles[sim_id]
      lw = linewidths[0]
      
      L = sim_data['Lbox_Mpc']
      n_cells = sim_data['n_cells']
      dx = L * 1e3 / n_cells
      label = r'$\Delta x \,=\, {0:.1f}$'.format( dx ) +'  $h^{-1}\mathrm{kpc}$' 
      
      ax1.plot( k_vals, delta_ps, c=color, zorder=zorder, ls=ls, lw=lw, label = label )
    
      
    ps_data_0 = data_all[id_0]['data_ps'][fig_id]
    ps_mean_0 = ps_data_0['ps_mean']
    k_vals_0 = ps_data_0['k_vals']
    
    
    sim_id = id_0
    color = colors[sim_id]
    zorder = 3-sim_id
    ls = linestyles[sim_id]
    lw = linewidths[sim_id]
    ax2.plot( k_vals_0, np.zeros_like(k_vals_0), c=color, zorder=zorder, ls=ls, lw=lw  )
     
    for sim_id in range(n_sims):
      if sim_id == id_0: continue
      
      sim_data = data_all[sim_id]
      data_ps = sim_data['data_ps'][fig_id]
      z = data_ps['z']
      k_vals  = data_ps['k_vals']
      ps_mean = data_ps['ps_mean']
        
      n_kvals = len( k_vals )
      ps_diff = ( ps_mean - ps_mean_0[:n_kvals] ) / ps_mean_0[:n_kvals] 
      
      color = colors[sim_id]
      zorder = 3-sim_id
      ls = linestyles[sim_id]
      lw = linewidths[sim_id]
      ax2.plot( k_vals, ps_diff,  c=color, zorder=zorder, ls=ls, lw=lw  )  
      print ( f'z={z}, diff:{ps_diff}')
    
      
    
    
    ax1.text(0.88, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax1.transAxes, fontsize=figure_text_size) 
    
    ax1.legend( loc=3,  frameon=False,  fontsize=11)
      
    delta_max = 0.5
    kmin = k_vals.min()
    # if i == 0: 
    #   ps_min, ps_max = 1e-7, 5e-2
    #   ax1.set_ylim( ps_min, ps_max )
    ax1.set_xlim( kmin, kmax )  
    ax2.set_xlim( kmin, kmax )  
    ax2.set_ylim( -delta_max, delta_max )  
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax2.set_xscale('log')
    ax1.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax1.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
    ax1.tick_params(axis='y', which='minor', labelsize=0, size=0, width=0, direction='in' )
    ax2.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
    ax2.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
    ax3.axis('off')
    ax1.set_xticklabels([])
    ax1.set_ylabel( r'$\pi^{\mathregular{-1}} \,k \,P\,(k)$', fontsize=label_size )
    ax2.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size )
    ax2.set_ylabel( r'$\Delta P\,(k) / P\,(k)$ ', fontsize=label_size )
    


fig.align_ylabels()

file_name = output_dir + 'power_spectrum_resolution.png'
fig.savefig( file_name,  pad_inches=0.1,  bbox_inches='tight', dpi=fig_dpi)
print('Saved Image: ', file_name)
