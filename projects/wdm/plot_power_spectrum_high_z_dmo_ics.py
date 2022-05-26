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
output_dir = proj_dir + 'figures/pk_ics/'
create_directory( output_dir )

sim_names = [ 'cdm', 'm_3.0kev' ]
data_type = 'particles'
snap_id = 0

base_input_dir = proj_dir + 'data/input_wdm_power_spectrum_music/'
data_input = {}
for i,sim_name in enumerate(sim_names):
  input_dir = base_input_dir + f'{sim_name}/'
  in_file_name = input_dir + 'input_powerspec.txt'
  data = np.loadtxt( in_file_name )
  k, P_cdm, P_vcdm, P_total = data.T
  data_input[i] = { 'k':k, 'P_cdm':P_cdm, 'P_vcdm':P_vcdm, 'P_total':P_total  }

input_k = data_input[0]['k']
input_cdm = data_input[0]['P_total']
input_wdm = data_input[1]['P_total']
input_ratio = data_input[1]['P_total'] / data_input[0]['P_total']    

sim_names = [ 'cdm', 'm3.0kev' ]

L_Mpc = 25

sim_base_name = f'1024_{L_Mpc}Mpc_dmo'

data_particles = {}
diff_particles = {}

density_types = [ 'cic', 'tsc' ]
for density_type in density_types:

  data_particles[density_type] = {}
  diff_particles[density_type] = {}

  for sim_id, sim_name in enumerate(sim_names):
    input_dir = base_dir + f'{sim_base_name}_{sim_name}/power_spectrum_files/'
    file_name = input_dir + f'power_spectrum_{data_type}_{density_type}_{snap_id}.pkl'
    data = Load_Pickle_Directory( file_name )
    data_particles[density_type][sim_id] = data


  pk_0 = data_particles[density_type][0]['power_spectrum']
  pk_1 = data_particles[density_type][1]['power_spectrum']
  pk_diff = ( pk_1 - pk_0 ) / pk_0
  diff_particles[density_type] = { 'pk_diff':pk_diff }


# sim_base_name = f'2048_{L_Mpc}Mpc_dmo'
# 
# data_particles_2048 = {}
# diff_particles_2048 = {}
# 
# for density_type in density_types:
#   data_particles_2048[density_type] = {}
#   diff_particles_2048[density_type] = {}
# 
#   for sim_id, sim_name in enumerate(sim_names):
#     input_dir = base_dir + f'{sim_base_name}_{sim_name}/power_spectrum_files/'
#     file_name = input_dir + f'power_spectrum_{data_type}_{density_type}_{snap_id}.pkl'
#     data = Load_Pickle_Directory( file_name )
#     data_particles_2048[density_type][sim_id] = data
# 
# 
#   pk_0 = data_particles_2048[density_type][0]['power_spectrum']
#   pk_1 = data_particles_2048[density_type][1]['power_spectrum']
#   pk_diff = ( pk_1 - pk_0 ) / pk_0
#   diff_particles_2048[density_type] = { 'pk_diff':pk_diff }
# 
# 

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
labels = [ f'CIC   1024   L={L_Mpc}Mpc/h', f'TSC  1024   L={L_Mpc}Mpc/h'] 

for i, density_type in enumerate(density_types):

  sim_id = 0
  k_0  = data_particles[density_type][sim_id]['k_vals']
  pk_0 = data_particles[density_type][sim_id]['power_spectrum']
  c = colors[i]
  label = labels[i]
  ax1.plot( k_0, pk_0, label=label, c=c )
  
  sim_id = 1
  k_1  = data_particles[density_type][sim_id]['k_vals']
  pk_1 = data_particles[density_type][sim_id]['power_spectrum']
  c = colors[i]
  ax1.plot( k_1, pk_1, ls='--', c=c )
  diff = pk_1 / pk_0
  ax2.plot( k_0, diff, c=c )

  if i == 1:
    input_factor = 1.2e12
    ax1.plot( input_k, input_cdm*input_factor, label='', ls='dotted', c='k' )
    
    
    ratio_interp = np.interp( k_0, input_k, input_ratio )
    ax1.plot( input_k, input_wdm*input_factor, label='', ls='dotted', c='k' )
    ax2.plot( k_0, ratio_interp, label='', ls='dotted', c='k' )

# labels = [ 'CIC   1024   L=10Mpc/h  2048 particles', 'TSC  1024   L=10Mpc/h  2048 particles'] 
# for i, density_type in enumerate(density_types):
# 
#   sim_id = 0
#   k_0  = data_particles_2048[density_type][sim_id]['k_vals']
#   pk_0 = data_particles_2048[density_type][sim_id]['power_spectrum']
#   c = colors[i+2]
#   label = labels[i]
#   ax1.plot( k_0, pk_0, label=label, c=c )
#   sim_id = 1
#   k_1  = data_particles_2048[density_type][sim_id]['k_vals']
#   pk_1 = data_particles_2048[density_type][sim_id]['power_spectrum']
#   ax1.plot( k_1, pk_1, ls='--', c=c )
#   diff = pk_1 / pk_0
# #   ax2.plot( k_0, diff, c=c )

diff_log =True

xmin, xmax = .1, 300
ymin, ymax = 1e-7, 1e10
ax1.set_xlim(xmin, xmax)
ax2.set_xlim(xmin, xmax)
ax1.set_ylim(ymin, ymax)

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

figure_name = output_dir + f'ps_ics_1024_{L_Mpc}Mpc_dmo_log.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )





  
  
  