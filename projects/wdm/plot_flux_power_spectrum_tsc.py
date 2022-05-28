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

Omega_M = 0.3111
Omega_L = 1 - Omega_M
H0 = 67.66
h = H0 / 100

def get_hubble( z, H0, Omega_M, Omega_L ):
  a = 1 / ( z + 1 )
  H = H0 * np.sqrt( Omega_M/a**3 + Omega_L )
  return H 


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

snapshots = [ 6, 7, 8 ]
n_snapshots = len( snapshots )

pk_data_all = {} 
for sim_name in sim_names:
  pk_data_all[sim_name] = {}
  for data_type in data_types:
    pk_data_all[sim_name][data_type] = {}
    for density_type in density_types:
      pk_data_all[sim_name][data_type][density_type] = {}
      for snap_id, n_snap in enumerate(snapshots):
        file_name = base_dir + f'{sim_base_name}_{sim_name}/{density_type}/power_spectrum_files/power_spectrum_{data_type}_{n_snap}.pkl'
        data = Load_Pickle_Directory( file_name )
        pk_data_all[sim_name][data_type][density_type][snap_id] = data



flux_pk_data_all = {}
flux_snapshots = [ 25, 29, 33 ]
for sim_name in sim_names:
  flux_pk_data_all[sim_name] = {}
  for density_type in density_types:
    flux_pk_data_all[sim_name][density_type] = {}
    for snap_id, n_snap in enumerate(flux_snapshots):
      file_name = base_dir + f'{sim_base_name}_{sim_name}/{density_type}/analysis_files/{n_snap}_analysis.h5'
      print( f'Loading File: {file_name}')
      file = h5.File( file_name, 'r' )
      z = file.attrs['current_z'][...][0]
      pk = file['lya_statistics']['power_spectrum']['p(k)'][...]
      k  = file['lya_statistics']['power_spectrum']['k_vals'][...]
      file.close()
      indices = pk > 0
      pk = pk[indices]
      k  = k[indices]
      pk = pk * k / np.pi
      flux_pk_data_all[sim_name][density_type][snap_id] = { 'z':z, 'k':k, 'pk':pk }
      
        




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

snap_id = 2

c_cic = 'C0'
c_tsc = 'C1'

