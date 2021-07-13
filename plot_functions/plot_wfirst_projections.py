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
from tools import *
from colors import * 


input_dir = data_dir + 'cosmo_sims/wfirst_1024/snapshots/h5_files/'
output_dir = data_dir + 'cosmo_sims/wfirst_1024/figures/'
create_directory( output_dir ) 


slice_start = 0
slice_width = 64


projections = {}

n_snap = 500
i = 0
file_name = input_dir + f'grid_CIC_{n_snap:03}.h5'
file = h5.File( file_name, 'r' )
current_z = file.attrs['current_z'][0]
density = file['density']
slice = density[slice_start:slice_start+slice_width, :, :]
proj2 = (slice**2).sum( axis=0 )
proj  = slice.sum( axis=0 )
projection = proj2 / proj
# projection = proj
projection = np.log10( projection )
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


color_map = 'inferno'

nrows, ncols = 3, 3
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(4*ncols,4*nrows))
plt.subplots_adjust( hspace = 0.015, wspace=0.015)

for i in range(nrows):
  for j in range(ncols):
    fig_id = i*ncols + j
    fig_id = 0
    ax = ax_l[i][j]

    z = projections[fig_id]['z']
    projection = projections[fig_id]['projection']
    ax.imshow( projection, cmap=color_map, extent=[0,115, 0,115] )
    
    text_pos_x = 0.75
    ax.text(text_pos_x, 0.95, r'$z={0:.1f}$'.format(z), horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 
    
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    # 
    ax.set_axis_off()
    
    if black_background: 
      fig.patch.set_facecolor('black') 
      ax.set_facecolor('k')
      [ spine.set_edgecolor('black') for spine in list(ax.spines.values()) ]
      
  
    if i == nrows - 1 and j == 0:
      ax.text(0.1, 0.1, r'$35 \, h^{-1}\mathrm{Mpc}$', horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=14, color=text_color) 
      line_start, line_width = 11.5,35 
      line_y = 6
      ax.plot( [line_start, line_start+line_width], [ line_y, line_y], c=text_color, lw=2)


figure_name = output_dir + f'fig_density_wdm_{n_snap}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=400, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )

