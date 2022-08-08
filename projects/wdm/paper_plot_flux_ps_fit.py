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
from stats_functions import compute_distribution, get_highest_probability_interval
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid
from load_tabulated_data import load_data_boera
from matrix_functions import Merge_Matrices


ps_data_dir = cosmo_dir + 'lya_statistics/data/'
base_dir = data_dir + 'cosmo_sims/sim_grid/'

proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + 'figures/'
create_directory( output_dir )

dir_data_boera = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_data_boera( dir_data_boera )

error_type = 'covmatrix'
grid_names = [ '1024_wdmgrid_extended_beta', '1024_wdmgrid_cdm_extended_beta' ] 
data_name = f'fit_results_P(k)+_Boera_{error_type}'
data_labels = [ 'Boera Sigma', 'Boera Cov M' ]

HL_key = 'Highest_Likelihood'
# HL_key = 'mean'
# HL_key = 'max'
print( f'HL key: {HL_key}')

line_colors = [ 'C0', 'C1', 'C2' ]

sim_labels = [ 'Best Fit', 'Best Fit CDM', ]
 
data_all = {} 
for data_id, grid_name in enumerate(grid_names):
  input_dir = base_dir + f'{grid_name}/fit_mcmc/{data_name}/observable_samples/'
  file_name = input_dir + 'samples_power_spectrum.pkl'
  data = Load_Pickle_Directory( file_name )
  data_sim = {}
  for snap_id in data:
    data_snap = data[snap_id]
    z = data_snap['z']
    k_vals = data_snap['k_vals']
    ps_mean = data_snap['mean'] 
    ps_HL = data_snap['Highest_Likelihood'] 
    ps_max = data_snap['max'] 
    ps_h = data_snap['higher']
    ps_l = data_snap['lower']
    data_sim[snap_id] = { 'z':z, 'k_vals':k_vals, 'Highest_Likelihood':ps_HL, 'mean':ps_mean, 'max':ps_max, 'higher':ps_h, 'lower':ps_l } 
  data_sim['z_vals'] = np.array([ data_sim[i]['z'] for i in data_sim ])
  data_all[data_id] = data_sim
  data_all[data_id]['label'] = data_labels[data_id]
  data_all[data_id]['line_color'] = line_colors[data_id]

  
data_all[0]['line_color'] = ocean_green

cool_orange = '#EF8354'
cream = '#ffbb6c'
mint_green = '#81B29A'
dark_blue = '#4f6a8f'
dark_purple = '#443850'
data_label = 'Boera et al. (2019)'
data_color =  ocean_green
data_color =  'dodgerblue'

# sim_colors = [ 'seagreen', 'slateblue' ]
# sim_colors = [ 'seagreen', 'royalblue' ]

sim_colors = [ 'dodgerblue', yellows[3] ]

sim_colors = [ 'midnightblue', 'orange' ]

import matplotlib
import matplotlib.font_manager
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

fig_width = 3 * figure_width
fig_height = 1.* figure_width
nrows = 2
ncols = 3
h_length = 4
main_length = 3

fig_dpi = 300
label_size = 22
figure_text_size = 18
legend_font_size = 18
tick_label_size_major = 18
tick_label_size_minor = 14
tick_size_major = 8
tick_size_minor = 6
tick_width_major = 2.5
tick_width_minor = 2
border_width = 2
text_color = 'k'

linewidth = 2
bars_alpha = [ 0.7, 0.5 ]

fig = plt.figure(0)
fig.set_size_inches(fig_width, fig_height )
fig.clf()

gs = plt.GridSpec(h_length, ncols)
gs.update(hspace=0.0, wspace=0.18, )


xmin, xmax = 0.0045, 0.25
y_lims = [ [6e-3, 4e-1], [9e-3, 5.5e-1], [1.5e-2, 7.5e-1] ]
delta_ylims = [ [-0.4, 0.7], [-0.3, 0.35], [-0.3, 0.5 ] ]
delta_ticks = [ [0.0, 0.5], [-.2, 0, .2], [0.0, 0.4]]
sim_reff_indx = 0 

sim_factor  = [ 1.03, 1.03, 1.02 ]


sum_matrix = { 0:{'ps':[]}, 1:{'ps':[]}, 'data':{'ps':[], 'covmatrix':[]} }
  

 