for i in range(3):

  ax1 = plt.subplot(gs[0:main_length, i])
  ax2 = plt.subplot(gs[main_length:h_length, i])
  ax2.axhline( y=1, ls='--', c='red')
  
  if i in [0, 1]:
    if i == 0: data = data_type = 'particles'
    if i == 1: data = data_type = 'hydro'
    



    colors = [ 'C0', 'C1', 'C2', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9' ]

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
    pk_diff_tsc = pk_wdm_tsc / pk_cdm_tsc


    label = ''
    c = colors[snap_id]
    ax1.plot( k_vals, pk_cdm_cic, label="CIC", c=c_cic )
    ax1.plot( k_vals, pk_wdm_cic, ls='--', c=c_cic )
    ax2.plot( k_vals, pk_diff_cic, c=c_cic )

    ax1.plot( k_vals, pk_cdm_tsc, label="TSC", c=c_tsc )
    ax1.plot( k_vals, pk_wdm_tsc, ls='--', c=c_tsc )
    ax2.plot( k_vals, pk_diff_tsc, c=c_tsc )
    
    k_min, k_max = 10**-2.2, 10**-0.7
    H = get_hubble( z, H0, Omega_M, Omega_L)
    v_max = 2*np.pi /k_min
    v_min = 2*np.pi /k_max
    
    y_min = pk_wdm_tsc.min() * 0.6
    y_max = pk_wdm_tsc.max() * 1.4 
    ax1.set_ylim( y_min, y_max)
    
    y_min = pk_diff_tsc.min() * 0.9
    y_max = pk_diff_tsc.max() * 1.1
    ax2.set_ylim( y_min, y_max)
    
    
    lambda_max = 1 / H * v_max * ( 1 + z ) * h
    lambda_min = 1 / H * v_min * ( 1 + z ) * h
    kc_min = 2 * np.pi / lambda_max
    kc_max = 2 * np.pi / lambda_min       
    ax1.fill_between( [kc_min, kc_max], [-1, -1 ], [1e13, 1e13], color='gray', alpha=0.3 )
    ax2.fill_between( [kc_min, kc_max], [-1, -1 ], [1e13, 1e13], color='gray', alpha=0.3 )
    
    
    # ax1.set_xlim( xmin, xmax )
    # ax1.set_ylim( ymin, ymax )

    if i==0:ax1.set_ylabel( r'$P_\mathrm{DM}(k) $', fontsize=font_size, color=text_color  )
    if i==0:ax2.set_ylabel( r'$P_\mathrm{DM}(k) \, / \, P_\mathrm{DM,CDM}(k)$', fontsize=font_size, color=text_color  )
    if i==1:ax1.set_ylabel( r'$P_\mathrm{gas}(k) $', fontsize=font_size, color=text_color  )
    if i==1:ax2.set_ylabel( r'$P_\mathrm{gas}(k) \, / \, P_\mathrm{gas,CDM}(k)$', fontsize=font_size, color=text_color  )
    ax2.set_xlabel( r'$k$  [$h$ Mpc$^{\mathrm{\mathregular{-1}}}$]', fontsize=font_size, color=text_color )
  
  if i == 2:
    
    data_cdm_cic = flux_pk_data_all['cdm']['cic'][snap_id]
    data_cdm_tsc = flux_pk_data_all['cdm']['tsc'][snap_id]
    data_wdm_cic = flux_pk_data_all['m4.0kev']['cic'][snap_id]
    data_wdm_tsc = flux_pk_data_all['m4.0kev']['tsc'][snap_id]
    z = data_cdm_cic['z']
    k_vals = data_cdm_cic['k']
    pk_cdm_cic = data_cdm_cic['pk']
    pk_cdm_tsc = data_cdm_tsc['pk']
    pk_wdm_cic = data_wdm_cic['pk']
    pk_wdm_tsc = data_wdm_tsc['pk']
    pk_diff_cic = pk_wdm_cic / pk_cdm_cic
    pk_diff_tsc = pk_wdm_tsc / pk_cdm_tsc
    
    pk_diff = pk_wdm_tsc / pk_cdm_cic
    
    c = colors[snap_id]
    ax1.plot( k_vals, pk_cdm_cic, label="CIC", c=c_cic )
    ax1.plot( k_vals, pk_wdm_cic, ls='--', c=c_cic )
    ax2.plot( k_vals, pk_diff_cic, c=c_cic )

    ax1.plot( k_vals, pk_cdm_tsc, label="TSC", c=c_tsc )
    ax1.plot( k_vals, pk_wdm_tsc, ls='--', c=c_tsc )
    ax2.plot( k_vals, pk_diff_tsc, c=c_tsc )
    
    ax2.plot( k_vals, pk_diff, label='WDM (TSC) / CDM (CIC)', c='C2', ls='--' )
    
    
    ax2.legend( loc=2, fontsize=14, frameon=False )
    
    y_min = pk_wdm_cic.min() * 0.6
    y_max = pk_wdm_cic.max() * 1.4 
    ax1.set_ylim( y_min, y_max)
    
    y_min = pk_diff_cic.min() * 0.9
    y_max = pk_diff_cic.max() * 1.1 
    ax2.set_ylim( y_min, y_max)

    ax1.fill_between( [k_min, k_max], [-1, -1 ], [1000, 1000], color='gray', alpha=0.3 )
    ax2.fill_between( [k_min, k_max], [-1, -1 ], [1000, 1000], color='gray', alpha=0.3 )
   
    ax1.set_ylabel( r'$ \pi^{-1}\, k \, P_\mathrm{flux}(k) $', fontsize=font_size, color=text_color  )
    ax2.set_ylabel( r'$P_\mathrm{flux}(k) \, / \, P_\mathrm{flux,CDM}(k)$', fontsize=font_size, color=text_color  )
    ax2.set_xlabel( r'$k$  [s km$^{\mathrm{\mathregular{-1}}}$]', fontsize=font_size, color=text_color )

    ax1.text(0.45, 0.08, r'Data from Boera+2018', horizontalalignment='center',  verticalalignment='center', transform=ax1.transAxes, fontsize=figure_text_size, color=text_color)

  ax1.text(0.89, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax1.transAxes, fontsize=figure_text_size, color=text_color)

  ax1.legend( loc=3, fontsize=14, frameon=False )
  ax1.set_xscale('log')
  ax1.set_yscale('log')
  ax2.set_xscale('log')

  ax1.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax1.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )  
  ax2.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax2.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )

figure_name = output_dir + f'flux_ps_{snap_id}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )







