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
output_dir = proj_dir + 'figures/pk_density_ceil/'
create_directory( output_dir )

n_points = 1024
L_Mpc = 25
sim_base_name = f'{n_points}_{L_Mpc}Mpc_cdm/cic/'
sim_dir = base_dir + sim_base_name
input_dir = sim_dir + 'power_spectrum_files/'

n_snap = 6

file_name = input_dir + f'power_spectrum_particles_{n_snap}.pkl'
pk_data_dm = Load_Pickle_Directory( file_name )
z = pk_data_dm['z']
k_vals_dm = pk_data_dm['k_vals']
pk_dm = pk_data_dm['power_spectrum']


file_name = input_dir + f'power_spectrum_hydro_{n_snap}.pkl'
pk_data_hydro = Load_Pickle_Directory( file_name )
z = pk_data_hydro['z']
k_vals_hydro = pk_data_hydro['k_vals']
pk_hydro = pk_data_hydro['power_spectrum']




# delta_max_vals = np.array([ 1, 10, 100, 500, 1000, 5000, 10000, 50000, 100000, 200000 ])
delta_max_vals = np.array([ 1000, 5000, 10000, 50000, 100000 ])
input_dir = sim_dir + 'power_spectrum_files_density_ceil/'

pk_data_ceil = {}
for data_id, delta_max in enumerate( delta_max_vals ):
  file_name = input_dir + f'power_spectrum_hydro_{n_snap}_dens_max_{delta_max}.pkl'
  pk_data = Load_Pickle_Directory( file_name )
  pk_data_ceil[data_id] = pk_data
  





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


ncols, nrows = 1, 1
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6*ncols,6*nrows))


colors = [ 'C0', 'C2', 'C3', 'C4', 'C5', 'C6' ]

for data_id, delta_max in enumerate( delta_max_vals ):
  k  = pk_data_ceil[data_id]['k_vals']
  pk = pk_data_ceil[data_id]['power_spectrum']
  label = r'$\Delta_\mathrm{max}$' + f' = {delta_max}'
  ax.plot( k, pk, label=label )
  

  
ax.plot( k_vals_hydro, pk_hydro, '--', c='gray', label='Gas')
ax.plot( k_vals_dm, pk_dm, '--', c='k', label='Dark Matter')


ax.text(0.89, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=font_size, color=text_color) 


ax.legend( loc=3, fontsize=14, frameon=False )
ax.set_xscale('log')
ax.set_yscale('log')

ax.set_ylabel( r'$P(k) $', fontsize=font_size, color=text_color  )
ax.set_xlabel( r'$k$  [$h$ Mpc$^{\mathrm{\mathregular{-1}}}$]', fontsize=font_size, color=text_color )

ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )  

figure_name = output_dir + f'ps_{n_points}_{L_Mpc}Mpc_density_ceil.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
