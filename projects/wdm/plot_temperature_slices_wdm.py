import os, sys, time
from pathlib import Path
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from figure_functions import *
from load_data import load_snapshot_data_distributed
from power_spectrum_functions import get_power_spectrum


field = 'density'
field = 'temperature'
input_dir = data_dir + f'cosmo_sims/1024_25Mpc_wdm/{field}_slices/'
proj_dir = data_dir + f'projects/wdm/'
output_dir = proj_dir + 'figures/'
create_directory( output_dir )



data_names = [ 'cdm', 'm_5.0kev', 'm_4.0kev', 'm_3.0kev', 'm_2.0kev' ]
labels = [ 'CDM', r'$m_\mathrm{WDM}=5 \, keV$', r'$m_\mathrm{WDM}=4 \, keV$', r'$m_\mathrm{WDM}=3 \, keV$', r'$m_\mathrm{WDM}=2 \, keV$']

z_id = 2

vmin, vmax = np.inf, -np.inf

data_all = {}
for data_id, data_name in enumerate(data_names):
  file_name = input_dir + f'slice_{data_name}_{z_id}.h5'
  print( f'Loading File: {file_name}' )
  file = h5.File( file_name, 'r' ) 
  z = file.attrs['current_z']
  slice = file['slice'][2:3,:,:]
  file.close()
  nx, ny, nz = slice.shape
  print(nx)
  proj = slice.sum( axis=0 ) / nx
  log_proj = np.log10(proj)
  vmin = min( vmin, log_proj.min() )
  vmax = max( vmax, log_proj.max() )
  data_all[data_id] = { 'slice':slice, 'proj':proj, 'log_proj':log_proj }

key = 'proj'
reference_id = 0
for data_id in data_all:
  ratio = data_all[data_id][key] / data_all[reference_id][key] - 1  
  print(ratio.shape) 
  # data_all[data_id]['ratio'] = ratio.sum(axis=0) / nx   
  data_all[data_id]['ratio'] = ratio


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

if field == 'temperature': delta = 0.25
if field == 'density': delta = 0.5

nrows, ncols = 2, 5

fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols,6*nrows))
plt.subplots_adjust( hspace = 0.1, wspace=0.15)

for i in range(ncols):
  
  ax = ax_l[0,i]
  log_proj = data_all[i]['log_proj']
  im = ax.imshow( log_proj, cmap='turbo', vmin=vmin, vmax=vmax*.9 )
  fig.colorbar( im, ax=ax)
  
  text  = f'{labels[i]}' 
  ax.text(0.95, 0.95, text, horizontalalignment='right',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='k')

  
  ax = ax_l[1,i]
  ratio = data_all[i]['ratio']
  im = ax.imshow( ratio, cmap='bwr', vmin=-delta, vmax=delta )
  fig.colorbar( im, ax=ax)
  
  text  = f'{labels[i]}' 
  ax.text(0.95, 0.95, text, horizontalalignment='right',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='k')

  

  
figure_name = output_dir + f'{field}_ratio_wdm_{z_id}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
