import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
import pylab
import palettable
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from colors import *
from figure_functions import *

input_dir  = data_dir + 'cosmo_sims/rescaled_P19/2048_50Mpc/skewers/rescaled_power_spectrum_new/'
output_dir = data_dir + 'cosmo_sims/figures/paper_thermal_history/'
create_directory( output_dir )

files = [ 90, 106,  130, 169 ][::-1]

z_vals = []

data_all = {}
for z_id, n_file in enumerate(files): 
  file_name = input_dir + f'rescaled_ps_{n_file}.pkl'
  ps_data = Load_Pickle_Directory(  file_name )

  current_z = ps_data['z']
  z_vals.append( current_z ) 
  ps_original_data = ps_data['original'] 
  k_vals_0 = ps_original_data['k_vals'] 
  ps_mean_0 = ps_original_data['ps_mean']

  rescaled_data = ps_data['rescaled']

  data_snap = {}
  for data_id in rescaled_data.keys():
    data_ps_rescaled = rescaled_data[data_id]
    alpha = data_ps_rescaled['alpha']
    rescale_factor = data_ps_rescaled['rescale_factor']
    k_vals_rescaled = data_ps_rescaled['k_vals']
    diff_k = np.abs( k_vals_rescaled - k_vals_0 ).sum()
    if diff_k >0: print( f'WARNIG: k_diff:{diff_k}')
    ps_mean_rescaled = data_ps_rescaled['ps_mean']  
    delta_ps = ( ps_mean_rescaled - ps_mean_0 ) / ps_mean_0
    data_snap[data_id] = { 'alpha':alpha, 'rescale_factor':rescale_factor, 'delta_ps':delta_ps, 'k_vals':k_vals_rescaled }
  
  data_all[z_id] = data_snap
  

figure_width = 8
figure_height = 4

tick_size_major, tick_size_minor = 6, 4
tick_label_size_major, tick_label_size_minor = 14, 12
tick_width_major, tick_width_minor = 1.5, 1
border_width = 1.5

text_color = 'black'

font_size = 18
label_size = 16

offset = 1
n = 6+offset
colors = plt.cm.inferno(np.linspace(0,1,n))
  
ncols, nrows = 2, 2
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,figure_height*nrows))
plt.subplots_adjust( hspace = .2, wspace=0.2)  

for index, current_z in enumerate( z_vals ):

  indx_j = index % ncols
  indx_i = index//ncols
  ax = ax_l[indx_i][indx_j]
  
  rescaled_data = data_all[index]
  
  data_snap = data_all[index]
  counter = 0
  for data_id in data_snap: 
    factor = 1
    if data_id == 3: continue
    
    data_rescaled = data_snap[data_id]
    alpha = data_rescaled['alpha']
    k_vals = data_rescaled['k_vals']
    delta_ps = data_rescaled['delta_ps'] * factor
    color = colors[n-counter - 1 - offset] 
    label = ''
    if index == 0:label = r'$\alpha$ = {0:.1f}'.format(alpha)
    ax.plot( k_vals, delta_ps, c=color , label=label )
    counter += 1
  
  ax.axhline( 0, ls='--', color='C3')
  
  text_pos_x = 0.1
  ax.text(text_pos_x, 0.93, r'$z=${0:.1f}'.format(current_z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=font_size ) 


  ax.set_xscale('log')
  ax.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size, labelpad=-8 )
  ax.set_ylabel( r'$\Delta P\,(k) / P\,(k)$', fontsize=label_size )
    
  ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )

  [sp.set_linewidth(border_width) for sp in ax.spines.values()]
  
  ax.set_ylim( -0.8, 0.8)
  ax.set_xlim( 1.5e-3, 0.5)
  
  fig.legend(bbox_to_anchor=(0.82, 0.95), ncol=6,  fontsize=15)


figure_name = output_dir + 'rescaled_power_spectrum.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
