import os, sys
from pathlib import Path
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools')
from tools import *
from load_data import Load_Skewers_File
from calculus_functions import *
from stats_functions import compute_distribution

data_dir = '/raid/bruno/data/'
input_dir  = data_dir + f'cosmo_sims/rescaled_P19/1024_50Mpc_new/skewers_files/'
output_dir = data_dir + f'cosmo_sims/rescaled_P19/1024_50Mpc_new/figures/'
create_directory( output_dir )

n_file = 45


skewers_data = Load_Skewers_File( n_file, input_dir, chem_type = 'HI', axis_list = [ 'x', 'y', 'z' ] )
current_z = skewers_data['current_z']
vel_Hubble = skewers_data['vel_Hubble']
dv = vel_Hubble[1] - vel_Hubble[0] 
skewers_flux = skewers_data['skewers_flux_HI']
# 
curv_vals = [] 
for F in skewers_flux:
  deriv_F = Get_Centered_First_Derivative( F, dv )
  deriv2_F = Get_Centered_Second_Derivative( F, dv )
  curv = deriv2_F / ( 1 + deriv_F**2 )**(3./2)
  curv_mean = np.abs(curv).mean()  
  curv_vals.append( curv_mean )
curv_vals = np.array( curv_vals ).flatten()  
curv_vals = np.abs( curv_vals )

curv_min = 1e-10
curv_vals[curv_vals < curv_min] = curv_min
log_curv = np.log10( curv_vals )

n_bins = 30
curv_hist, bin_centers = compute_distribution( log_curv, n_bins=n_bins, log=False )
d_log_k = bin_centers[1] - bin_centers[0]
curv_distribution = curv_hist / d_log_k

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'
font_size = 14

nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,8*nrows))

ax.plot( bin_centers, curv_distribution )
ax.set_ylabel( r'$d P / d \log \langle|\kappa|\rangle$', fontsize=font_size )
ax.set_xlabel( r'$\log \langle|\kappa|\rangle$',  fontsize=font_size)
# ax.set_xlim( -17.5, -4 )

fig_name = 'curvature_distribution.png'
figure_name = output_dir + f'{fig_name}'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
