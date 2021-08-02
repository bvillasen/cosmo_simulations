import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab

cosmo_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
# from tools import *
# from colors import * 

data_dir = '/data/groups/comp-astro/bruno/'
input_dir = data_dir + 'cosmo_sims/wfirst_1024/snapshots/h5_files/grid_files/'
output_dir = data_dir + 'cosmo_sims/wfirst_1024/figures/'
# create_directory( output_dir ) 


slice_width = 64
slice_start = 14*slice_width
slice_start = 0*slice_width

dens_max = 2e6 /100
dens_min = 1e1
projections = {}

snapshots = np.arange( 50, 501, 50 )[::-1]

vmin, vmax = np.inf, -np.inf
for i, n_snap in enumerate(snapshots):
  file_name = input_dir + f'grid_CIC_{n_snap:03}.h5'
  file = h5.File( file_name, 'r' )
  current_z = file.attrs['current_z'][0]
  density = file['density']
  slice = density[slice_start:slice_start+slice_width, :, :]
  slice[slice > dens_max ] = dens_max
  slice[slice < dens_min ] = dens_min
  proj2 = (slice**2).sum( axis=0 )
  proj  = slice.sum( axis=0 )
  projection = proj2 / proj
  # projection = proj
  projection = np.log10( projection )
  vmax = max( vmax, projection.max() )
  vmin = min( vmin, projection.min() )
  print( vmin, vmax )
  data_sim = { 'projection':projection, 'z':current_z }
  projections[i] = data_sim



font_size = 12
figure_text_size = 16
text_color = 'white'

black_background = False
if black_background:
  text_color = 'white'
  color_line = blues[4]

matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'
if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=12)
if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)


# color_map = 'inferno'
color_map = palettable.cmocean.sequential.Dense_20_r.mpl_colormap
# color_map = palettable.scientific.sequential.Devon_20.mpl_colormap

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'


nrows, ncols = 3, 3
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(5*ncols,4*nrows))
plt.subplots_adjust( hspace = 0.015, wspace=0.015)

fig = plt.figure(figsize=(5*ncols, 4*nrows))

from mpl_toolkits.axes_grid1 import ImageGrid

grid = ImageGrid(fig, 111,          # as in plt.subplot(111)
                 nrows_ncols=(nrows, ncols),
                 axes_pad=0.08,
                 share_all=True,
                 cbar_location="right",
                 cbar_mode="single",
                 cbar_size="3%",
                 cbar_pad=0.15,
                 )
#
# for i in range(nrows):
#   for j in range(ncols):
for fig_id, ax in enumerate(grid):
  # fig_id = i*ncols + j
  # ax = ax_l[i][j]

  z = projections[fig_id]['z']
  projection = projections[fig_id]['projection']
  im = ax.imshow( projection, vmax=vmax, vmin=vmin, cmap=color_map, extent=[0,115, 0,115] )

  text_pos_x = 0.95
  ax.text(text_pos_x, 0.94, r'$z={0:.1f}$'.format(z), horizontalalignment='right',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 

  ax.set_yticks([])
  ax.set_xticks([])
  # 
  # ax.set_axis_off()

  if black_background: 
    fig.patch.set_facecolor('black') 
    ax.set_facecolor('k')
    [ spine.set_edgecolor('black') for spine in list(ax.spines.values()) ]


  if fig_id == 8:
    ax.text(0.1, 0.1, r'$40 \, h^{-1}\mathrm{Mpc}$', horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=16, color=text_color) 
    line_start, line_width = 11.5, 40
    line_y = 5
    ax.plot( [line_start, line_start+line_width], [ line_y, line_y], c=text_color, lw=2)


# Colorbar
cbar = ax.cax.colorbar(im)
ax.cax.toggle_label(True)
cbar.ax.tick_params(labelsize=12, size=5, width=2, length=3, direction='in' )
cbar.set_label_text( r'$\log_{10}  \,( \rho_{\mathrm{DM}} /   h^2 \mathrm{M_\odot } \mathrm{kpc}^{-3} ) $', fontsize=14 )

figure_name = output_dir + f'fig_density_dm.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=400, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )

