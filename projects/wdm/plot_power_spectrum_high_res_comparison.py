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
output_dir = proj_dir + 'figures/pk_high_res/'
create_directory( output_dir )

n_snap = 6


n_points = 1024
L_Mpc = 25
sim_base_name = f'{n_points}_{L_Mpc}Mpc'

data_lr = {}
for sim_type in ['cdm', 'm4.0kev']:

  sim_dir = base_dir + sim_base_name + f'_{sim_type}/cic/'
  input_dir = sim_dir + 'power_spectrum_files/'

  file_name = input_dir + f'power_spectrum_particles_{n_snap}.pkl'
  pk_data_dm = Load_Pickle_Directory( file_name )

  file_name = input_dir + f'power_spectrum_hydro_{n_snap}.pkl'
  pk_data_gas = Load_Pickle_Directory( file_name )

  input_dir = sim_dir + 'analysis_files/'
  
  if n_snap == 6: snap_id = 25
  if n_snap == 7: snap_id = 29
  if n_snap == 8: snap_id = 33

  file_name = input_dir + f'{snap_id}_analysis.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z'][0]
  flux_k = file['lya_statistics']['power_spectrum']['k_vals'][...]
  flux_pk = file['lya_statistics']['power_spectrum']['p(k)'][...]
  indices = flux_pk > 0
  flux_k  = flux_k[indices]
  flux_pk = flux_pk[indices]
  
  dm = { 'k_vals':pk_data_dm['k_vals'], 'ps':pk_data_dm['power_spectrum']}
  gas = { 'k_vals':pk_data_gas['k_vals'], 'ps':pk_data_gas['power_spectrum']}
  flux = { 'k_vals':flux_k, 'ps':flux_pk }
  data_lr = { 'z':pk_data_dm['z'], 'dm':dm, 'gas':gas, 'flux':flux }


n_points = 2048
L_Mpc = 5
sim_base_name = f'{n_points}_{L_Mpc}Mpc'

data_hr = {}
for sim_type in ['cdm', 'm4.0kev']:

  sim_dir = base_dir + sim_base_name + f'_{sim_type}/cic/'
  input_dir = sim_dir + 'power_spectrum_files/'

  file_name = input_dir + f'power_spectrum_particles_{n_snap}.pkl'
  pk_data_dm = Load_Pickle_Directory( file_name )

  file_name = input_dir + f'power_spectrum_hydro_{n_snap}.pkl'
  pk_data_gas = Load_Pickle_Directory( file_name )

  input_dir = sim_dir + 'analysis_files/'
  
  if n_snap == 6: snap_id = 25
  if n_snap == 7: snap_id = 29
  if n_snap == 8: snap_id = 33

  file_name = input_dir + f'{snap_id}_analysis.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z'][0]
  flux_k = file['lya_statistics']['power_spectrum']['k_vals'][...]
  flux_pk = file['lya_statistics']['power_spectrum']['p(k)'][...]
  indices = flux_pk > 0
  flux_k  = flux_k[indices]
  flux_pk = flux_pk[indices]
  
  dm = { 'k_vals':pk_data_dm['k_vals'], 'ps':pk_data_dm['power_spectrum']}
  gas = { 'k_vals':pk_data_gas['k_vals'], 'ps':pk_data_gas['power_spectrum']}
  flux = { 'k_vals':flux_k, 'ps':flux_pk }
  data_hr = { 'z':pk_data_dm['z'], 'dm':dm, 'gas':gas, 'flux':flux }


import matplotlib
import matplotlib.font_manager
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

fig_width = 1 * figure_width
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
fig.set_size_inches(ncols*fig_width, fig_height )
fig.clf()

gs = plt.GridSpec(h_length, ncols)
gs.update(hspace=0.0, wspace=0.18, )


label_l = '1024  L=25 Mpc/h'
label_h = '2048  L=5 Mpc/h'

for i in range(3):

  if i == 0:
    k_l = data_lr['dm']['k_vals']
    pk_l = data_lr['dm']['ps']
    k_h = data_hr['dm']['k_vals']
    pk_h = data_hr['dm']['ps']
    
  if i == 1:
    k_l = data_lr['gas']['k_vals']
    pk_l = data_lr['gas']['ps']
    k_h = data_hr['gas']['k_vals']
    pk_h = data_hr['gas']['ps']

  if i == 2:
    k_l = data_lr['flux']['k_vals']
    pk_l = data_lr['flux']['ps']    
    k_h = data_hr['flux']['k_vals']
    pk_h = data_hr['flux']['ps']    

  ax1 = plt.subplot(gs[0:main_length, i])
  ax2 = plt.subplot(gs[main_length:h_length, i])


  ax1.plot( k_l, pk_l, label=label_l )
  ax1.plot( k_h, pk_h, label=label_h )

  

  ax1.text(0.89, 0.93, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax1.transAxes, fontsize=font_size, color=text_color) 


  ax1.legend( loc=3, fontsize=14, frameon=False )
  ax1.set_xscale('log')
  ax1.set_yscale('log')

  if i == 0:ax1.set_ylabel( r'$P_\mathrm{DM}(k) $', fontsize=font_size, color=text_color  )
  if i == 0:ax1.set_ylabel( r'$P_\mathrm{gas}(k) $', fontsize=font_size, color=text_color  )
  if i == 0:ax1.set_ylabel( r'$P_\mathrm{flux}(k) $', fontsize=font_size, color=text_color  )
  ax2.set_xlabel( r'$k$  [$h$ Mpc$^{\mathrm{\mathregular{-1}}}$]', fontsize=font_size, color=text_color )

  ax1.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax1.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )  
  ax2.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
  ax2.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )  



figure_name = output_dir + f'ps_high_{n_snap}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
