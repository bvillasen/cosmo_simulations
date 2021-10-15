import os, sys
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from mpl_toolkits.axes_grid1 import make_axes_locatable
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import load_analysis_data
from phase_diagram_functions import fit_thermal_parameters_mcmc, get_density_temperature_values_to_fit, get_phase_diagram_from_data
# from turbo_cmap import *
from figure_functions import *
from interpolation_functions import smooth_line

# sim_name = '1024_50Mpc'
sim_name = '2048_100Mpc'
input_dir = data_dir + f'cosmo_sims/rescaled_P19/{sim_name}/analysis_files/'
output_dir = data_dir + f'cosmo_sims/figures/paper_thermal_history/'
create_directory( output_dir )

data_all = {}

files = [ 45, 35 ]

for data_id, n_file in enumerate( files ):

  data = load_analysis_data( n_file, input_dir )
  z = data['cosmology']['current_z'] 
  data_pd = data['phase_diagram']
  phase_diagram = get_phase_diagram_from_data( data_pd )
  values_to_fit = get_density_temperature_values_to_fit( data['phase_diagram'], delta_min=-1.0, delta_max=1.0, n_samples_line=25, fraction_enclosed=0.68 )
  dens = values_to_fit['density']
  temp = values_to_fit['temperature']
  temp_sigma_p = values_to_fit['temperature_sigma_p']
  temp_sigma_m = values_to_fit['temperature_sigma_l']
  temp_error = np.array([ temp_sigma_m, temp_sigma_p ])
  fit_all = {}
  fit_all[0] = { 'xmin':-1, 'xmax':0, 'order':1 }
  fit_all[1] = { 'xmin':0,  'xmax':1, 'order':1 }
  fit_all[2] = { 'xmin':-1, 'xmax':1, 'order':1 }

  for index in fit_all.keys():
    fit = fit_all[index]
    xmin, xmax = fit['xmin'], fit['xmax']
    order = fit['order']
    indices_0 = ( dens >= xmin ) * ( dens <= xmax )
    fit_res =  np.polyfit( dens[indices_0], temp[indices_0], order   )[::-1]
    x_vals = np.linspace( xmin, xmax, 100 )
    y_vals = np.zeros_like( x_vals )
    # fit_res[0]*x_vals + fit_res[1]
    fit['fit_res'] = fit_res
    for i,coeff in enumerate( fit_res ):
      y_vals +=  coeff * x_vals**i
    fit['xvals'], fit['yvals'] = x_vals, y_vals
    # label = r'$T_0 \,= \, {0:.2f} \times 10^4$'.format( 10**fit_res[0]/ 10**4 ) + r' $\mathrm{K}$' + '\n' + r' $\,\gamma \, = \,{0:.2f} $'.format(  fit_res[1]+1) 
    label = r'$T_0 \,= \,$' + f'{10**fit_res[0]/ 10**4:.2f}' + r'$\times \mathregular{10^4}$ K' + '\n' + r' $\,\gamma \, = \,$' + f'{fit_res[1]+1:.2f}' 
    fit['label'] = label
      
  data_all[data_id] = { 'z':z, 'phase_diagram':phase_diagram, 'values_to_fit':values_to_fit, 'fit':fit_all }



text_color = 'black'
colormap =  'turbo'
fig_dpi = 300
alpha = 0.6
label_size = 16

figure_text_size = 18
legend_font_size = 16
tick_label_size_major = 12
tick_label_size_minor = 12
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.2
tick_width_minor = 1
border_width = 1

nrows, ncols = 2, 2
fig = plt.figure( figsize=(8*ncols,7*nrows))
n_grid_y, n_grid_x = 2, 15
split_x = 7
gs = plt.GridSpec(n_grid_y, n_grid_x)
gs.update(hspace=0.13, wspace=0.8, )
ax0 = plt.subplot(gs[0,0:split_x])
ax1 = plt.subplot(gs[0,split_x+1:])
ax2 = plt.subplot(gs[1,0:split_x])
ax3 = plt.subplot(gs[1,split_x+1:])
ax_l = [ [ax0, ax1], [ax2, ax3] ]

color_line = 'black'


matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"

prop_bold = matplotlib.font_manager.FontProperties( fname=os.path.join('/home/bruno/fonts/Helvetica', "Helvetica_bold.ttf"), size=20)
fig_labels_0 = [ 'a','b' ]
fig_labels_1 = [ 'c','d' ]



