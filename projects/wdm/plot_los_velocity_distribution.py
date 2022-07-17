import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import Load_Skewers_File, load_analysis_data
from figure_functions import *
from stats_functions import compute_distribution, get_highest_probability_interval

use_mpi = False
if use_mpi:
  from mpi4py import MPI
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  n_procs = comm.Get_size()
else:
  rank = 0
  n_procs = 1

proj_dir = data_dir + 'projects/wdm/'
output_dir = proj_dir + 'figures/los_velocity_distribution/'
create_directory( output_dir )


files = [ 0, 7, 15, 25, 33 ]

axis_list = [ 'x', 'y', 'z' ]
n_skewers_list = [ 'all', 'all', 'all']
skewer_ids_list = [ 'all', 'all', 'all']
field_list = [ 'los_velocity',  ]

n_bins = 200
vel_min = 1e-3

data_all = {}
for type in [ 'cdm', 'wdm' ]:
  data_all[type] = {}
  if type == 'cdm': sim_dir  = data_dir + f'cosmo_sims/wdm_sims/new/1024_25Mpc_cdm/'
  if type == 'wdm': sim_dir  = data_dir + f'cosmo_sims/wdm_sims/new/1024_25Mpc_m4.0kev/'
  input_dir  = sim_dir + f'skewers_files/'

  for snap_id,n_file in enumerate(files):
    skewer_dataset = Load_Skewers_File( n_file, input_dir, axis_list=axis_list, fields_to_load=field_list )
    z = skewer_dataset['current_z']
    los_velocity = skewer_dataset['los_velocity']
    los_velocity[los_velocity<vel_min] = vel_min
    distribution, centers = compute_distribution( los_velocity, n_bins=n_bins, log=True )
    
    data_all[type][snap_id] = { 'z':z, 'bin_centers':centers, 'distribution':distribution }



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


nrows, ncols = 1, 1

fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.15)


for i in range(2):

  if i == 0: 
   type = 'cdm'
   ls = '-'
   lw = 2.5
  if i == 1: 
   type = 'wdm'
   ls = '--'
   lw = 1.5

  data = data_all[type]
  for snap_id in data:
    z = data[snap_id]['z']
    bin_centers  = data[snap_id]['bin_centers']
    distribution = data[snap_id]['distribution']

    label = ''
    if i == 0:
     label = r'$z$' + f'={z}'
    if i == 1 and snap_id == 0: label= 'WDM'
    color = f'C{snap_id}'
    if i == 1: color = 'k'
    ax.plot( bin_centers, distribution, c=color, lw=lw, label=label, ls=ls )
   
 
ax.legend( frameon=False, loc=1, fontsize=12)

ax.set_ylabel( r'$P(v\,_\mathrm{LOS})$', fontsize=label_size, color= text_color )  
ax.set_xlabel( r'$v\,_\mathrm{LOS}$  [km/s]', fontsize=label_size, color=text_color )
ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')

ax.set_xlim( 0.002, 300 )
ax.set_ylim( 0.0, 0.02 )

figure_name = output_dir + f'los_velocity_distribution.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
