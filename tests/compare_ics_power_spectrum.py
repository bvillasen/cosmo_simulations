import os, sys
from os import listdir
from os.path import isfile, join
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_data import load_snapshot_data_distributed
from power_spectrum_functions import get_power_spectrum


sim_dir = data_dir + 'cosmo_sims/test_ics/'
input_dir_0 = sim_dir + 'snapshot_files_music_hydro/'
input_dir_1 = sim_dir + 'snapshot_files_python_hydro/'
input_dirs = [ input_dir_0, input_dir_1 ]

output_dir = sim_dir + 'figures/'
create_directory( output_dir ) 

data_type = 'particles'
fields = [ 'density' ]

Lbox = 50000.0    #kpc/h
n_cells = 256
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid
precision = np.float64

n_bins = 20
Lbox = 50.0    #Mpc/h
nx, ny, nz = grid_size
dx, dy, dz = Lbox/nx, Lbox/ny, Lbox/nz

# snapshots = [0]
snapshots = [ 0, 2, 4, 6, 8, 10, 12, 13  ]
snapshots.reverse()

power_spectrum_all = {}

z_vals = []
for snap_id in snapshots:
  power_spectrum_all[snap_id] = {}
  for data_type in [ 'particles', 'hydro' ]:
    power_spectrum_all[snap_id][data_type] = {}
    for data_id, input_dir in enumerate(input_dirs):
      snap_data = load_snapshot_data_distributed( data_type, fields,  snap_id, input_dir,  box_size, grid_size, precision  )
      z = snap_data['Current_z']
      if data_id == 0 and data_type=='hydro': z_vals.append(z)
      density = snap_data['density']
      print( f'Computing Power Spectrum  snap_id: {snap_id}  z:{z}' )
      power_spectrum, k_vals, n_in_bin = get_power_spectrum( density, Lbox, nx, ny, nz, dx, dy, dz,  n_kSamples=n_bins )
      power_spectrum_all[snap_id][data_type][data_id] = { 'z': z, 'k_vals': k_vals, 'power_spectrum':power_spectrum }

z_vals = np.array( z_vals )
a_vals = 1./( z_vals + 1 )



figure_width = 4
text_color = 'black'  
nrows = 1
ncols = 2
fig_height = 1 * figure_width
fig_width = ncols * figure_width
h_length = 4
main_length = 3
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_width, fig_height) )
plt.subplots_adjust( hspace = 0.0, wspace=0.25)


i = 0
data_type = 'particles' 
ax1 = ax_l[i]

for snap_id in snapshots:
  z = power_spectrum_all[snap_id][data_type][0]['z'] 
  k_vals = power_spectrum_all[snap_id][data_type][0]['k_vals'] 
  ps_0   = power_spectrum_all[snap_id][data_type][0]['power_spectrum']
  ps_1   = power_spectrum_all[snap_id][data_type][1]['power_spectrum']

  label = r'$z=$' +f'{z:.1f}'
  ax1.plot( k_vals, ps_0, label=label  )
  ax1.plot( k_vals, ps_1, ls='--'  )

ax1.set_xlabel(r'$k$  [$h\, \mathrm{Mpc^{-1}}$]')
ax1.set_ylabel(r'DM $P(k)$')


ax1.set_xscale('log')
ax1.set_yscale('log')

ax1.legend(frameon=False, loc=3, fontsize=8)


i = 1
data_type = 'hydro'
ax1 = ax_l[i]

for snap_id in snapshots:
  z = power_spectrum_all[snap_id][data_type][0]['z'] 
  k_vals = power_spectrum_all[snap_id][data_type][0]['k_vals'] 
  ps_0   = power_spectrum_all[snap_id][data_type][0]['power_spectrum']
  ps_1   = power_spectrum_all[snap_id][data_type][1]['power_spectrum']

  label = r'$z=$' +f'{z:.1f}'
  ax1.plot( k_vals, ps_0, label=label  )
  ax1.plot( k_vals, ps_1, ls='--'  )
  
ax1.set_xlabel(r'$k$  [$h\, \mathrm{Mpc^{-1}}$]')
ax1.set_ylabel(r'Gas $P(k)$')
  

ax1.set_xscale('log')
ax1.set_yscale('log')


ax1.legend(frameon=False, loc=3, fontsize=8)

figure_name  = output_dir + 'power_spectrum_comparison_hydro.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )



