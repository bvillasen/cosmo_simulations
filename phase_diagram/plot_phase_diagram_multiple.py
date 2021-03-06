import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pickle
from mpl_toolkits.axes_grid1 import ImageGrid
import palettable

root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from phase_diagram_functions import *

use_mpi = True
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

import matplotlib
matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/Downloads'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

delta_min, delta_max = 0, 1.0


input_dir_0 = data_dir + f'cosmo_sims/256_50Mpc/analysis_files_grackle/'
input_dir_1 = data_dir + f'cosmo_sims/256_50Mpc/analysis_files_cholla/'
output_dir = data_dir + f'cosmo_sims/256_50Mpc/figures/phase_diagram/'
create_directory( output_dir )


input_dirs = [ input_dir_0, input_dir_1 ]

snapshots = np.arange( 0, 200, 1, dtype=int )

local_ids = split_indices( snapshots, rank, n_procs )
snaps_local = snapshots[local_ids]

data_all = {}
for sim_id,input_dir in enumerate(input_dirs):
  fit_dir = input_dir + f'fit_mcmc_delta_{delta_min}_{delta_max}/'
  # Load phase diagram
  v_min, v_max = np.inf, -np.inf 
  data_sim = {}
  for n_snap in snaps_local:
    in_file_name = input_dir + f'{n_snap}_analysis.h5'
    in_file = h5.File( in_file_name, 'r' )
    current_z = in_file.attrs['current_z'][0]
    pd_data = in_file['phase_diagram']
    phase = pd_data['data'][...]
    n_dens = pd_data.attrs['n_dens'][0]
    n_temp = pd_data.attrs['n_temp'][0]
    temp_max = pd_data.attrs['temp_max'][0]
    temp_min = pd_data.attrs['temp_min'][0]
    dens_max = pd_data.attrs['dens_max'][0]
    dens_min = pd_data.attrs['dens_min'][0]
    log_temp_max = np.log10(temp_max)
    log_temp_min = np.log10(temp_min) 
    log_dens_max = np.log10(dens_max)
    log_dens_min = np.log10(dens_min) 
    log_temp_vals = np.linspace( log_temp_min, log_temp_max, n_temp )
    log_dens_vals = np.linspace( log_dens_min, log_dens_max, n_dens )
    dens_points, temp_points = np.meshgrid( log_dens_vals, log_temp_vals )
    temp_points = temp_points.flatten()
    dens_points = dens_points.flatten()
    phase_1D = phase.flatten() 
    indices = np.where(phase_1D > 0 )
    phase_1D = phase_1D[indices]
    dens_points = dens_points[indices]
    temp_points = temp_points[indices]
    indices = np.where( phase_1D > 1*phase_1D.min() )
    phase_1D = phase_1D[indices]
    dens_points = dens_points[indices]
    temp_points = temp_points[indices]
    phase_1D = np.log10( phase_1D )
    v_min = min( v_min, phase_1D.min() ) 
    v_max = max( v_max, phase_1D.max() )
    # fit_file = fit_dir + f'fit_{n_snap}.pkl'
    # fit_data = Load_Pickle_Directory( fit_file )
    # T0 = fit_data['T0']['mean']
    # gamma = fit_data['gamma']['mean']
    # data_snap = { 'dens_points':dens_points, 'temp_points':temp_points, 'phase_1D':phase_1D, 'T0':T0, 'gamma':gamma, 'z':current_z }
    data_snap = { 'dens_points':dens_points, 'temp_points':temp_points, 'phase_1D':phase_1D, 'z':current_z }
    data_sim[n_snap] = data_snap
  data_all[sim_id] = data_sim



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

text_color = 'black'

n_data = 2
n_rows = 1
n_cols = n_data

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

labels = ['Grackle', 'Cholla']


# n_snap = 0
for n_snap in snaps_local:

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

  colormap =  'turbo'
  alpha = 0.6

  x_min, x_max = -2, 4
  y_min, y_max =  0, 8.
  
  for sim_id in data_all:

    ax = grid[sim_id]
    z = data_all[sim_id][n_snap]['z'] 
    dens_points = data_all[sim_id][n_snap]['dens_points']
    temp_points = data_all[sim_id][n_snap]['temp_points']
    phase_1D    = data_all[sim_id][n_snap]['phase_1D'] 
    im = ax.scatter( dens_points, temp_points, c=phase_1D, s=0.1, vmin=v_min, vmax=v_max, alpha=alpha, cmap=colormap  )


    # Add the fit line
    # T0 = data_all[n_snap]['T0']
    # gamma = data_all[n_snap]['gamma']
    # x_l, x_r = delta_min, delta_max
    # line_x = np.linspace( x_l, x_r, 100 )
    # line_y = gamma*line_x + T0
    # ax.plot( line_x, line_y, '--', c='w', alpha=1, lw=1.8 ) 
    # 
    # T0 = 10**T0
    # T0_4 = T0 * 1e-4
    # text = r' $\,  \gamma  = {0:.2f} $'.format( gamma+1 ) + '\n' + r'$T_0 = {0:.2f} \times 10^4   \,\,  $'.format( T0_4 ) + r'$\mathrm{K}$' 
    # ax.text(0.65, 0.1, text, horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color)
    


    cb = ax.cax.colorbar(im,   )
    cb.ax.tick_params(labelsize=tick_label_size_major, size=tick_size_major, color=text_color, width=tick_width_major, length=tick_size_major, labelcolor=text_color, direction='in' )
    ax.cax.toggle_label(True)
    [sp.set_linewidth(border_width) for sp in cb.ax.spines.values()]

    ax.set_aspect( 0.6)
    # 
    font = {'fontname': 'Helvetica',
        'color':  text_color,
        'weight': 'normal',
        'size': label_size,
        'ha':'center'
        }
    cb.set_label_text( r'$\log_{10}  \,\, P\,(\Delta, T\,) $', fontdict=font )
    # cb.set_label( r'$\log_{10}  \,\, P\,(\Delta, T\,) $', fontdict=font )
    ax.set_ylabel(r'$\log_{10} \, T \,\,[\,\mathrm{K}\,]$', fontsize=label_size , color=text_color)
    ax.set_xlabel(r'$\log_{10} \, \Delta$ ', fontsize=label_size , color=text_color )

    text  = r'$z = {0:.1f}$'.format( z ) 
    ax.text(0.03, 0.95, text, horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color)

    text  = f'{labels[sim_id]}' 
    ax.text(0.83, 0.95, text, horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color)

    ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in')
    ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
    [sp.set_linewidth(border_width) for sp in ax.spines.values()]
    ax.set_xlim( x_min, x_max )
    ax.set_ylim( y_min, y_max )

  out_fileName = output_dir + f'phase_diagram_{n_snap}.png'
  fig.savefig( out_fileName,  pad_inches=0.1,  facecolor=fig.get_facecolor(),  bbox_inches='tight', dpi=300)
  print( f'Saved Image:  {out_fileName} ')




