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
from load_tabulated_data import load_data_boera

ps_data_dir = cosmo_dir + 'lya_statistics/data/'
input_dir  = data_dir + 'figures/wdm/pk_convergence/'
output_dir = data_dir + 'figures/wdm/pk_convergence/'
create_directory( output_dir )

dir_data_boera = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_data_boera( dir_data_boera )
k_vals = data_boera[0]['k_vals'] 


file_name = input_dir + 'pk_scale_H_Eheat_interpolated.pkl'
pk_data = Load_Pickle_Directory( file_name )
param_vals = np.array(pk_data['param_change_vals'])
refference_id = np.where( param_vals == 1.0 )[0][0]
print( f'alpha=1 id: {refference_id}')
pk_reference_all = pk_data['pk_samples'][refference_id]['interpolated']


z_vals = [ 4.2, 4.6, 5.0 ]

# ids_to_plot = [ 0, 1, 2, 3, 4, 5, 6, 7, 8]
ids_to_plot = [ 0, 1, 2, 3, 4, 5, ]

nrows = 1
ncols = 3

tick_size_major, tick_size_minor = 6, 4
tick_label_size_major, tick_label_size_minor = 14, 12
tick_width_major, tick_width_minor = 1.5, 1

font_size = 18
label_size = 16
alpha = 0.7

line_width = 0.6

border_width = 1.5

text_color  = 'black'
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8*ncols,6*nrows))


n_local = 16
for i in range(3):
  ax = ax_l[i]
  
  for data_id in ids_to_plot:
    pk_all = pk_data['pk_samples'][data_id]['interpolated']
    pk = pk_all[i*n_local:(i+1)*n_local]
    pk_reference = pk_reference_all[i*n_local:(i+1)*n_local]
    pk_diff = ( pk - pk_reference ) / pk_reference
    val = param_vals[data_id]
    label = r'$\alpha$=' + f'{val:.1f}'
    ax.plot( k_vals, pk_diff, label=label )
    
  ax.axhline( y=0, ls='--', c='C3')
    
  ax.legend( loc=2, frameon=False, fontsize=font_size-4)
  ax.text(0.89, 0.93, r'$z=${0:.1f}'.format(z_vals[i]), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=font_size, color=text_color) 
  ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
  ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
  
  ax.set_xscale('log')
  ax.set_ylabel( r'$ \Delta P\,(k) / P\,(k, \alpha=1.0)$', fontsize=label_size, color= text_color ) 
  ax.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size, color=text_color )


# figure_name = output_dir + 'pk_convergence_simulations.png'
figure_name = output_dir + 'pk_convergence_interpolated_alpha.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )


