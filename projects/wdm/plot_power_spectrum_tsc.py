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


base_dir = data_dir + 'cosmo_sims/wdm_sims/tsc/'
proj_dir = data_dir + 'projects/wdm/'

sim_names = [ 'cdm', 'm_4.0kev' ]
data_type = 'particles'
snap_id = 0

base_input_dir = proj_dir + 'data/input_wdm_power_spectrum_music/'
data_input = {}
for i,sim_name in enumerate(sim_names):
  input_dir = base_input_dir + f'{sim_name}/'
  in_file_name = input_dir + 'input_powerspec.txt'
  data = np.loadtxt( in_file_name )
  k, P_cdm, P_vcdm, P_total = data.T
  data_input[i] = { 'k':k, 'P_cdm':P_cdm, 'P_vcdm':P_vcdm, 'P_total':P_total  }

input_k = data_input[0]['k']
input_cdm = data_input[0]['P_total']
input_wdm = data_input[1]['P_total']
input_ratio = data_input[1]['P_total'] / data_input[0]['P_total']    



output_dir = proj_dir + 'figures/pk_tsc/'
create_directory( output_dir )

n_points = 1024
sim_base_name = f'{n_points}_25Mpc'
sim_names  = [ 'cdm', 'm4.0kev' ]
data_types = [ 'particles', 'hydro' ]
density_types = [ 'cic', 'tsc' ]

snapshots = [ 0, 2, 3, 4, 5 ]
n_snapshots = len( snapshots )

pk_data_all = {} 
for sim_name in sim_names:
  pk_data_all[sim_name] = {}
  for data_type in data_types:
    pk_data_all[sim_name][data_type] = {}
    for density_type in density_types:
      pk_data_all[sim_name][data_type][density_type] = {}
      for snap_id in snapshots:
        file_name = base_dir + f'{sim_base_name}_{sim_name}/{density_type}/power_spectrum_files/power_spectrum_{data_type}_{snap_id}.pkl'
        data = Load_Pickle_Directory( file_name )
        pk_data_all[sim_name][data_type][density_type][snap_id] = data




import matplotlib
import matplotlib.font_manager
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

fig_width = 2 * figure_width
fig_height = 1.* figure_width
nrows = 2
ncols = 2
h_length = 4
main_length = 3

label_size = 18
figure_text_size = 18
legend_font_size = 13
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 6
tick_size_minor = 4
tick_width_major = 2
tick_width_minor = 1.5
border_width = 1.5
text_color = 'black'
linewidth = 2
bars_alpha = [ 0.7, 0.5 ]


font_size = 16
legend_font_size = 12

label_size = 18
figure_text_size = 18
legend_font_size = 12
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
border_width = 1
text_color = 'k'

fig = plt.figure(0)
fig.set_size_inches(fig_width, fig_height )
fig.clf()

gs = plt.GridSpec(h_length, ncols)
gs.update(hspace=0.0, wspace=0.18, )


xmin, xmax = 0.2, 300
ymin, ymax = 1e-5, 1e12

for i in range(2):
  if i == 0: data = data_type = 'particles'
  if i == 1: data = data_type = 'hydro'

  ax1 = plt.subplot(gs[0:main_length, i])
  ax2 = plt.subplot(gs[main_length:h_length, i])

  ax2.axhline( y=1, ls='--', c='red')

  colors = [ 'C0', 'C1', 'C2', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9' ]
  
  density_type = 'tsc'  
  # density_type = 'cic'

  for id in range(n_snapshots):
    snap_id = snapshots[n_snapshots - id - 1]
    data_cdm_cic = pk_data_all['cdm'][data_type]['cic'][snap_id]
    data_cdm_tsc = pk_data_all['cdm'][data_type]['tsc'][snap_id]
    data_wdm_cic = pk_data_all['m4.0kev'][data_type]['cic'][snap_id]
    data_wdm_tsc = pk_data_all['m4.0kev'][data_type]['tsc'][snap_id]
    z = data_cdm_cic['z']
    k_vals = data_cdm_cic['k_vals']
    pk_cdm_cic = data_cdm_cic['power_spectrum']
    pk_cdm_tsc = data_cdm_tsc['power_spectrum']
    pk_wdm_cic = data_wdm_cic['power_spectrum']
    pk_wdm_tsc = data_wdm_tsc['power_spectrum']
    pk_diff_cic = pk_wdm_cic / pk_cdm_cic
    
    if density_type == 'cic':
      pk_cdm = pk_cdm_cic
      pk_wdm = pk_wdm_cic
    
    if density_type == 'tsc':
      pk_cdm = pk_cdm_tsc
      pk_wdm = pk_wdm_tsc
    
    
    pk_diff = pk_wdm / pk_cdm
    
        
    label = r'$z = {0:.1f}$'.format( z )
    c = colors[snap_id]
    ax1.plot( k_vals, pk_cdm, label=label, c=c )
    ax1.plot( k_vals, pk_wdm, ls='--', c=c )
    ax2.plot( k_vals, pk_diff, c=c )
    
    if np.abs(z-100) < 1e-1:
      input_factor = 1.2e12
      ratio_interp = np.interp( k_vals, input_k, input_ratio )
      ax1.plot( input_k, input_cdm*input_factor, label='input CDM', ls='dotted', c='k' )
      ax1.plot( input_k, input_wdm*input_factor, label='input WDM 4.0kev', ls='dotted', c='k' )
      ax2.plot( k_vals, ratio_interp, label='', ls='dotted', c='k' )  
    

  diff_log =True

  ax1.legend( loc=3, fontsize=14, frameon=False )
  ax1.set_xscale('log')
  ax1.set_yscale('log')
  ax2.set_xscale('log')
  if diff_log: ax2.set_yscale('log')
  
  ax1.set_xlim( xmin, xmax )
  ax1.set_ylim( ymin, ymax )

  if i==0:ax1.set_ylabel( r'$P_\mathrm{DM}(k) $', fontsize=font_size, color=text_color  )
  if i==0:ax2.set_ylabel( r'$P_\mathrm{DM}(k) \, / \, P_\mathrm{DM,CDM}(k)$', fontsize=font_size, color=text_color  )
  if i==1:ax1.set_ylabel( r'$P_\mathrm{gas}(k) $', fontsize=font_size, color=text_color  )
  if i==1:ax2.set_ylabel( r'$P_\mathrm{gas}(k) \, / \, P_\mathrm{gas,CDM}(k)$', fontsize=font_size, color=text_color  )
  ax2.set_xlabel( r'$k$  [$h$ Mpc$^{\mathrm{\mathregular{-1}}}$]', fontsize=font_size, color=text_color )

  ax1.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax1.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )  
  ax2.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax2.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )

figure_name = output_dir + f'ps_{density_type}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )







