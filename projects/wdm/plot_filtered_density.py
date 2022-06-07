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
cut_id = 46
# for cut_id in range(50):
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
plt.subplots_adjust( hspace = 0.1, wspace=0.02)
  
ax0, ax1, ax2, ax3 = ax_l

dx = 25/1025
ax0.plot( pk_dm['k_vals'], pk_dm['power_spectrum']   * pk_dm['k_vals']**3  * dx**6, label='DM', zorder=2)
ax0.plot( pk_gas['k_vals'], pk_gas['power_spectrum'] * pk_gas['k_vals']**3 * dx**6, label='Gas', zorder=2 )
ax0.fill_between( [k_cut, 1000], [1e50, 1e50], [0, 0], color='gray', alpha=0.4, zorder=1)
ax0.set_xlim( 0.2, 250 )
ax0.set_ylim( 0.7, 9e3 )
ax0.legend( loc=2, frameon=False, fontsize=label_size )
ax0.set_ylabel( r'$k^3 \, P(k) $', fontsize=font_size, color=text_color  )
ax0.set_xlabel( r'$k$  [$h$ Mpc$^{\mathrm{\mathregular{-1}}}$]', fontsize=font_size, color=text_color )
ax0.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax0.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )  
ax0.set_xscale( 'log')
ax0.set_yscale( 'log')


cmap = 'inferno'
vmax = max( proj_dm.max(), proj_gas.max() ) 
vmin = min( proj_dm.min(), proj_gas.min() )
im = ax1.imshow( proj_dm, vmin=vmin, vmax=vmax, cmap=cmap )
cbar = plt.colorbar(im, ax=ax1)
cbar.set_label( r'$  \log_{10} \, \Delta_\mathrm{DM} $', fontsize=label_size )

im = ax2.imshow( proj_gas, vmin=vmin, vmax=vmax, cmap=cmap )
cbar = plt.colorbar(im, ax=ax2)
cbar.set_label( r'$ \log_{10} \, \Delta_\mathrm{gas} $', fontsize=label_size )


ax1.set_title( 'DM overdensity', fontsize=font_size )
ax2.set_title( 'Gas overdensity', fontsize=font_size )
ax1.set_xticks([])
ax1.set_yticks([])
ax2.set_xticks([])
ax2.set_yticks([])

delta = 0.4
ratio = dens_gas / dens_dm - 1
proj_ratio = ratio.sum( axis=0 ) / nz  
im = ax3.imshow( proj_ratio, vmin=-delta, vmax=delta, cmap='coolwarm' )
cbar = plt.colorbar(im, ax=ax3)
cbar.set_label( r'$\Delta_\mathrm{gas} / \Delta_\mathrm{DM} - 1$', fontsize=label_size )
ax3.set_xticks([])
ax3.set_yticks([])


figure_name = output_dir + f'filtered_density_{snap_id}_{cut_id}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