for i in range( ncols ):
  
  ax1 = plt.subplot(gs[0:main_length, i])
  ax2 = plt.subplot(gs[main_length:h_length, i])
  
  data = data_boera[i]
  z = data['z']
  data_k = data['k_vals']
  data_ps = data['delta_power']
  data_ps_sigma = data['delta_power_error']
  data_covmatrix = data['covariance_matrix']
  ps_d = data_ps / data_k * np.pi
  sum_matrix['data']['ps'].append(ps_d)
  sum_matrix['data']['covmatrix'].append(data_covmatrix)
  ax1.errorbar( data_k, data_ps, yerr=data_ps_sigma, fmt='o', c=data_color, label=data_label, zorder=3)
  
  for data_id in data_all:
    factor = sim_factor[i]
    # factor = 1.0
    data_sim = data_all[data_id][i]
    z_sim = data_sim['z'] 
    k_sim = data_sim['k_vals']
    ps_sim = data_sim[HL_key]     
    ps_sim_h = data_sim['higher'] 
    ps_sim_l = data_sim['lower']  
    if data_id == sim_reff_indx:
      ps_sim   *= factor
      ps_sim_h *= factor
      ps_sim_l *= factor 
    line_color = sim_colors[data_id]
    line_alpha = 1.0
    bar_alpha = bars_alpha[data_id] 
    ax1.plot( k_sim, ps_sim ,linewidth=linewidth,  zorder=2, color=line_color, alpha=line_alpha, label=sim_labels[data_id] )
    ax1.fill_between( k_sim, ps_sim_h, ps_sim_l, color=line_color, alpha=bar_alpha,  zorder=1 )
    
    
    data_sim_reff = data_all[sim_reff_indx][i]
    k_reff = data_sim_reff['k_vals']
    ps_reff = data_sim_reff[HL_key] 
    delta_ps = ( ps_sim - ps_reff ) / ps_reff
    delta_h = ( ps_sim_h - ps_reff ) / ps_reff
    delta_l = ( ps_sim_l - ps_reff ) / ps_reff
    
    ax2.plot( k_sim, delta_ps ,linewidth=linewidth,  zorder=2, color=line_color, alpha=line_alpha )
    ax2.fill_between( k_sim, delta_h, delta_l, color=line_color, alpha=bar_alpha, zorder=1)
    
    sim_ps_interp = 10**np.interp( np.log10(data_k), np.log10(k_sim), np.log10(ps_sim) ) 
    delta_ps_data = ( data_ps - sim_ps_interp ) / sim_ps_interp
    delta_ps_data_h = ( data_ps_sigma ) / sim_ps_interp
    delta_ps_data_l = ( data_ps_sigma ) / sim_ps_interp
    delta_sigma = [ delta_ps_data_h, delta_ps_data_l]
    
    
    ps_s = sim_ps_interp / data_k * np.pi
    if data_id == sim_reff_indx: ps_s /= factor 
    sum_matrix[data_id]['ps'].append(ps_s.copy())
    
    if data_id == sim_reff_indx:  ax2.errorbar( data_k, delta_ps_data, yerr=delta_sigma, fmt='o', c=data_color, label=data_label, zorder=3)
    
  
  ps_data_vector = np.concatenate( sum_matrix['data']['ps'] )
  ps_sim_vector_0 = np.concatenate( sum_matrix[0]['ps'] )
  ps_sim_vector_1 = np.concatenate( sum_matrix[1]['ps'] )  
  cov_matrix = Merge_Matrices( sum_matrix['data']['covmatrix'])
  cov_matrix_inv = np.linalg.inv( cov_matrix )
  
  if i == 0:   leg = ax1.legend(  loc=3, frameon=False, fontsize=legend_font_size    )
  
  
    
  
  ax1.text(0.89, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax1.transAxes, fontsize=figure_text_size, color=text_color) 

  ax1.set_ylabel( r'$\pi^{\mathregular{-1}} \,k \,P\,(k)$', fontsize=label_size, color= text_color )  
  ax1.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
  ax1.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
  ax1.set_xscale('log')
  ax1.set_yscale('log')
  [sp.set_linewidth(border_width) for sp in ax1.spines.values()]
  ax1.set_xlim( xmin, xmax )
  ax1.set_ylim( y_lims[i][0], y_lims[i][1] )
  

  ax2.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
  ax2.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
  ax2.set_ylabel( r'$ \Delta P\,(k) / P\,(k)$', fontsize=label_size, color= text_color )  
  ax2.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=label_size, color=text_color, labelpad=-5 )
  ax2.set_xscale('log')
  [sp.set_linewidth(border_width) for sp in ax2.spines.values()]
  ax2.set_xlim( xmin, xmax )
  ax2.set_ylim( delta_ylims[i][0], delta_ylims[i][1] )
  ax2.set_yticks( delta_ticks[i] )

delta_vector_0 = ps_sim_vector_0 - ps_data_vector
delta_vector_1 = ps_sim_vector_1 - ps_data_vector

mult_partial = np.matmul( delta_vector_0.T, cov_matrix_inv )
M_0 = np.matmul( mult_partial, delta_vector_0)

mult_partial = np.matmul( delta_vector_1.T, cov_matrix_inv )
M_1 = np.matmul( mult_partial, delta_vector_1)
N = len( delta_vector_0 )
ln_L_0 = -0.5 * M_0 - 0.5 * np.log( np.linalg.det(cov_matrix)) - N/2*np.log(2*np.pi)
ln_L_1 = -0.5 * M_1 - 0.5 * np.log( np.linalg.det(cov_matrix)) - N/2*np.log(2*np.pi)  

L0 = np.exp( ln_L_0 )
L1 = np.exp( ln_L_1 )

ax1 = plt.subplot(gs[0:main_length, 0])

M_vals = [ M_0, M_1 ]
pos_x = 0.66
for data_id in data_all:
  txt = r'$\chi^2=\Delta^{T} \mathbf{C}^{-1} \Delta=$' + f'{M_vals[data_id]:.1f}'
  pos_y = 0.24 - 0.075*data_id
  ax1.text(pos_x, pos_y, txt, horizontalalignment='center',  verticalalignment='center', transform=ax1.transAxes, fontsize=legend_font_size-1, color=sim_colors[data_id]) 
  
fig.align_ylabels()
  
figure_name = output_dir + f'flux_ps_wdm_fit.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
















