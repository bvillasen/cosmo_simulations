import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from cosmology import Cosmology
from load_data import Load_Skewers_File, load_analysis_data
from figure_functions import *
from mpl_toolkits.axes_grid1 import ImageGrid

use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + 'figures/vel_peculiar/'
create_directory( output_dir )

cosmo = Cosmology()


files = [ 25, 29, 33]

n_file = 33
sim_dir  = data_dir + f'cosmo_sims/wdm_sims/compare_wdm/1024_25Mpc_cdm/'
flux_dir = data_dir + f'cosmo_sims/wdm_sims/new/transmitted_flux/'
input_dir  = sim_dir + f'skewers_files/'

axis_list = [ 'x', 'y', 'z' ]
n_skewers_list = [ 'all', 'all', 'all']
skewer_ids_list = [ 'all', 'all', 'all']
field_list = [  'temperature', 'los_velocity',  ]


skewer_dataset = Load_Skewers_File( n_file, input_dir, axis_list=axis_list, fields_to_load=field_list )
z = skewer_dataset['current_z']
temperature = np.log10(skewer_dataset['temperature'].flatten() )
los_velocity = skewer_dataset['los_velocity'].flatten() 

n_points = 200
temp_vals = np.linspace( 3.5, 7, n_points )
vel_vals = np.linspace( -350, 350, n_points) 

# dens_points, vel_points = np.meshgrid( dens_vals, vel_vals )
# vel_points = vel_points.flatten()
# dens_points = dens_points.flatten()

phase, yedges, xedges  = np.histogram2d( temperature, los_velocity, bins=[ temp_vals, vel_vals] )
phase = phase.T
phase = phase.astype(np.float)
phase /= phase.sum()
vel_centers = (xedges[:-1] + xedges[1:])/2
temp_centers = (yedges[:-1] + yedges[1:])/2
# 
# indices = phase > 0
# dens_points, vel_points = np.meshgrid( dens_centers, vel_centers )
# phase = np.log10( phase[indices] )
# vel_points = vel_points[indices]
# dens_points = dens_points[indices]
# phase = phase.flatten()
# vel_points = vel_points.flatten()
# dens_points = dens_points.flatten()

fig_width = 8
fig_dpi = 300
label_size = 18
figure_text_size = 18
legend_font_size = 16
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
border_width = 1

def force_aspect_ratio(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

n_rows, n_cols = 1, 1

colormap = 'turbo'
alpha = 0.6

text_color = 'black'

# Set up figure and image grid
fig = plt.figure( figsize=(fig_width*n_cols,10*n_rows),  )
grid = ImageGrid(fig, 111,          # as in plt.subplot(111)
               nrows_ncols=(n_rows,n_cols),
               axes_pad=0.2,
               share_all=True,
               cbar_location="right",
               cbar_mode="single",
               cbar_size="5%",
               cbar_pad=0.1,
               )

ax = grid[0]

# im = ax.scatter( dens_points, vel_points, c=phase, s=0.5, vmin=-0.5, vmax=3, alpha=alpha, cmap=colormap  )
phase = np.log10( phase )
im = ax.imshow( phase, cmap=colormap, extent=[temp_centers.min(), temp_centers.max(), vel_centers.min(), vel_centers.max(), ], origin='lower' )

cb = ax.cax.colorbar(im,   )
cb.ax.tick_params(labelsize=tick_label_size_major, size=tick_size_major, color=text_color, width=tick_width_major, length=tick_size_major, labelcolor=text_color, direction='in' )
ax.cax.toggle_label(True)
[sp.set_linewidth(border_width) for sp in cb.ax.spines.values()]
cb.set_label( r'$ \log_\mathrm{10} \, PDF( T, \, v_\mathregular{pec})$', fontsize=18)

ax.text(0.85, 0.95, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='white') 

ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

ax.set_ylabel( r'$v_\mathrm{pec} \,\, \mathregular{[km/s]}$', fontsize=label_size, color= text_color )  
ax.set_xlabel( r'$\log_{10} T \,\, \mathregular{[K]}$ ', fontsize=label_size, color=text_color )

ax.set_aspect(1/100)

figure_name = output_dir + f'vlos_temperature_distribution_{n_file}_log.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )







