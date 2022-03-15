import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
cosmo_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
sys.path.append( cosmo_dir + 'lya_statistics/data' )
from tools import *
from data_optical_depth import *
from colors import * 
from stats_functions import compute_distribution, get_highest_probability_interval
from plot_flux_power_spectrum_grid import Plot_Power_Spectrum_Grid
from load_tabulated_data import load_data_boera, load_data_irsic, load_data_boss 
from matrix_functions import Normalize_Covariance_Matrix, Merge_Matrices
from data_optical_depth_HeII import data_tau_HeII_Worserc_2019 as data_worsec

import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

output_dir = data_dir + 'figures/thermal_history/cov_matrix_data/'
create_directory( output_dir )

ps_data_dir = cosmo_dir + 'lya_statistics/data/'
data_boera_dir = ps_data_dir + 'data_power_spectrum_boera_2019/'
data_boera = load_data_boera( data_boera_dir )

data_irsic_dir = ps_data_dir + 'data_power_spectrum_irsic_2017/'
data_irsic = load_data_irsic( data_irsic_dir )

data_boss_dir = ps_data_dir + 'data_power_spectrum_boss/'
data_boss = load_data_boss(data_boss_dir)

covariance_matrices = []
data_sets =  [ data_boss, data_irsic, data_boera ]
for data_set in data_sets:
  for data_id in data_set:
    if data_id in [ 'z_vals', 'k_vals', 'full_covariance' ]: continue
    cov_matrix = data_set[data_id]['covariance_matrix']
    covariance_matrices.append( cov_matrix )
    
    
tau_sigma = data_worsec['tau_sigma']
n = len( tau_sigma )
tau_cov = np.zeros([ n,n ])
for i in range( n):
  tau_cov[i,i] = tau_sigma[i]**2
covariance_matrices.append( tau_cov )
full_covariance_matrix  = Merge_Matrices( covariance_matrices )

# 
# plot_normalized = True
# 
# label_size = 16
# figure_text_size = 18
# tick_label_size_major = 15
# tick_label_size_minor = 13
# tick_size_major = 5
# tick_size_minor = 3
# tick_width_major = 1.5
# tick_width_minor = 1
# text_color = 'black'
# legend_font_size = 14
# ax_lenght = 6 
# 
# 
# ncols, nrows = 3, 1
# figure_width, figure_height = ncols * ax_lenght, nrows * ax_lenght
# fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width,figure_height))
# plt.subplots_adjust( hspace = 0.15, wspace=0.2)
# vmin, vmax = np.inf, -np.inf
# for data_id in data_boera:
#   if data_id in [ 'z_vals', 'full_covariance', 'k_vals']: continue
#   cov_matrix = data_boera[data_id]['covariance_matrix']
#   if plot_normalized: cov_matrix = Normalize_Covariance_Matrix( cov_matrix )
#   vmin, vmax = min(cov_matrix.min(), vmin), max(cov_matrix.max(), vmax)
# for data_id in data_boera:
#   if data_id in [ 'z_vals', 'full_cov_matrix', 'k_vals']: continue
#   ax = ax_l[data_id]
#   data = data_boera[data_id]
#   z = data['z']
#   cov_matrix = data['covariance_matrix']
#   if plot_normalized: cov_matrix = Normalize_Covariance_Matrix( cov_matrix )
#   k_vals = data['k_vals']
#   k_min, k_max = np.log10(k_vals.min()), np.log10(k_vals.max())
#   im = ax.imshow( cov_matrix, cmap='turbo', extent=(k_min, k_max, k_max, k_min), vmin=vmin, vmax=vmax )
#   ax.set_aspect('equal')
#   if data_id == 2:
#     cax = ax.inset_axes([1.04, 0.1, 0.05, 0.8], transform=ax.transAxes)
#     fig.colorbar(im, ax=ax, cax=cax)
#   ax.text(0.85, 0.92, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='white') 
#   ax.set_ylabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )
#   ax.set_xlabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )
#   ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
#   ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
#   ax.set_xticks( [ -2, -1.5, -1])
#   ax.set_yticks( [ -2, -1.5, -1])
# 
# figure_name = output_dir + 'covariance_matrix_boera'
# if plot_normalized: figure_name += '_normalized'
# figure_name += '.png'
# fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
# print( f'Saved Figure: {figure_name}' )
# 
# 
# ncols, nrows = 4, 2
# figure_width, figure_height = ncols * ax_lenght, nrows * ax_lenght
# fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width,figure_height))
# plt.subplots_adjust( hspace = 0.15, wspace=0.2)
# vmin, vmax = np.inf, -np.inf
# for data_id in data_irsic:
#   if data_id in [ 'z_vals', 'full_covariance', 'k_vals']: continue
#   cov_matrix = data_irsic[data_id]['covariance_matrix']
#   if plot_normalized: cov_matrix = Normalize_Covariance_Matrix( cov_matrix )
#   vmin, vmax = min(cov_matrix.min(), vmin), max(cov_matrix.max(), vmax) 
# for data_id in data_irsic:
#   if data_id in [ 'z_vals', 'full_covariance', 'k_vals']: continue
#   ax_i = data_id // ncols
#   ax_j = data_id % ncols
#   ax = ax_l[ax_i][ax_j]
#   data = data_irsic[data_id]
#   z = data['z']
#   cov_matrix = data['covariance_matrix']
#   if plot_normalized: cov_matrix = Normalize_Covariance_Matrix( cov_matrix )
#   k_vals = data['k_vals']
#   k_min, k_max = np.log10(k_vals.min()), np.log10(k_vals.max())
#   im = ax.imshow( cov_matrix, cmap='turbo', extent=(k_min, k_max, k_max, k_min), vmin=vmin, vmax=vmax )
#   ax.set_aspect('equal')
#   if data_id == ncols-1:
#     cax = ax.inset_axes([1.04, 0.1, 0.05, 0.8], transform=ax.transAxes)
#     fig.colorbar(im, ax=ax, cax=cax)
#   ax.text(0.85, 0.92, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='black') 
#   ax.set_ylabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )
#   ax.set_xlabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )
#   ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
# 
# figure_name = output_dir + 'covariance_matrix_irsic'
# if plot_normalized: figure_name += '_normalized'
# figure_name += '.png'
# fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
# print( f'Saved Figure: {figure_name}' )
# 
# 
# ncols, nrows = 1, 1
# figure_width, figure_height = ncols * ax_lenght, nrows * ax_lenght
# fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width,figure_height))
# plt.subplots_adjust( hspace = 0.15, wspace=0.2)
# cov_matrix = data_irsic['full_covariance']
# if plot_normalized: cov_matrix = Normalize_Covariance_Matrix( cov_matrix )
# n = cov_matrix.shape[0]
# im = ax.imshow( cov_matrix, cmap='turbo', extent=(0,n,0,n) )
# 
# # Plot redshift lines
# k_vals = data_irsic['k_vals']
# n_samples = len(k_vals)
# n_redshift = cov_matrix.shape[0] // n_samples
# lw = 0.8
# for i in range(n_redshift):
#   for j in range(n_redshift):
#     ax.axvline( x=i*n_samples, ls='--', c='k', lw=lw)
#     ax.axhline( y=i*n_samples, ls='--', c='k', lw=lw)
# 
# 
# 
# ax.set_aspect('equal')
# cax = ax.inset_axes([1.04, 0.1, 0.05, 0.8], transform=ax.transAxes)
# fig.colorbar(im, ax=ax, cax=cax)
# ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
# ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
# 
# figure_name = output_dir + 'covariance_matrix_irsic_full'
# if plot_normalized: figure_name += '_normalized'
# figure_name += '.png'
# fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
# print( f'Saved Figure: {figure_name}' )
# 
# ncols, nrows = 5, 3
# figure_width, figure_height = ncols * ax_lenght, nrows * ax_lenght
# fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width,figure_height))
# plt.subplots_adjust( hspace = 0.15, wspace=0.2)
# vmin, vmax = np.inf, -np.inf
# for data_id in data_irsic:
#   if data_id in [ 'z_vals', 'full_covariance', 'k_vals']: continue
#   cov_matrix = data_boss[data_id]['covariance_matrix']
#   if plot_normalized: cov_matrix = Normalize_Covariance_Matrix( cov_matrix )
#   vmin, vmax = min(cov_matrix.min(), vmin), max(cov_matrix.max(), vmax) 
# for data_id in data_boss:
#   if data_id in [ 'z_vals', 'full_covariance', 'k_vals']: continue
#   ax_i = data_id // ncols
#   ax_j = data_id % ncols
#   ax = ax_l[ax_i][ax_j]
#   data = data_boss[data_id]
#   z = data['z']
#   cov_matrix = data['covariance_matrix']
#   if plot_normalized: cov_matrix = Normalize_Covariance_Matrix( cov_matrix )
#   k_vals = data['k_vals']
#   k_min, k_max = np.log10(k_vals.min()), np.log10(k_vals.max())
#   im = ax.imshow( cov_matrix, cmap='turbo', extent=(k_min, k_max, k_max, k_min), vmin=vmin, vmax=vmax )
#   ax.set_aspect('equal')
#   if data_id == ncols-1:
#     cax = ax.inset_axes([1.04, 0.1, 0.05, 0.8], transform=ax.transAxes)
#     fig.colorbar(im, ax=ax, cax=cax)
#   ax.text(0.85, 0.92, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='white') 
#   ax.set_ylabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )
#   ax.set_xlabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )
#   ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
# 
# figure_name = output_dir + 'covariance_matrix_boss'
# if plot_normalized: figure_name += '_normalized'
# figure_name += '.png'
# fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
# print( f'Saved Figure: {figure_name}' )