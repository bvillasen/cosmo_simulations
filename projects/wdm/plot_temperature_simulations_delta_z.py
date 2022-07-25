import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 



base_dir = data_dir + 'cosmo_sims/wdm_sims/compare_delta_z/'
output_dir = data_dir + f'projects/wdm/figures/'
create_directory( output_dir )


sim_names = [ 'sim_0', 'sim_1', 'sim_2', 'sim_3', 'sim_4', 'sim_5', 'sim_6' ]
delta_z_vals = [ -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75 ]

n_files = 36
sim_data_all = {}
for sim_id, sim_name in enumerate(sim_names):
  
  input_dir = base_dir + f'{sim_name}/analysis_files/'

  z_vals, T0_vals = [], []
  for n_file in range(n_files):

    file_name = input_dir + f'{n_file}_analysis.h5'
    print( f'Loading File: {file_name}' )
    file = h5.File( file_name, 'r')
    z = file.attrs['current_z'][0]
    file.close()

    file_name = input_dir + f'fit_mcmc_delta_0_1.0/fit_{n_file}.pkl'
    fit_data = Load_Pickle_Directory( file_name, 'r' )
    T0 = 10**fit_data['T0']['mean']
    z_vals.append(z)
    T0_vals.append(T0)
  sim_label = r'$\Delta z = {0}$'.format( delta_z_vals[sim_id])
  sim_data_all[sim_id] = {'z':z_vals, 'T0':T0_vals, 'label':sim_label }


import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'



nrows = 1
ncols = 1

tick_size_major, tick_size_minor = 6, 4
tick_label_size_major, tick_label_size_minor = 14, 12
tick_width_major, tick_width_minor = 1.5, 1

font_size = 18
label_size = 16
alpha = 0.7

line_width = 0.6

border_width = 1.5

text_color  = 'black'


fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8*ncols,6*nrows))


for sim_id in sim_data_all:
  sim_data = sim_data_all[sim_id]
  z = sim_data['z']
  T0 = sim_data['T0']
  label = sim_data['label']
  ax.plot( z, T0, label=label)

ax.legend( frameon=False)


ax.set_xlim( 4, 8 )
ax.set_ylim( 7e3, 1.4e4 )

figure_name = output_dir + 'temperature_compare_delta_z.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
