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
sys.path.append( cosmo_dir + 'lya_statistics/data' )
from tools import *
from data_optical_depth import *
from colors import * 
from stats_functions import compute_distribution, get_highest_probability_interval
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid
from load_tabulated_data import load_data_boera



root_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_resolution/'
output_dir = root_dir + 'figures/'
create_directory( output_dir ) 

sim_names = [ '1024_50Mpc', '1024_40Mpc', '1024_30Mpc', '1024_25Mpc', '1024_20Mpc', ]

n_models = 5
n_files = 36

data_ps = {}
for model_id in range(n_models):
  input_dir = root_dir + f'{sim_names[model_id]}/analysis_files/'
  data_sim = {}
  factor = 1.1
  for n_file in range(n_files):
    file_name = input_dir + f'{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    ps_data = file['lya_statistics']['power_spectrum']
    k_vals  = ps_data['k_vals'][...]
    ps_mean = ps_data['p(k)'][...] * factor
    indices = ps_mean > 0
    delta_ps = ps_mean * k_vals / np.pi
    k_vals = k_vals[indices]
    delta_ps = delta_ps[indices]
    data_sim[n_file] = { 'z':z, 'k_vals':k_vals, 'ps_mean':delta_ps } 
  data_sim['z_vals'] = np.array([ data_sim[i]['z'] for i in data_sim ])
  data_ps[model_id] = data_sim


ps_data_dir= 'data/'
dir_data_boera = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_data_boera( dir_data_boera )


from figure_functions import *
figure_text_size = 14
legend_font_size = 9
text_color = 'black'
figure_width = 8
fig_width = 2 * figure_width
fig_height = 0.6 * figure_width
nrows = 2
ncols = 3
h_length = 4
main_length = 3

fig = plt.figure(0)
fig.set_size_inches(fig_width, fig_height )
fig.clf()

gs = plt.GridSpec(h_length, ncols)
gs.update(hspace=0.0, wspace=0.18, )

x_min, x_max = 2e-3, 4e-1
y_min, y_max = 5e-3, 1.2e0

z_vals = [ 4.2, 4.6, 5.0 ] 

c_boera = dark_green

colors = [ 'C0', 'C2', 'C4', 'C1', 'C3' ]
box_sizes = [ 50., 40., 30., 25., 20. ]
line_styles = [ '--', '--', '--', '--', '-', ]

ref_id = 4

for i in range(3):
  ax1 = plt.subplot(gs[0:main_length, i])
  ax2 = plt.subplot(gs[main_length:h_length, i])


  current_z = z_vals[i]


  ax1.text(0.85, 0.93, r'$z=${0:.1f}'.format(current_z), horizontalalignment='center',  verticalalignment='center', transform=ax1.transAxes, fontsize=figure_text_size, color=text_color) 


  for model_id in range(n_models):
    sim_data = data_ps[model_id]
    sim_z = sim_data['z_vals']
    z_diff = np.abs( sim_z - current_z )
    diff_min = z_diff.min()
    print( f'Model ID: {model_id}' )
    if diff_min < 1e-1:
      snap_index = np.where( z_diff == diff_min )[0][0]
      snap_data = sim_data[snap_index]
      k_vals  = snap_data['k_vals']
      ps_mean = snap_data['ps_mean']
      color = colors[model_id]
      ls = line_styles[model_id]
      box_size = box_sizes[model_id]
      resolution = box_size / 1024. * 1000
      label = r'$\Delta x =$' + f' {resolution:.1f} ' + r'$h^{-1}\mathrm{kpc}$'
      label += r'  $L =$' + f' {box_size:.0f} ' + r'$h^{-1}\mathrm{Mpc}$'
      ax1.plot( k_vals, ps_mean, c=color, ls=ls, label=label )

      ps_ref = data_ps[ref_id][snap_index]['ps_mean'].copy()
      k_ref  = data_ps[ref_id][snap_index]['k_vals'].copy()
      k_l = max( k_ref.min(), k_vals.min() )
      k_r = min( k_ref.max(), k_vals.max() )
      print( k_l, k_r )
      k_indices = ( k_ref >= k_l ) * ( k_ref <= k_r )
      print( len(k_indices), len(k_ref ))
      k_ref = k_ref[k_indices]
      ps_ref = ps_ref[k_indices]
      ps_interp = np.interp( k_ref, k_vals, ps_mean )
      
      
      ps_diff = ( ps_interp - ps_ref ) / ps_ref 
      ax2.plot( k_ref, ps_diff, c=color, ls=ls  )
      
      


  # Add Boera data
  data_z = data_boera['z_vals']
  z_diff = np.abs( data_z - current_z )
  diff_min = z_diff.min()
  if diff_min < 1e-1:
    data_index = np.where( z_diff == diff_min )[0][0]
    data_z_local = data_z[data_index]
    data_k = data_boera[data_index]['k_vals']
    data_delta_power = data_boera[data_index]['delta_power']
    data_delta_power_error = data_boera[data_index]['delta_power_error']
    label_boera ='Boera et al. (2019)'
    d_boera = ax1.errorbar( data_k, data_delta_power, yerr=data_delta_power_error, fmt='o', c=c_boera, label=label_boera, zorder=2 )




  ax1.set_ylabel( r'$\pi^{\mathregular{-1}} \,k \,P\,(k)$', fontsize=label_size, color=text_color, labelpad=0)
  ax1.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax1.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
  [sp.set_linewidth(border_width) for sp in ax1.spines.values()]  

  ax2.set_ylabel( r'$\Delta P\,(k) / P\,(k)$', fontsize=label_size, color=text_color, labelpad=0)
  ax2.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size, color=text_color, labelpad=0)
  ax2.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax2.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
  [sp.set_linewidth(border_width) for sp in ax2.spines.values()]  

  ax1.set_xlim( x_min, x_max )
  ax1.set_ylim( y_min, y_max )
  ax1.set_xscale('log')
  ax1.set_yscale('log')
  ax2.set_xscale('log')

  ax2.set_xlim( x_min, x_max )
  ax2.set_ylim( -.3, .3 )

  leg = ax1.legend(  loc=3, frameon=False, fontsize=legend_font_size    )


figure_name = output_dir + 'flux_ps_resolution.png'

fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )



