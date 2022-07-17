import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
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
output_dir = proj_dir + 'figures/tau_distribution/'
create_directory( output_dir )

type = 'cdm'
type = 'wdm'

files = [ 25, 29, 33]

n_file = files[rank]

if type == 'cdm': sim_dir  = data_dir + f'cosmo_sims/wdm_sims/new/1024_25Mpc_cdm/'
if type == 'wdm': sim_dir  = data_dir + f'cosmo_sims/wdm_sims/new/1024_25Mpc_m4.0kev/'
flux_dir = data_dir + f'cosmo_sims/wdm_sims/new/transmitted_flux/'
input_dir  = sim_dir + f'skewers_files/'

axis_list = [ 'x', 'y', 'z' ]
n_skewers_list = [ 'all', 'all', 'all']
skewer_ids_list = [ 'all', 'all', 'all']
field_list = [  'HI_density', 'los_velocity',  ]


skewer_dataset = Load_Skewers_File( n_file, input_dir, axis_list=axis_list, fields_to_load=field_list )
HI_density = skewer_dataset['HI_density']
los_velocity = skewer_dataset['los_velocity']

space = 'redshift'
file_name = flux_dir + f'lya_flux_{type}_{space}_{n_file:03}.h5'
file = h5.File( file_name, 'r' )
z = file.attrs['current_z']
skewers_Flux_redshift = file['skewers_Flux'][...]

space = 'real'
file_name = flux_dir + f'lya_flux_{type}_{space}_{n_file:03}.h5'
file = h5.File( file_name, 'r' )
z = file.attrs['current_z']
skewers_Flux_real = file['skewers_Flux'][...]







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


n_rows, n_cols = 1, 2

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

n_pixles = 1024 * 5000

flux_min = 1e-200

for i in range(2):

  if i == 0: 
    skewers_Flux = skewers_Flux_redshift
    base = 'Redshift space  '
  if i == 1: 
    skewers_Flux = skewers_Flux_real
    base = 'Real space  '
  
  
  flux = skewers_Flux.flatten()[:n_pixles]
  indices = flux < flux_min
  flux[indices] = flux_min
  
  tau = - np.log( flux )
  log_tau = np.log10( tau )
  HI_dens = np.log10(HI_density.flatten())[:n_pixles]
  vel = los_velocity.flatten()[:n_pixles]
  
  flux_mean = flux.mean()

  ax = grid[i]
  im = ax.scatter( HI_dens, vel, c=log_tau, s=0.5, vmin=-0.5, vmax=3, alpha=alpha, cmap=colormap  )
  
  ax.set_title(base + r'$\overline{F}$ = ' + f'{flux_mean:.3f}', fontsize=16 )
  
  cb = ax.cax.colorbar(im,   )
  cb.ax.tick_params(labelsize=tick_label_size_major, size=tick_size_major, color=text_color, width=tick_width_major, length=tick_size_major, labelcolor=text_color, direction='in' )
  ax.cax.toggle_label(True)
  [sp.set_linewidth(border_width) for sp in cb.ax.spines.values()]
  cb.set_label( r'$\log_{10} \, \tau$', fontsize=18)
  ax.set_aspect(0.014)
  
  ax.text(0.89, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 
  
  ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
  ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

  ax.set_ylabel( 'LOS Velocity [km/s]', fontsize=label_size, color= text_color )  
  ax.set_xlabel( r'$\log_{10} \rho_\mathrm{HI}$ ', fontsize=label_size, color=text_color )
  
  ax.set_ylim( -300, 300 )
  

figure_name = output_dir + f'tau_distribution_{type}_{n_file}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )







