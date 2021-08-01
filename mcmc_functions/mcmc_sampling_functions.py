import os, sys
import numpy as np



def Get_Highest_Likelihood_Params( param_samples, n_bins=100 ):
  param_ids = param_samples.keys()
  n_param = len(param_ids )
  param_samples_array = np.array([ param_samples[i]['trace'] for i in range(n_param) ] ).T

  hist_4D, bin_edges = np.histogramdd( param_samples_array, bins=n_bins )
  bin_centers = [ (edges[1:] + edges[:-1])/2 for edges in bin_edges ]
  hist_max = hist_4D.max()
  max_id = np.where( hist_4D == hist_max  )
  p_vals = np.array([ bin_centers[i][max_id[i]] for i in range(n_param) ])
  # print( f"Highest_Likelihood: {hist_max} {p_vals}")
  while( len(p_vals.flatten()) > n_param ):
    n_bins = np.int( n_bins * 0.9 )
    hist_4D, bin_edges = np.histogramdd( param_samples_array, bins=n_bins )
    bin_centers = [ (edges[1:] + edges[:-1])/2 for edges in bin_edges ]
    hist_max = hist_4D.max()
    max_id = np.where( hist_4D == hist_max  )
    p_vals = np.array([ bin_centers[i][max_id[i]] for i in range(n_param) ])
    # print( f"Highest_Likelihood: {hist_max} {p_vals}")
  return p_vals 

