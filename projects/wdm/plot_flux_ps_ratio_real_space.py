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
from data_optical_depth import *
from colors import * 


# data_name = 'zero_temp'
# data_name = 'vmax_120'


# data_name = 'unchanged'
# text = 'Physical redshift vs. real space'

# data_name = 'temp_10'
# text = 'temperature = 10 K everywhere '
# 
# data_name = 'vmin_20'
# text = 'v < 20 km/s is set to zero '
# 
# data_name = 'vmin_50'
# text = 'v < 50 km/s is set to zero '
# 
# data_name = 'vmax_120'
# text = 'v > 120 km/s is set to zero '
# 
data_name = 'vmax_100'
text = 'v > 100 km/s is set to zero '


proj_dir = data_dir + 'projects/wdm/'
input_dir = data_dir + f'cosmo_sims/wdm_sims/compare_wdm/1024_25Mpc_cdm/flux_power_spectrum_{data_name}/'
output_dir = proj_dir + 'figures/flux_ps_wdm_ratio_redshift_real/'
create_directory( output_dir )



snaps = [ 25, 29, 33]

data_all = {}
for space in [ 'redshift', 'real' ]:
  
  data_all[space] = {}
    
  for n_snap,snap_id in enumerate(snaps):

    file_name = input_dir + f'flux_ps_{space}_{snap_id:03}.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z']
    print(z)
    pk_cdm = { 'z':z, 'k_vals':file['k_vals'][...], 'ps_mean':file['ps_mean'][...] }
    file.close()

    data_all[space][n_snap] = pk_cdm


for snap_id in range(3):

  z_real = data_all['real'][snap_id]['z']
  z_redshift = data_all['redshift'][snap_id]['z'] 
  print( f'z: {z_real}  {z_redshift}  ')

  k_real = data_all['real'][snap_id]['k_vals']
  k_redshift = data_all['redshift'][snap_id]['k_vals'] 
  k_vals = k_real

  pk_real = data_all['real'][snap_id]['ps_mean'] * k_vals / np.pi
  pk_redshift = data_all['redshift'][snap_id]['ps_mean'] * k_vals / np.pi

  k_diff = k_real - k_redshift
  print( k_diff ) 

  file_name = output_dir + f'ps_{data_name}_z{z_real}.txt'
  header = f"k [s/km]   pk_redshift   pk_real"
  data = np.array([ k_vals, pk_redshift, pk_real ]).T
  np.savetxt( file_name, data, header=header )
  print( f'Saved File: {file_name}')
  

border_width = 1
text_color = 'k'


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


nrows, ncols = 1, 1

fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.15)


for i in range(3):

  z = data_all['redshift'][i]['z']
  k_vals = data_all['redshift'][i]['k_vals']
  pk_redshift = data_all['redshift'][i]['ps_mean']
  pk_real = data_all['real'][i]['ps_mean']
  
  pk_redshift *= pk_real[0] / pk_redshift[0]
  
  ratio = pk_redshift / pk_real 
  
  label = r'z = {0}'.format(z)
  
  ax.plot( k_vals, ratio, lw=2, label=label )

  ax.legend( frameon=False, loc=3, fontsize=12)

  k_min, k_max = 10**-2.2, 10**-0.7
  ax.fill_between( [k_min, k_max], [-1, -1 ], [1000, 1000], color='gray', alpha=0.3 )
  
  ax.axhline( y=1, ls='--', c='C3')

  ax.text(0.05, 0.95, text, horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 

  ax.set_xscale( 'log')

  ax.set_xlim( 2e-3, 1.2)
  ax.set_ylim( 0.3, 1.6)

  ax.set_ylabel( r'$P_\mathrm{redshift}(k) / P_\mathrm{real}(k)$', fontsize=label_size, color= text_color )  
  ax.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size, color=text_color )
  ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
  ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')


figure_name = output_dir + f'flux_ps_ratio_real_{data_name}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


  



# for snap_id in range(3):
# 
#   z_real = data_all['real'][snap_id]['z']
#   z_redshift = data_all['redshift'][snap_id]['z'] 
#   print( f'z: {z_real}  {z_redshift}  ')
# 
#   k_real = data_all['real'][snap_id]['k_vals']
#   k_redshift = data_all['redshift'][snap_id]['k_vals'] 
#   k_vals = k_real
# 
# 
#   pk_real = data_all['real'][snap_id]['ps_mean'] * k_vals / np.pi
#   pk_redshift = data_all['redshift'][snap_id]['ps_mean'] * k_vals / np.pi
# 
# 
# 
#   k_diff = k_real - k_redshift
#   print( k_diff ) 
# 
#   file_name = output_dir + f'flux_ps_z{z_real}.txt'
#   header = f"k [s/km]   pk_redshift   pk_real"
#   data = np.array([ k_vals, pk_redshift, pk_real ]).T
#   np.savetxt( file_name, data, header=header )
#   print( f'Saved File: {file_name}')
  
# 
# 
# border_width = 1
# text_color = 'k'
# 
# 
# fig_width = 8
# fig_dpi = 300
# label_size = 18
# figure_text_size = 18
# legend_font_size = 16
# tick_label_size_major = 15
# tick_label_size_minor = 13
# tick_size_major = 5
# tick_size_minor = 3
# tick_width_major = 1.5
# tick_width_minor = 1
# border_width = 1
# 
# 
# nrows, ncols = 1, 3
# 
# fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
# plt.subplots_adjust( hspace = 0.1, wspace=0.15)
# 
# 
# for i in range(3):
# 
#   z = data_all['redshift'][i]['z']
#   k_vals = data_all['redshift'][i]['k_vals']
#   pk_redshift = data_all['redshift'][i]['ps_mean']
#   pk_real = data_all['real'][i]['ps_mean']
#   ratio = pk_redshift / pk_real 
# 
# 
#   ax = ax_l[i]
# 
# 
#   ax.plot( k_vals, ratio, lw=2, label=r'' )
# 
#   ax.legend( frameon=False, loc=3, fontsize=12)
# 
#   k_min, k_max = 10**-2.2, 10**-0.7
#   ax.fill_between( [k_min, k_max], [-1, -1 ], [1000, 1000], color='gray', alpha=0.3 )
# 
#   ax.text(0.1, 0.1, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 
# 
#   ax.set_xscale( 'log')
# 
#   ax.set_xlim( 2e-3, 3e-1)
#   ax.set_ylim( 0.1, 1.05)
# 
#   ax.set_ylabel( r'$P_\mathrm{redshift}(k) / P_\mathrm{real}(k)$', fontsize=label_size, color= text_color )  
#   ax.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size, color=text_color )
#   ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
#   ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
# 
# 
# 
# 
# 
# figure_name = output_dir + f'flux_ps_ratio_real_space.png'
# fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
# print( f'Saved Figure: {figure_name}' )
# 
# 
# 
