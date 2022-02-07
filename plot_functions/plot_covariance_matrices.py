import sys, os
import numpy as np
import h5py as h5
import palettable
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib.pyplot as plt
import pylab
import pickle
from matplotlib.legend_handler import HandlerTuple
import os, sys
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from matrix_functions import Normalize_Covariance_Matrix


import matplotlib
matplotlib.font_manager.findSystemFonts(fontpaths=['/home/bruno/fonts/Helvetica'], fontext='ttf')
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'
label_size = 16
figure_text_size = 18
tick_label_size_major = 15
tick_label_size_minor = 13
tick_size_major = 5
tick_size_minor = 3
tick_width_major = 1.5
tick_width_minor = 1
text_color = 'black'
legend_font_size = 14


def plot_cov_matrices_data_sim( cov_matrices,  output_dir, plot_normalized=False ):

  ncols, nrows = 3, 3
  ax_lenght = 6 
  figure_width, figure_height = ncols * ax_lenght, nrows * ax_lenght


  fig, ax_l = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figure_width,figure_height))
  plt.subplots_adjust( hspace = 0.15, wspace=0.2)

  for j in range(3):
    k_vals = cov_matrices['k_vals'][j]
    z = cov_matrices['z_vals'][j]
    cov_max, cov_min = cov_matrices['cov_max'][j], cov_matrices['cov_min'][j],   
    for i in range(3):
      if i == 0: cov_matrix = cov_matrices['data'][j]
      if i == 1: cov_matrix = cov_matrices['sims'][j]
      if i == 2: cov_matrix = cov_matrices['rescaled'][j] 
      
      ax = ax_l[i][j]
      
      if plot_normalized:
        cov_matrix = Normalize_Covariance_Matrix( cov_matrix )
        cov_max, cov_min = 1, 0
      
      k_min, k_max = np.log10(k_vals.min()), np.log10(k_vals.max())
      im = ax.imshow( cov_matrix, cmap='turbo', extent=(k_min, k_max, k_max, k_min) )
      ax.set_aspect('equal')
      
      if j == 2:
        cax = ax.inset_axes([1.04, 0.1, 0.05, 0.8], transform=ax.transAxes)
        fig.colorbar(im, ax=ax, cax=cax)
        
      ax.text(0.85, 0.92, r'$z=${0:.1f}'.format(z), horizontalalignment='center',  verticalalignment='center', transform=ax.transAxes, fontsize=figure_text_size, color='white') 
      
      
      ax.set_ylabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )
      ax.set_xlabel( r'$\log_{10} \,k\,\,\, [\mathregular{s/km}]$  ', fontsize=label_size, color= text_color )
    
      ax.tick_params(axis='both', which='major', color=text_color, labelcolor=text_color, labelsize=tick_label_size_major, size=tick_size_major, width=tick_width_major, direction='in' )
      ax.tick_params(axis='both', which='minor', color=text_color, labelcolor=text_color, labelsize=tick_label_size_minor, size=tick_size_minor, width=tick_width_minor, direction='in')
      
      ax.set_xticks( [ -2, -1.5, -1])
      ax.set_yticks( [ -2, -1.5, -1])
    
    
  figure_name = output_dir + 'covariance_matrix_data_sim'
  if plot_normalized: figure_name += '_normalized'
  figure_name += '.png'
  fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
  print( f'Saved Figure: {figure_name}' )