for index_j in range(2):
  
  if index_j == 0: fig_labels = fig_labels_0
  if index_j == 1: fig_labels = fig_labels_1
  ax = ax_l[ index_j][0]
  data_id = index_j
  data = data_all[data_id]
  z = data['z']
  pd_data = data['phase_diagram']
  fit_all = data['fit']
  fit = fit_all[2]



  T0, gamma = fit['fit_res'] 
  x_vals = np.linspace( -1, 1, 100 )
  y_vals = T0 + gamma*x_vals
  dens_points = pd_data['dens_points']
  temp_points = pd_data['temp_points']
  phase_1D    = pd_data['phase_1D'] 
  im = ax.scatter( dens_points, temp_points, c=phase_1D, s=0.1, alpha=alpha, cmap=colormap  )
  ax.plot( x_vals, y_vals, '--', lw=2, c=color_line )
  divider = make_axes_locatable(ax)
  cax = divider.append_axes('right', size='5%', pad=0.05)
  cbar = plt.colorbar(im, cax = cax, ticks=[-8, -4])

  cbar.set_label( r'$\log_{10}  \,\, f\,(\rho_{\,\mathrm{gas}}/\bar{\rho}\,, T\,) $', labelpad=7, fontsize=label_size, rotation=270 )
  cbar.ax.tick_params(labelsize=tick_label_size_major, size=tick_size_major, color=text_color, width=tick_width_major, length=tick_size_major, labelcolor=text_color, direction='in' )

  text  = fit['label'] 
  ax.text(0.59, 0.08, text, horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color)


  text  = r'$z =${0:.1f}'.format( z ) 
  ax.text(0.05, 0.95, text, horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color)


  ax.set_ylabel(r'$\log_{10} \, T$  [K]', fontsize=label_size , color=text_color)
  # ax.set_xlabel(r'$\log_{10} \, \Delta$ ', fontsize=label_size , color=text_color, labelpad=-5 )
  # ax.set_xlabel(r'$\log_{10} \, \Delta$ ', fontsize=label_size , color=text_color, )
  ax.set_xlabel(r'$\log_{10} \,( \,\rho_{\mathrm{gas}}/\bar{\rho} \,)$ ', fontsize=label_size , color=text_color )
  ax.set_xticks( [ -2, 0, 2, 4  ])
  ax.tick_params(axis='both', which='major', labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in')
  ax.tick_params(axis='both', which='minor', labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
  [sp.set_linewidth(border_width) for sp in ax.spines.values()]
  ax.set_xlim( -3, 5 )
  ax.set_ylim( 2.2, 8.3 )

  # fig_label_pos_x = 0.09
  # fig_label_pos_y = 0.76 - index_j * 0.405 + 0.1
  # fig.text( fig_label_pos_x, fig_label_pos_y,  fig_labels[0],  fontproperties=prop_bold )

  ax = ax_l[ index_j][1]
  values_to_fit = data['values_to_fit']
  delta = 10**values_to_fit['density']
  temp = 10**values_to_fit['temperature']
  temp_h = 10**( values_to_fit['temperature'] + values_to_fit['temperature_sigma_p'] )
  temp_l = 10**( values_to_fit['temperature'] - values_to_fit['temperature_sigma_l'] )
  temp_fit = 10**T0 * delta**gamma
  ax.plot( [-1,1], [0,0], '--', lw=2, color=color_line,  )
  color_band = 'C0'
  x = np.log10(delta)
  line = temp/temp_fit
  line_h = temp_h/temp_fit
  line_l = temp_l/temp_fit 
  n_neig, order = 5, 3 
  x, line = smooth_line( line, x, n_neig=n_neig, order=order )
  x, line_h = smooth_line( line_h, x, n_neig=n_neig, order=order )
  x, line_l = smooth_line( line_l, x, n_neig=n_neig, order=order )
   
  ax.plot( x, line -1 , color=color_band )
  ax.fill_between( x, line_h -1, line_l -1, color=color_band, alpha=0.5 )
  ax.set_xlim( -1, 1 )
  ax.set_ylim( -0.2, 0.4 )

  ax.set_ylabel(r'$\Delta T / T $', fontsize=label_size , color=text_color , labelpad=-3)
  ax.set_xlabel(r'$\log_{10} \,( \,\rho_{\mathrm{gas}}/\bar{\rho} \,)$ ', fontsize=label_size , color=text_color )
  ax.set_xticks( [ -1.0, -0.5,  0., 0.5, 1.0  ])

  # fig_label_pos_x = 0.09 + 0.42
  # fig_label_pos_y = 0.76 - index_j * 0.405 + 0.1
  # fig.text( fig_label_pos_x, fig_label_pos_y,  fig_labels[1],  fontproperties=prop_bold )


  text  = r'$z =${0:.1f}'.format( z ) 
  ax.text(0.05, 0.95, text, horizontalalignment='left',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color=text_color)



 


file_name = output_dir + f'phase_diagram_new.png'
fig.savefig( file_name,  pad_inches=0.1, bbox_inches='tight', dpi=fig_dpi, facecolor=fig.get_facecolor() )
print('Saved Image: ', file_name )




