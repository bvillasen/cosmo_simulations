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

base_dir = data_dir + 'cosmo_sims/wdm_sims/tsc/'
proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + 'figures/pk_HM12/'
create_directory( output_dir )

n_points = 1024
sim_base_name = f'{n_points}_25Mpc_cdm'
sim_names = [ '', '_HM12', '_adiabatic'  ]

n_snaps = 7


data_type = 'hydro'
data_hydro = {}
for sim_id, sim_name in enumerate(sim_names):
  data_hydro[sim_id] = {}
  for snap_id in range(n_snaps):
    input_dir = base_dir + f'{sim_base_name}{sim_name}/power_spectrum_files/'
    file_name = input_dir + f'power_spectrum_{data_type}_{snap_id}.pkl'
    data = Load_Pickle_Directory( file_name )
    data_hydro[sim_id][snap_id] = data

data_type = 'particles'
data_particles = {}
for sim_id, sim_name in enumerate(sim_names):
  data_particles[sim_id] = {}
  for snap_id in range(n_snaps):
    input_dir = base_dir + f'{sim_base_name}{sim_name}/power_spectrum_files/'
    file_name = input_dir + f'power_spectrum_{data_type}_{snap_id}.pkl'
    data = Load_Pickle_Directory( file_name )
    data_particles[sim_id][snap_id] = data

  
ref_id = 0  
diff_particles = {}
data = data_particles
for data_id in range(3):
  diff_particles[data_id] = {}
  for z_id in range(n_snaps):
    k_vals = data[data_id][z_id]['k_vals']
    pk_0 = data[ref_id][z_id]['power_spectrum']
    pk_1 = data[data_id][z_id]['power_spectrum']
    pk_diff = ( pk_1 - pk_0 ) / pk_0
    diff_particles[data_id][z_id] = { 'k_vals':k_vals, 'pk_diff':pk_diff }
  
diff_hydro = {}
data = data_hydro
for data_id in range(3):
  diff_hydro[data_id] = {}
  for z_id in range(n_snaps):
    k_vals = data[data_id][z_id]['k_vals']
    pk_0 = data[ref_id][z_id]['power_spectrum']
    pk_1 = data[data_id][z_id]['power_spectrum']
    pk_diff = ( pk_1 - pk_0 ) / pk_0
    print( pk_diff )
    diff_hydro[data_id][z_id] = { 'k_vals':k_vals, 'pk_diff':pk_diff }



import matplotlib
import matplotlib.font_manager
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

fig_width = 2 * figure_width
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


font_size = 16
legend_font_size = 12

label_size = 18
figure_text_size = 18
legend_font_size = 12
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
border_width = 1
text_color = 'k'

fig = plt.figure(0)
fig.set_size_inches(fig_width, fig_height )
fig.clf()

gs = plt.GridSpec(h_length, ncols)
gs.update(hspace=0.0, wspace=0.18, )

for data_id in range(2):
  if data_id == 0: 
    data = data_particles
    diff = diff_particles
  if data_id == 1: 
    data = data_hydro
    diff = diff_hydro
    
  ax1 = plt.subplot(gs[0:main_length, data_id])
  ax2 = plt.subplot(gs[main_length:h_length, data_id])

  ax2.axhline( y=1, ls='--', c='red')

  colors = [ 'C0', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7' ]
  linestyles = [ '-', '--', 'dotted' ]
  for sim_id in range(3):
    for z_id in range(n_snaps):
      id = n_snaps - z_id -1
      z = data[sim_id][id]['z']
      k_0  = data[sim_id][id]['k_vals']
      pk_0 = data[sim_id][id]['power_spectrum']
      label = ''
      if sim_id == 1 and id == 0: label = 'HM12'
      if sim_id == 2 and id == 0: label = 'adiabatic'
      if sim_id == 0: label = r'$z = {0:.0f}$'.format( z )
      c = colors[z_id]
      ax1.plot( k_0, pk_0, label=label, c=c, ls=linestyles[sim_id] )
  
      pk_diff = diff[sim_id][id]['pk_diff'] +1
      ax2.plot( k_0, pk_diff, c=c, ls=linestyles[sim_id] )
  
      
      
  diff_log = False

  ax1.legend( loc=3, fontsize=14, frameon=False )
  ax1.set_xscale('log')
  ax1.set_yscale('log')
  ax2.set_xscale('log')
  if diff_log: ax2.set_yscale('log')

  if data_id==0:ax1.set_ylabel( r'$P_\mathrm{DM}(k) $', fontsize=font_size, color=text_color  )
  if data_id==0:ax2.set_ylabel( r'$P_\mathrm{DM}(k) \, / \, P_\mathrm{DM,CDM}(k)$', fontsize=font_size, color=text_color  )
  if data_id==1:ax1.set_ylabel( r'$P_\mathrm{gas}(k) $', fontsize=font_size, color=text_color  )
  if data_id==1:ax2.set_ylabel( r'$P_\mathrm{gas}(k) \, / \, P_\mathrm{gas,CDM}(k)$', fontsize=font_size, color=text_color  )
  ax2.set_xlabel( r'$k$  [$h$ Mpc$^{\mathrm{\mathregular{-1}}}$]', fontsize=font_size, color=text_color )

  ax1.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax1.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )  
  ax2.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax2.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )

figure_name = output_dir + f'ps_hydro_different_UVB.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )





  
  
  