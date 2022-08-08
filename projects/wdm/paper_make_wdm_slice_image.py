import sys, time, os
from os import listdir
from os.path import isfile, join
import matplotlib.colors as cl
import matplotlib.cm as cm
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import palettable
import h5py as h5
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.axes_grid1 import make_axes_locatable
#Add Modules from other directories
root_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
sub_directories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(sub_directories)
from tools import *
from cosmology import Cosmology
from constants_cosmo import Myear

black_background = False

proj_dir = data_dir + 'projects/wdm/'
input_dir  = proj_dir + 'data/wdm_slice/images/'
output_dir = proj_dir + 'figures/'
create_directory( output_dir )


# Initialize Cosmology
z_start = 10000
cosmo = Cosmology( z_start )
cosmo_z = cosmo.z_vals
cosmo_t = cosmo.t_vals / Myear / 1000 #Gyear


pixel_data = h5.File( input_dir + 'pixel_data.h5', 'r')
pixel_z_raw = pixel_data['pixel_z'][...]
pixel_m_raw = pixel_data['pixel_m'][...]
nz = len( pixel_z_raw )
nm = len( pixel_m_raw )
xz_raw = np.linspace( 0, nz-1, nz )
xm_raw = np.linspace( 0, nm-1, nm )

image_file_name = input_dir + 'slice_wdm_extended_new.png'
print(  f'Loading Image: {image_file_name}' )
mp_image = mpimg.imread(image_file_name)
ny, nx, nc = mp_image.shape

xz = np.linspace(0, nz-1, nx)
xm = np.linspace(0, nm-1, ny)
pixel_m = np.interp( xm, xm_raw, pixel_m_raw )
pixel_z = np.interp( xz, xz_raw, pixel_z_raw )

m_min, m_max = 0.4, 100000
invm_max, invm_min = 1/m_min, 1/m_max
pixel_m = np.linspace( invm_max, invm_min, ny)


crop_l, crop_r, crop_u, crop_d = 700, 300, 100, 50
mp_image = mp_image[crop_u:ny-crop_d,crop_l:nx-crop_r,:]
pixel_m = pixel_m[crop_u:ny-crop_d]
pixel_z = pixel_z[crop_l:nx-crop_r]
ny, nx, nc = mp_image.shape

pixel_t = []
for z in pixel_z:
  z_diff = np.abs( z - cosmo_z )
  indx = np.where( z_diff == z_diff.min() )[0][0]
  t = cosmo_t[indx] 
  pixel_t.append( t )
pixel_t = np.array( pixel_t )



out_nx, out_ny = nx, ny
dpi = 400 
w, h = out_nx / dpi, out_ny / dpi
print( f'Fig dpi: {dpi}')
print( f'Image Size: ({w}, {h})')
print( f'Image Size: ({out_nx}, {out_ny})')

import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

text_color = 'black'
tick_color = 'black'
labelsize = 14
tick_label_size_major, tick_label_size_minor = 11, 10
tick_size_major, tick_size_minor = 5, 3
tick_width_major, tick_width_minor = 1.9, 1
border_width = 1.4

if black_background:
  text_color = 'white'
  tick_color = 'white'

# fig = plt.figure(figsize=(w,h))
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(w,h))

colormap = palettable.scientific.sequential.Davos_20.mpl_colormap
im = plt.imshow( mp_image, cmap=colormap, extent=(0, nx, ny, 0 ) )


line_y = ny-150
line_x = 200
line_length = 400
plt.text( line_x + 14, line_y-33, '30 cMpc', fontsize=14, color='white'  )
plt.plot( [line_x, line_x+line_length], [line_y, line_y], lw=1.5, c='white')

tick_labels = [ 0.3,  0.5, 1.0,  2.0,  4.0, 6.0, 'CDM' ] 
tick_vals =   [ 2.5,  1.8, 1.3,  0.85, 0.5, 0.2, 0.001 ]
tick_indices = []
for tick_val in tick_vals:
  diff = np.abs( pixel_m - tick_val )
  indx = np.where( diff == diff.min() )[0][0]
  tick_indices.append( indx )
