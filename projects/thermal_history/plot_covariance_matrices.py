import os, sys
import numpy as np
import pickle
import matplotlib.pyplot as plt
base_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from figure_functions import *
from matrix_functions import Normalize_Covariance_Matrix

proj_dir = data_dir + 'projects/thermal_history/'
input_dir = proj_dir + 'data/sim_grid/1024_P19m_np4_nsim400/'
output_dir = proj_dir + 'figures/'

file_name = input_dir + 'selected_sims.pkl'
selected_sims_all = Load_Pickle_Directory( file_name )
defult_params = selected_sims_all['default_params'] 

param_ids = [ 0, 1, 2, 3 ]

selected_vals_all = {0:[1, 2, 3, 4], 1:[0, 1, 2, 3], 2:[0, 1, 2, 3], 3:[ 1, 2, 3, 4 ]}

files_to_load = [ 45, 29 ]


cov_matrices_all = {}
for param_id in param_ids:
  selected_sims = selected_sims_all[param_id]
  param_name = selected_sims['param_name']
  param_vals = selected_sims['param_vals']
  print( f'{param_name}  {param_vals}')
  cov_matrices_param = {}
  selected_vals = selected_vals_all[param_id]
  cov_matrices = {}
  cov_matrices['param_name'] = param_name
  cov_matrices['selected_sims'] = {}
  for v_id, selected_val in enumerate(selected_vals):
    data = selected_sims['selected_sims'][selected_val]
    sim_key = data['sim_key']
    sim_params = data['sim_params']
    sim_dir = input_dir + f'pk_covariance/{sim_key}/'
    cov_matrices['selected_sims'][v_id] = { 'param_val':sim_params[param_name], 'cov_matrices':{} }
    for z_id, n_file in enumerate(files_to_load):
      file_name = sim_dir + f'covariance_{n_file:03}.pkl'
      cov_data = Load_Pickle_Directory( file_name )
      z = cov_data['current_z']
      cov_matrix = cov_data['covariance_matrix']
      cov_matrix = Normalize_Covariance_Matrix( cov_matrix )
      k_vals = cov_data['k_vals']
      cov_matrices['selected_sims'][v_id][z_id] = { 'z':z, 'cov_matrix':cov_matrix, 'k_vals':k_vals }
  cov_matrices_all[param_id] = cov_matrices
      
      
tick_size_major, tick_size_minor = 6, 4
tick_label_size_major, tick_label_size_minor = 12, 12
tick_width_major, tick_width_minor = 1.5, 1
figure_text_size = 15

font_size = 16
legend_font_size = 12
alpha = 0.5

text_color = 'black'
border_width = 1.5

# type = 'H'
type = 'He'

if type == 'H': 
  param_ids = [ 1, 3 ]
  z_id = 1
if type == 'He': 
  param_ids = [ 0, 2 ]
  z_id = 0

labels = { 'scale_He':r'$\beta_{\mathrm{He}}$', 'scale_H':r'$\beta_{\mathrm{H}}$', 'deltaZ_He':r'$\Delta z_{\mathrm{He}}$', 'deltaZ_H':r'$\Delta z_{\mathrm{H}}$'    }


nrows, ncols = 2, 4 
fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width*ncols/2,figure_width*nrows/2))
plt.subplots_adjust( hspace = 0.03, wspace=0.03)


cov_reference = None
vmin, vmax = np.inf, -np.inf
cov_data = []
selected_indx = 0
for index_i in range( nrows ):
  for index_j in range( ncols ):
    param_id = param_ids[index_i]
    data = cov_matrices_all[param_id]
    selected_sims = data['selected_sims']
    sim_data = selected_sims[index_j]
    cov_matrix = sim_data[z_id]['cov_matrix']
    vmin = min( vmin, cov_matrix.min() )
    vmax = max( vmax, cov_matrix.max() )
    if index_i==selected_indx: 
      if cov_reference is None: cov_reference = cov_matrix 
      diff = np.abs(( cov_reference - cov_matrix) )
      diff = np.abs(cov_reference - cov_matrix) 
      ids = np.where( diff == diff.max()) 
      print( ids, diff.mean() ) 

    
for index_i in range( nrows ):
  for index_j in range( ncols ):
    ax = ax_l[index_i][index_j] 

    param_id = param_ids[index_i]
    data = cov_matrices_all[param_id]
    param_name = data['param_name']
    selected_sims = data['selected_sims']

    sim_data = selected_sims[index_j]
    param_val = sim_data['param_val'] 
    z = sim_data[z_id]['z']
    cov_matrix = sim_data[z_id]['cov_matrix']
    k_vals = sim_data[z_id]['k_vals']
    k_min, k_max = np.log10(k_vals.min()), np.log10(k_vals.max())
    print( f'{param_name}  {z}  {param_val}' )
    im = ax.imshow( cov_matrix, cmap='turbo', extent=(k_min, k_max, k_max, k_min ), vmin=vmin, vmax=vmax )
    
    # if index_j==ncols-1 and index_i==0: fig.colorbar( im, ax=ax_l[:, ncols-1], shrink=1)
    if index_j==ncols-1 and index_i==0:
      L = 1.5
      cax = ax.inset_axes([1.04, -L/2, 0.07, L], transform=ax.transAxes)
      cbar=fig.colorbar(im, ax=ax, cax=cax)  
      cax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
      [sp.set_linewidth(border_width) for sp in cax.spines.values()] 
      cbar.set_label('Normalized Covariance', fontsize=font_size, color=text_color)
      
        
    param_label = labels[param_name]
    text = param_label + r'$=$' + f'{param_val:.2f}'
    ax.text(0.8, 0.94, text, horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='white') 
    
    if index_j == 0:ax.text(0.13, 0.07, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='white') 
          
    ax.tick_params(axis='both', which='major', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major  )
    ax.tick_params(axis='both', which='minor', direction='in', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor  )
    
    label = r'$\log _{10} \, k$'
    if index_i == nrows - 1: ax.set_xlabel( label, fontsize=font_size, color=text_color )
    if index_j == 0: ax.set_ylabel( label, fontsize=font_size, color=text_color )
    
    if index_j != 0: ax.set_yticklabels([])
    if index_i != nrows-1: ax.set_xticklabels([])
    
    [sp.set_linewidth(border_width) for sp in ax.spines.values()] 
    



figure_name = output_dir + f'covariance_matrices_{type}.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )    




