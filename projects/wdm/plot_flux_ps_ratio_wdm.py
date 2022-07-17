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


proj_dir = data_dir + 'projects/wdm/'
input_dir = data_dir + 'cosmo_sims/wdm_sims/new/flux_power_spectrum/'
output_dir = proj_dir + 'figures/flux_ps_wdm_ratio/'
create_directory( output_dir )


snap_id = 25
snap_id = 29
snap_id = 33

data_all = {}
for space in [ 'redshift', 'real' ]:
  
  data_all[space] = {}
    
  file_name = input_dir + f'flux_ps_cdm_{space}_{snap_id:03}.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  pk_cdm = { 'k_vals':file['k_vals'][...], 'ps_mean':file['ps_mean'][...] }
  file.close()

  file_name = input_dir + f'flux_ps_wdm_{space}_{snap_id:03}.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  pk_wdm = { 'k_vals':file['k_vals'][...], 'ps_mean':file['ps_mean'][...] }
  file.close()
  
  file_name = input_dir + f'flux_ps_wdm_{space}_{snap_id:03}_replaced_cdm_density.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  pk_wdm_density = { 'k_vals':file['k_vals'][...], 'ps_mean':file['ps_mean'][...] }
  file.close()

  file_name = input_dir + f'flux_ps_wdm_{space}_{snap_id:03}_replaced_cdm_velocity.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  pk_wdm_velocity = { 'k_vals':file['k_vals'][...], 'ps_mean':file['ps_mean'][...] }
  file.close()
  
  file_name = input_dir + f'flux_ps_wdm_{space}_{snap_id:03}_replaced_cdm_temperature.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z']
  pk_wdm_temperature = { 'k_vals':file['k_vals'][...], 'ps_mean':file['ps_mean'][...] }
  file.close()

  data_all[space]['cdm'] = pk_cdm
  data_all[space]['wdm'] = pk_wdm
  data_all[space]['wdm_density'] = pk_wdm_density
  data_all[space]['wdm_velocity'] = pk_wdm_temperature
  data_all[space]['wdm_temperature'] = pk_wdm_velocity
  
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


nrows, ncols = 1, 2

fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.15)


titles = [ 'Redshift Space', 'Real Space' ]

for i in range(2):
  
  if i == 0: space = 'redshift'
  if i == 1: space = 'real'
  
  data = data_all[space]
  
  k_vals = data['cdm']['k_vals']
  pk_cdm = data['cdm']['ps_mean']
  pk_wdm = data['wdm']['ps_mean']
  pk_wdm_density = data['wdm_density']['ps_mean']
  pk_wdm_velocity = data['wdm_velocity']['ps_mean']
  pk_wdm_temperature = data['wdm_temperature']['ps_mean']
  
  
  ratio_wdm = pk_wdm / pk_cdm 
  ratio_wdm_density = pk_wdm_density / pk_cdm 
  ratio_wdm_velocity = pk_wdm_velocity / pk_cdm
  ratio_wdm_temperature = pk_wdm_temperature / pk_cdm  
  
  ax = ax_l[i]
  
  ax.set_title( titles[i], fontsize = 13)
  
  ax.plot( k_vals, ratio_wdm, lw=3.5, label=r'WDM  $m=4\,\, \mathrm{keV}$' )
  ax.plot( k_vals, ratio_wdm_density, '--', lw=2, label='WDM with CDM HI_density' )
  ax.plot( k_vals, ratio_wdm_temperature, '--', lw=2, label='WDM with CDM temperature' )
  ax.plot( k_vals, ratio_wdm_velocity, '--', lw=2, label='WDM with CDM LOS peculiar velocity' )
  
  ax.legend( frameon=False, loc=3, fontsize=12)
  
  k_min, k_max = 10**-2.2, 10**-0.7
  ax.fill_between( [k_min, k_max], [-1, -1 ], [1000, 1000], color='gray', alpha=0.3 )
  
  ax.text(0.1, 0.3, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 

  ax.set_xscale( 'log')
  
  ax.set_xlim( 2e-3, 3e-1)
  ax.set_ylim( 0.6, 1.1)
  
  ax.set_ylabel( r'$P_\mathrm{WDM}(k) / P_\mathrm{CDM}(k)$', fontsize=label_size, color= text_color )  
  ax.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size, color=text_color )
  ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
  ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

  
  


figure_name = output_dir + f'flux_ps_ratio_wdm_{space}_{snap_id}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )



