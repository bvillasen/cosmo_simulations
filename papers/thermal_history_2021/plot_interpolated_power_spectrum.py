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

black_background = True


base_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
input_dir = base_dir + 'interpolated_observables/'
output_dir = data_dir + 'cosmo_sims/figures/paper_thermal_history/'
if black_background: output_dir += 'black_background/'
create_directory( output_dir )

in_file_name = input_dir + 'interpolated_observables.pkl'
ps_data = Load_Pickle_Directory( in_file_name )['power_spectrum']

z_vals = ps_data['z_vals']
params = ps_data['params']

k_max = 2e-1
n_to_plot = 4
indices_to_plot = { 0:[1,2,3,4], 1:[0,1,2,3,], 2:[0,1,2,3,], 3:[1,2,3,4] }
vary_params = [ 'scale_He', 'scale_H', 'deltaZ_He', 'deltaZ_H' ]



# for z in z_vals:
z_to_plot =  [ 3.0, 4.0 ] 


ps_plot = {}

for id_z,z in enumerate(z_to_plot): 
  z_index = np.where( z_vals == z )[0][0]
  ps_redshift = {}
  for param_indx, vary_param in enumerate(vary_params):
    ps_redshift[param_indx] = { 'param_name': vary_param }
    ps_param = ps_data[vary_param]
    for i,indx in enumerate(indices_to_plot[param_indx]):
      ps_redshift[param_indx][i] = { 'k_vals':ps_param[indx]['ps'][z_index]['k_vals'], 'ps':ps_param[indx]['ps'][z_index]['mean'], 'p_val':ps_param[indx]['params'][param_indx] }
  ps_plot[id_z] = ps_redshift

labels = {'scale_He':' \\beta_{\mathrm{He}}', 'scale_H':' \\beta_{\mathrm{H}}', 'deltaZ_He':'\Delta z _{\mathrm{He}}', 'deltaZ_H':'\Delta z _{\mathrm{H}}' }


# fig_width = 3.5
fig_width = 4.5
fig_dpi = 300
label_size = 18
figure_text_size = 18
legend_font_size = 16
tick_label_size_major = 14
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
border_width = 1
text_color  = 'black'
linewidth = 2
alpha_bar = 0.5


text_color  = 'black'
colors = [ sky_blue, ocean_green, ocean_blue, dark_purple  ] 

blue = blues[4]
yellow = yellows[1]
orange = yellows[4]
if black_background:  
  text_color = 'white'
  
  # colors = [ yellow,  light_orange, light_green, blue  ] 
  colors = [ yellow,  orange, light_green, sky_blue  ] 
  border_width = 1.5
  label_size = 22
  legend_font_size = 18
  tick_label_size_major = 16
  tick_size_major = 6
  tick_size_minor = 4
  

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"

plot_order = [1, 3, 0, 2 ]

nrows, ncols = len(z_to_plot), 4
prop = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica.ttf"), size=legend_font_size)
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.02, wspace=0.02)

for indx_i in range(nrows):
  for indx_j in range(ncols):

    id = indx_i*ncols + indx_j

    if nrows == 1: ax = ax_l[indx_j]
    else:  ax = ax_l[indx_i][indx_j]
    
    id_z = indx_i
    ps_redshift = ps_plot[id_z]
    
    plot_id = plot_order[indx_j]
    ps_param = ps_redshift[plot_id]
    param_name = ps_param['param_name']
    for i in range(n_to_plot):
      ps_d = ps_param[i]
      k_vals = ps_d['k_vals']
      indices = k_vals < k_max
      k_vals = k_vals[indices]
      ps = ps_d['ps'][indices]
      p_val = ps_d['p_val']
      label_param = labels[param_name]
      color = colors[i]
      label = r'${0}  = ${1:.1f}'.format(label_param, p_val)
      ax.plot( k_vals, ps, linewidth=1.5, label=label, color=colors[i] )


    legend_loc = 3
    leg = ax.legend(  loc=legend_loc, frameon=False, prop=prop, fontsize=legend_font_size    )
    for text in leg.get_texts():
      plt.setp(text, color = text_color)
    # [ text.set_color(text_color) for text in leg.get_texts() ] 
      
    z = z_to_plot[indx_i]
    ax.text(0.87, 0.95, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color) 

    ax.set_xscale('log')
    ax.set_yscale('log')

    if indx_j > 0:ax.set_yticklabels([])
    if indx_i != nrows-1 :ax.set_xticklabels([])

    ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in', color=text_color, labelcolor=text_color )
    ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in', color=text_color, labelcolor=text_color)

    if indx_j == 0: ax.set_ylabel( r'$\pi^{\mathregular{-1}} \,k \,P\,(k)$', fontsize=label_size, color= text_color )
    # if indx_i == nrows-1: ax.set_xlabel( r'$ k   \,\,\,  [\mathrm{s}\,\mathrm{km}^{-1}] $',  fontsize=label_size, color= text_color )
    ax.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size, color=text_color )

    x_min, x_max = 2e-3, 1e-1
    if indx_i == 0: y_min, y_max = 1e-2, 1.01e-1
    if indx_i == 1: y_min, y_max = 3e-2, 3.01e-1
    if indx_i == 2: y_min, y_max = 3e-2, 4.01e-1
    ax.set_xlim( x_min, x_max )
    ax.set_ylim( y_min, y_max )

  
    [sp.set_linewidth(border_width) for sp in ax.spines.values()]
    
    if black_background: 
      fig.patch.set_facecolor('black') 
      ax.set_facecolor('k')
      [ spine.set_edgecolor(text_color) for spine in list(ax.spines.values()) ]



file_name = output_dir + f'power_spectrum_parameters.png'
fig.savefig( file_name,  pad_inches=0.1, bbox_inches='tight', dpi=fig_dpi, facecolor=fig.get_facecolor() )
print('Saved Image: ', file_name )



