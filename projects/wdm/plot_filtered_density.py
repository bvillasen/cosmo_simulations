import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
sys.path.append( cosmo_dir + 'lya_statistics/data' )
from tools import *
from colors import * 
from figure_functions import *

sim_dir  = data_dir + 'cosmo_sims/wdm_sims/tsc/1024_25Mpc_cdm/cic/'
proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + 'figures/filtered_density/'
create_directory( output_dir )

snap_id = 5

input_dir = sim_dir + 'power_spectrum_files/'
file_name_dm  = input_dir + f'power_spectrum_particles_{snap_id}.pkl'
file_name_gas = input_dir + f'power_spectrum_hydro_{snap_id}.pkl'
pk_dm  = Load_Pickle_Directory( file_name_dm )
pk_gas = Load_Pickle_Directory( file_name_gas )


slice_depth = 256
cut_id = 40
input_dir = sim_dir + 'density_slices/'
file_name = input_dir + f'filtered_density_{snap_id}_{cut_id}_{slice_depth}.h5'
print( f'Loading File: {file_name}' )
file = h5.File( file_name, 'r' )
z = file.attrs['z']
k_cut = file.attrs['k_cut']
dens_dm  = file['dm'][...]   
dens_gas = file['gas'][...] 
dens_dm /= dens_dm.mean()
dens_gas /= dens_gas.mean()
file.close()
nz, ny, nx = dens_dm.shape 

proj_dm  = np.log10( dens_dm.sum(axis=0)  / nz )
proj_gas = np.log10( dens_gas.sum(axis=0) / nz )


nrows = 1
ncols = 4

tick_size_major, tick_size_minor = 6, 4
tick_label_size_major, tick_label_size_minor = 14, 12
tick_width_major, tick_width_minor = 1.5, 1

font_size = 18
label_size = 16
bar_alpha = 0.5
border_width = 1.5
text_color  = 'black'


fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
ax0, ax1, ax2, ax3 = ax_l

ax0.plot( pk_dm['k_vals'], pk_dm['power_spectrum']   * pk_dm['k_vals']**3)
ax0.plot( pk_gas['k_vals'], pk_gas['power_spectrum'] * pk_gas['k_vals']**3 )
ax0.set_ylabel( r'$k^3 \, P(k) $', fontsize=font_size, color=text_color  )
ax0.set_xlabel( r'$k$  [$h$ Mpc$^{\mathrm{\mathregular{-1}}}$]', fontsize=font_size, color=text_color )
ax0.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax0.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )  
ax0.set_xscale( 'log')
ax0.set_yscale( 'log')

ax1.imshow( proj_dm )


ax2.imshow( proj_gas )

figure_name = output_dir + f'filtered_density_{snap_id}_{cut_id}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
