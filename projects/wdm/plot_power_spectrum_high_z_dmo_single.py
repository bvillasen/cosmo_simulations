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

base_dir = data_dir + 'cosmo_sims/wdm_sims/'
proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + 'figures/pk_high_z/'
create_directory( output_dir )

n_points = 2048
L_Mpc = 10
sim_base_name = f'{n_points}_{L_Mpc}Mpc_dmo'
sim_names = [ 'cdm', 'm3.0kev' ]

sim_base_names = [ '1024_25Mpc_dmo', '1024_10Mpc_dmo', '1024_5Mpc_dmo', '2048_10Mpc_dmo', ]
labels = ['N=1024  L=25', 'N=1024  L=10', 'N=1024  L=5', 'N=2048  L=10' ]
dx_vals = [ 25/1024, 10/1024, 5/1024,  10/2048 ]

diff_all = {}
z_id = 0

data_type = 'particles'

for data_id, sim_base_name in enumerate(sim_base_names):
  data_particles = {}
  for sim_id, sim_name in enumerate(sim_names):
    data_particles[sim_id] = {}
    for snap_id in range(6):
      input_dir = base_dir + f'{sim_base_name}_{sim_name}/power_spectrum_files/'
      if data_id == 0: 
        file_name = input_dir + f'power_spectrum_{data_type}.pkl'
        data = Load_Pickle_Directory( file_name )[snap_id]
      else:  
        file_name = input_dir + f'power_spectrum_{data_type}_{snap_id}.pkl'
        data = Load_Pickle_Directory( file_name )
      data_particles[sim_id][snap_id] = data
      
  diff_particles = {}
  data = data_particles
  dx = dx_vals[data_id]
  z_0 = data[0][z_id]['z']
  z_1 = data[1][z_id]['z']
  z_diff = z_0 - z_1
  # print( z_diff )
  k_vals_0 = data[0][z_id]['k_vals']
  k_vals_1 = data[1][z_id]['k_vals']
  k_diff =  k_vals_0 - k_vals_1 
  k_vals = k_vals_0
  pk_0 = data[0][z_id]['power_spectrum'] * dx**6 
  pk_1 = data[1][z_id]['power_spectrum'] * dx**6
  pk_diff = ( pk_1 - pk_0 ) / pk_0
  diff_particles = { 'k_vals':k_vals_0, 'pk_diff':pk_diff, 'pk_0':pk_0, 'pk_1':pk_1 }
  diff_all[data_id] = diff_particles



import matplotlib
import matplotlib.font_manager
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

fig_width = 1 * figure_width
fig_height = 1.* figure_width
nrows = 2
ncols = 1
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

ax1 = plt.subplot(gs[0:main_length, 0])
ax2 = plt.subplot(gs[main_length:h_length, 0])

ax2.axhline( y=1, ls='--', c='red')

colors = [ 'C0', 'C2', 'C3', 'C4', 'C5', 'C6' ]

for i in range(4):
  
  data = diff_all[i]
  k = data['k_vals']
  pk_0 = data['pk_0']
  pk_1 = data['pk_1']
  pk_diff = data['pk_diff']
  label = labels[i]
  c = colors[i]
  
  ax1.plot( k, pk_0, label=label, c=c )
  ax1.plot( k, pk_1, ls='--', c=c )

  diff = pk_1 / pk_0
  ax2.plot( k, diff, c=c )


diff_log =True

ax1.legend( loc=3, fontsize=14, frameon=False )
ax1.set_xscale('log')
ax1.set_yscale('log')
ax2.set_xscale('log')
if diff_log: ax2.set_yscale('log')

ax1.set_ylabel( r'$P_\mathrm{DM}(k) $', fontsize=font_size, color=text_color  )
ax2.set_ylabel( r'$P_\mathrm{DM}(k) \, / \, P_\mathrm{DM,CDM}(k)$', fontsize=font_size, color=text_color  )
ax2.set_xlabel( r'$k$  [$h$ Mpc$^{\mathrm{\mathregular{-1}}}$]', fontsize=font_size, color=text_color )

ax1.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax1.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )  
ax2.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax2.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )

figure_name = output_dir + f'ps_diff_zid_{z_id}.png'
if diff_log: figure_name = output_dir +  f'ps_diff_zid_{z_id}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )

# 
# 
# 
# 
# 
# 
# 