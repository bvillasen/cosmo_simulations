import os, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate as interp 
import pymc
root_dir = os.path.dirname(os.getcwd())  + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from matrix_functions import Normalize_Covariance_Matrix

def Plot_MCMC_Stats( stats, MDL, params_mcmc,  stats_file, output_dir, plot_corner=True, plot_model=True,  ):
  cwd = os.getcwd()
  os.chdir( output_dir )
  
  if plot_model: pymc.Matplot.plot(MDL)  

  labels, samples = [], []
  for p_id in params_mcmc.keys():
    param = params_mcmc[p_id]
    labels.append( param['name'] )
    samples.append( param['sampler'].trace())
  samples = np.array( samples ).T

  if plot_corner:
    import corner
    corner_fig = corner.corner(samples[:,:], labels=labels )
    corner_fig.savefig( 'corner_fig.png' )  
  os.chdir( cwd )  


def Plot_Comparable_Data( field, comparable_data, comparable_grid, output_dir  ):

  nrows, ncols = 1, 1
  fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(20*ncols,5*nrows))

  data_mean = comparable_data[field]['mean']
  data_sigma = comparable_data[field]['sigma']
  n_points = len( data_mean )
  x = np.arange( 0, n_points, 1)

  ax.errorbar( x, data_mean, yerr=data_sigma, fmt='o', c='C0', label='Data', ms=1)

  sim_ids = comparable_grid.keys()
  for sim_id in sim_ids:
    sim_mean = comparable_grid[sim_id][field]['mean']
    ax.scatter(x, sim_mean, s=1 )

  ax.set_yscale('log')
  ax.legend( frameon=False )

  figure_name = output_dir + 'data_for_fit.png'
  fig.savefig( figure_name, bbox_inches='tight', dpi=500 )
  print( f'Saved Figure: {figure_name}' )
  
  if 'covariance_matrix' in comparable_data[field]:
    nrows, ncols = 1, 1
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,10*nrows))
    cov_matrix = comparable_data[field]['covariance_matrix']
    im = ax.imshow( cov_matrix, cmap='turbo' )
    cax = ax.inset_axes([1.04, 0.1, 0.05, 0.8], transform=ax.transAxes)
    fig.colorbar(im, ax=ax, cax=cax)
    ax.set_aspect('equal')
    figure_name = output_dir + 'covariance_matrix.png'
    fig.savefig( figure_name, bbox_inches='tight', dpi=500 )
    print( f'Saved Figure: {figure_name}' )
    
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,10*nrows))
    cov_matrix_norm = Normalize_Covariance_Matrix( cov_matrix )
    im = ax.imshow( cov_matrix_norm, cmap='turbo' )
    cax = ax.inset_axes([1.04, 0.1, 0.05, 0.8], transform=ax.transAxes)
    fig.colorbar(im, ax=ax, cax=cax)
    ax.set_aspect('equal')
    figure_name = output_dir + 'covariance_matrix_normalized.png'
    fig.savefig( figure_name, bbox_inches='tight', dpi=500 )
    print( f'Saved Figure: {figure_name}' )
    
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,10*nrows))
    cov_matrix_inv = np.linalg.inv( cov_matrix )
    im = ax.imshow( cov_matrix_inv, cmap='turbo' )
    cax = ax.inset_axes([1.04, 0.1, 0.05, 0.8], transform=ax.transAxes)
    fig.colorbar(im, ax=ax, cax=cax)
    ax.set_aspect('equal')
    figure_name = output_dir + 'covariance_matrix_inverse.png'
    fig.savefig( figure_name, bbox_inches='tight', dpi=500 )
    print( f'Saved Figure: {figure_name}' )
    
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(10*ncols,10*nrows))
    cov_matrix_norm = Normalize_Covariance_Matrix( cov_matrix_inv )
    im = ax.imshow( cov_matrix_norm, cmap='turbo' )
    cax = ax.inset_axes([1.04, 0.1, 0.05, 0.8], transform=ax.transAxes)
    fig.colorbar(im, ax=ax, cax=cax)
    ax.set_aspect('equal')
    figure_name = output_dir + 'covariance_matrix_inverse_normalized.png'
    fig.savefig( figure_name, bbox_inches='tight', dpi=500 )
    print( f'Saved Figure: {figure_name}' )
    