ax.set_yticks( tick_indices, labels=tick_labels )



tick_vals =   [ 5.0, 4.0, 3.0, 2.0, 1.0, 0.5, 0.2 ]
tick_indices = []
for tick_val in tick_vals:
  diff = np.abs( pixel_z - tick_val )
  indx = np.where( diff == diff.min() )[0][0]
  tick_indices.append( indx )
ax.set_xticks( tick_indices, labels=tick_vals )


# axtop = ax.twiny()
axtop = ax.secondary_xaxis('top')
tick_vals =   [ 1.2, 2.0, 4.0, 8.0, 12.0, ]
tick_indices = []
for tick_val in tick_vals:
  diff = np.abs( pixel_t - tick_val )
  indx = np.where( diff == diff.min() )[0][0]
  tick_indices.append( indx )
axtop.set_xticks( tick_indices, labels=tick_vals )

dens_max = 5.585e+05 * 10 * 5 * cosmo.h**2
dens_min = 0.005 * 10 * cosmo.h**2
log_dens_x = np.linspace( 0, 1, 1000 )
log_dens_vals = np.linspace( np.log10(dens_min), np.log10(dens_max), 1000 )

log_d_vals = [ -1, 1, 3, 5, 7, ]
tick_labels = []
tick_vals = []
for log_d in log_d_vals:
  d_diff = np.abs( log_dens_vals - log_d )
  indx = np.where( d_diff == d_diff.min() )[0][0]
  tick_val = log_dens_x[indx]
  tick_vals.append( tick_val )
  tick_string = '\mathregular{10}^{\mathregular{' + f'{log_d}' + '}}'
  tick_label = r'${0}$'.format( tick_string ) 
  tick_labels.append( tick_label )

# cax = ax.inset_axes([1.04, 0.1, 0.05, 0.8], transform=ax.transAxes)
cax   = inset_axes(ax,
                   width="3.5%", 
                   height="70%", 
                   loc='center left',
                   bbox_to_anchor=(1.02, 0., 1, 1),
                   bbox_transform=ax.transAxes,
                   borderpad=0,
                   )
cbar = fig.colorbar(im, cax=cax )
[sp.set_linewidth(1.2) for sp in cbar.ax.spines.values()]
cbar.ax.tick_params(axis='both', which='major', direction='in', color=tick_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
cbar.set_label( r'$\rho_\mathrm{gas}$   [$\mathregular{M}\!_\odot \mathregular{kpc}^{\mathregular{-3}}$]', fontsize=labelsize-2, color=text_color, labelpad=-2 )
cbar.ax.set_yticks( tick_vals, labels=tick_labels )
# divider = make_axes_locatable(ax)
# cax = divider.append_axes("right", size="5%", pad=0.05)
# fig.colorbar(im, ax=ax, cax=cax )

ax.tick_params(axis='both', which='major', direction='in', color=tick_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
ax.tick_params(axis='both', which='minor', direction='in', color=tick_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
axtop.tick_params(axis='x', which='major', direction='in', color=tick_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
axtop.tick_params(axis='x', which='minor', direction='in', color=tick_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )

ax.set_xlabel( r'$\mathregular{Redshift}  \,\,\, z$', fontsize=labelsize, color=text_color)
ax.set_ylabel( r'$m_\mathregular{WDM} \,\,\,  \mathregular{[keV]}$', fontsize=labelsize, labelpad=-5, color=text_color )
axtop.set_xlabel( 'Time after the Big Bang  [Gyr]', fontsize=labelsize - 2, color=text_color, labelpad=5)

[sp.set_linewidth(border_width) for sp in ax.spines.values()]

if black_background: 
  fig.patch.set_facecolor('black') 
  ax.set_facecolor('k')
  [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]
  [ sp.set_edgecolor(text_color) for sp in cbar.ax.spines.values() ]
  

out_file_name = output_dir + f'slice_wdm_composite.png'
if black_background: out_file_name = output_dir + f'slice_wdm_composite_black.png'
plt.savefig( out_file_name, bbox_inches='tight', dpi=dpi, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {out_file_name} ')

