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
from colors import * 



dir_cdm = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc/slices/'
dir_wdm_0 = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m3.0kev/slices/'
dir_wdm_1 = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m1.0kev/slices/'
dir_wdm_2 = data_dir + 'cosmo_sims/rescaled_P19/wdm/1024_50Mpc_wdm_m0.5kev/slices/'
output_dir = data_dir + 'cosmo_sims/figures/paper_wdm_2021/'
create_directory( output_dir ) 

input_dirs = [ dir_cdm, dir_wdm_0, dir_wdm_1, dir_wdm_2 ]
n_sims = len( input_dirs )


labels = [ r'$\mathrm{CDM}$', r'$\mathrm{WDM\,\,\, m = 3.0 keV}$', r'$\mathrm{WDM\,\,\, m = 1.0 \,keV}$', r'$\mathrm{WDM\,\,\, m = 0.5 \,keV}$', ]
labels = [ r'CDM', r'WDM  $m = 3.0 \,\,\mathrm{keV}$', r'WDM  $m = 1.0 \,\,\mathrm{keV}$', r'WDM  $m = 0.5 \,\,\mathrm{keV}$', ]



data_type = 'hydro'
# data_type = 'particles'
field = 'density'
slice_start, slice_depth = 192, 64


n_snap = 11

val_max = None

# data_types = ['particles', 'hydro']
data_types = [ 'hydro']

vmin, vmax = np.inf, -np.inf

projections = {}
for i in range(n_sims):
  input_dir = input_dirs[i]
  data_sim = {}
  for data_type in data_types:
    file_name = input_dir + f'slice_{data_type}_{n_snap}_start{slice_start}_depth{slice_depth}.h5'
    file = h5.File( file_name, 'r' )
    current_z = file.attrs['current_z']

    slice = file[field][...]
    proj2 = (slice**2).sum( axis=0 )
    proj  = slice.sum( axis=0 )
    projection = proj2 / proj
    if data_type == 'hydro': scale = 0.01
    if data_type == 'particles': scale = 0.1
    if not val_max: val_max = scale*projection.max()
    projection[projection > val_max] = val_max
    projection = np.log10( projection )
    data_sim[data_type] = projection
    vmax = max( vmax, projection.max() )
    vmin = min( vmin, projection.min() )
  projections[i] = data_sim
  


font_size = 12
figure_text_size = 14
text_color = 'black'

black_background = False
if black_background:
  text_color = 'white'
  color_line = blues[4]
  
matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'
if system == 'Lux':      prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/brvillas/fonts', "Helvetica.ttf"), size=12)
if system == 'Shamrock': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)
if system == 'Tornado': prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=12)


data_type = 'hydro' 
if data_type == 'hydro': color_map = cmap_deep_r

nrows, ncols = 2, 2
# fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(4*ncols,4*nrows))
# plt.subplots_adjust( hspace = 0.02, wspace=0.02 )


fig = plt.figure(figsize=(4*ncols, 4*nrows))
from mpl_toolkits.axes_grid1 import ImageGrid
grid = ImageGrid(fig, 111,          # as in plt.subplot(111)
                 nrows_ncols=(nrows, ncols),
                 axes_pad=0.08,
                 share_all=True,
                 cbar_location="right",
                 cbar_mode="single",
                 cbar_size="3%",
                 cbar_pad=0.1,
                 )

# for i in range(nrows):
#   for j in range(ncols):
    # fig_id = i*ncols + j
    # ax = ax_l[i][j]
    
for fig_id, ax in enumerate(grid):
  
  projection = projections[fig_id][data_type]

  im = ax.imshow( projection, cmap=color_map, extent=[0, 50, 0, 50], vmin=vmin, vmax=vmax )
    
    
  text_pos_x = 0.05
  text_pos_y = 0.07
  bbox_props = dict(boxstyle="round", fc="gray", ec="0.5", alpha=0.5)
  ax.text(text_pos_x, text_pos_y, labels[fig_id], horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='white', bbox=bbox_props) 
  
  ax.set_yticklabels([])
  ax.set_xticklabels([])
  ax.set_yticks([])
  ax.set_xticks([])
  
  if fig_id == 3: 
    text_pos_x = 0.85
    ax.text(text_pos_x, 0.92, r'$z={0:.1f}$'.format(current_z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='white', bbox=bbox_props) 
    # 
    ax.text(0.095, 0.94, r'$15 \, h^{-1}\mathrm{Mpc}$', horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='white') 
    line_start, line_width = 5, 15
    line_y = 45
    ax.plot( [line_start, line_start+line_width], [ line_y, line_y], c='white', lw=2)

  
  leg = ax.legend(loc=2, frameon=False, fontsize=22, prop=prop)
  for text in leg.get_texts():
    plt.setp(text, color = text_color)
  
  if black_background: 
    fig.patch.set_facecolor('black') 
    ax.set_facecolor('k')
    [ spine.set_edgecolor('black') for spine in list(ax.spines.values()) ]


# Colorbar
cbar = ax.cax.colorbar(im)
ax.cax.toggle_label(True)
cbar.ax.tick_params(labelsize=12, size=4, width=1.5, length=3, direction='in' )
cbar.set_ticks( [ 1, 2, 3, 4] )
cbar.set_label( r'$\log_{10}  \, \rho_{\mathrm{gas}}  \,\,\, [  h^2 \mathrm{M_\odot } \mathrm{kpc}^{-3} ] $', fontsize=14 )

figure_name = output_dir + f'fig_gas_density_wdm.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )



# nrows, ncols = 2, 4
# fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(4*ncols,4*nrows))
# plt.subplots_adjust( hspace = 0.01, wspace=0.01)
# 
# for i in range(nrows):
#   for j in range(ncols):
#     # fig_id = i*ncols + j
#     fig_id = j
#     ax = ax_l[i][j]
# 
#     if i == 0: data_type = 'particles'
#     if i == 1: data_type = 'hydro' 
#     projection = projections[fig_id][data_type]
# 
#     if data_type == 'particles': color_map = 'inferno'
#     if data_type == 'hydro': color_map = cmap_deep_r
# 
#     ax.imshow( projection, cmap=color_map )
# 
#     text_pos_x = 0.05
#     ax.text(text_pos_x, 0.95, labels[fig_id], horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 
# 
#     ax.set_yticklabels([])
#     ax.set_xticklabels([])
# 
#     # ax.set_axis_off()
#     if j == 0: 
#       text_pos_x = 0.15
#       ax.text(text_pos_x, 0.05, r'$z={0:.1f}$'.format(current_z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=16, color=text_color) 
#       if data_type == 'particles': ylabel = r'$\mathrm{DM\,\, Density}$'
#       if data_type == 'hydro': ylabel = r'$\mathrm{Gas\,\, Density}$'
#       ax.set_ylabel( ylabel, fontsize=14, color=text_color, labelpad=-4 )
# 
#     leg = ax.legend(loc=2, frameon=False, fontsize=22, prop=prop)
#     for text in leg.get_texts():
#       plt.setp(text, color = text_color)
# 
#     if black_background: 
#       fig.patch.set_facecolor('black') 
#       ax.set_facecolor('k')
#       [ spine.set_edgecolor('black') for spine in list(ax.spines.values()) ]
# 
# 
# figure_name = output_dir + f'fig_density_wdm_{n_snap}.png'
# fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
# print( f'Saved Figure: {figure_name}' )
# 
