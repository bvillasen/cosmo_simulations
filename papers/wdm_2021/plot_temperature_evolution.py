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


grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_nsim600/'
fit_name = 'fit_results_P(k)+_Boera_covmatrix'
input_dir = grid_dir + f'fit_mcmc/{fit_name}/temperature_evolution/'
output_dir = data_dir + f'figures/wdm/'
create_directory( output_dir )

files = [ f for f in os.listdir(input_dir) if f[0] == 's' ]
files.sort()
n_files = len(files)

selected_files = np.random.randint( 0, n_files, 10)

data_all = {}
for sim_id,file_id in enumerate(selected_files):
  file_name = input_dir + f'solution_{file_id}.h5'
  print( f'Loading File: {file_name}' )
  file = h5.File( file_name, 'r' )
  z = file['z'][...]
  T0 = file['temperature'][...]
  file.close()
  data_all[sim_id] = { 'z':z, 'T0':T0 }


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


for sim_id in data_all:
  sim_data = data_all[sim_id]
  z = sim_data['z']
  T0 = sim_data['T0']
  label = ''
  ax.plot( z, T0, label=label)

ax.legend( frameon=False)


ax.set_xlim( 2, 8 )
# ax.set_xlims( 2, 8 )


figure_name = output_dir + 'temperature_wdm_chains.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
