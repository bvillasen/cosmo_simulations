import numpy as np
from tools import print_line_flush
from scipy import interpolate as interp 



def compute_covariance_matrix( samples ):
  n_samples, sample_length = samples.shape 
  cov_matrix =  np.zeros( [sample_length, sample_length] )
  for i in range( sample_length ):
    for j in range( sample_length ):
      vals_i = samples[:,i]
      vals_j = samples[:,j]
      mean_i, mean_j = vals_i.mean(), vals_j.mean()
      n_samples_i = vals_i.shape[0]
      n_samples_j = vals_j.shape[0]
      if n_samples_i != n_samples_j: 
        print('ERROR: Number od samples mismatch')
        exit
      n_samples = n_samples_i
      # cov_matrix[i,j] = np.array([ (vals_i[k] - mean_i)*(vals_j[k] - mean_j) for k in range(n_samples)  ]).mean()
      cov_matrix[i,j] = ( (vals_i - mean_i)*(vals_j - mean_j) ).mean() 
  return cov_matrix

def get_sample_mean( n_in_sample, data ):
  n_dim = data.ndim
  n_total = data.shape[0]
  sample_ids = np.random.randint( 0, n_total, n_in_sample  )
  sample = data[sample_ids]
  sample_mean = sample.mean(axis=0)
  return sample_mean


def bootstrap_sample_mean( n_iterations, n_in_sample, data, print_out ):
  sample_mean_all = []
  for i in range( n_iterations ):
    if i%(n_iterations//10)==0: print_line_flush( f' Sampling Iteration: {i}/{n_iterations}   {i/n_iterations*100}%' )
    sample_mean = get_sample_mean( n_in_sample, data )
    sample_mean_all.append( sample_mean )
  if (i+1)%(n_iterations//10)==0: print_line_flush( f' Sampling Iteration: {i+1}/{n_iterations}   {(i+1)/n_iterations*100}%' )  
  sample_mean_all = np.array( sample_mean_all )
  return sample_mean_all

def get_HPI_2D( hist_2D, frac_final ):
  max = hist_2D.max()
  sum_total = hist_2D.sum()
  level = max
  factor = 0.99
  frac_enclosed = 0
  while  frac_enclosed < frac_final:
    level = level * factor
    indices_enclosed = np.where( hist_2D >= level )
    sum_enclosed = (hist_2D[indices_enclosed]).sum()
    frac_enclosed = sum_enclosed / sum_total
  return level, indices_enclosed

def compute_distribution( values, n_bins=None, log=False, edges=None, normalize_to_bin_width=False, normalize_to_interval=False ):
  if log: values = np.log10( values )
  val_min, val_max = values.min(), values.max()
  if not edges: edges = np.linspace( val_min, val_max, n_bins+1 )
  hist, edges = np.histogram( values, bins=edges )
  # print( edges )
  hist = hist.astype( np.float )
  distribution = hist / hist.sum()
  if not log: centers = 0.5*( edges[:-1] + edges[1:] )
  else: 
    edges = 10**edges
    centers = np.sqrt( edges[:-1] * edges[1:] )
  if centers[0] > centers[-1]:
    centers = centers[::-1]
    distribution = distribution[::-1]
  if normalize_to_bin_width:
    bin_width = centers[1] - centers[0]
    distribution /= bin_width
  if normalize_to_interval:
    interval = centers[-1] - centers[0]
    distribution /= interval
  return distribution, centers


def get_highest_probability_interval( bin_centers, distribution, fill_sum, log=False, n_interpolate=None, print_eval=False):
  if log: bin_centers = np.log10( bin_centers )
  # print( f'Original {bin_centers}')

  min, max = bin_centers.min(), bin_centers.max()
  if np.abs( min - max ) < 1e-6:  
    print( 'WARNING: 1D HPI: All samples have the same value')
    return min, max, max,  1.0
  if np.any(bin_centers[1:] == bin_centers[:-1]): 
    print( f'WARNING: 1D HPI: duplicate in bin_centers {bin_centers}')
    exit(-1)
  if max / bin_centers.sum() > fill_sum:
     print( f'WARNING: 1D HPI: fill sum contained on one bin')
     return max, max, max, max / bin_centers.sum()
  if n_interpolate: 
    bin_centers_interp = np.linspace( min, max, n_interpolate )
    # distribution = np.interp( bin_centers_interp, bin_centers, distribution )
    f_interp  = interp.interp1d( bin_centers, distribution,  kind='cubic' )
    distribution_interp = f_interp(bin_centers_interp)
    distribution = distribution_interp
    bin_centers = bin_centers_interp
    # print( f'interpolated {bin_centers}')
  distribution = distribution / distribution.sum()
  n = len( distribution )
  v_max = distribution.max()
  id_max = np.where( distribution == v_max )[0]
  sum_val = distribution.sum()
  # if len( id_max ) > 1:
  #   print('ERROR: Unable to find unique maximum in distribution')
  #   exit(-1)
  id_max  = id_max[0]
  id_l, id_r = id_max - 1, id_max + 1
  # print( id_l, id_r )
  if id_l == -1: id_l = 0
  if id_r == n:  id_r = n-1
  # print( distribution.sum() )
  while distribution[id_l:id_r].sum() < fill_sum* sum_val:
    # print( id_l, id_r, distribution[id_l:id_r].sum()*sum_val)
    if  id_r == n-1: id_l -= 1
    elif  id_l == 0: id_r += 1
    elif distribution[id_l] < distribution[id_r]: id_r += 1
    elif distribution[id_l] > distribution[id_r]: id_l -= 1
    elif distribution[id_l] == distribution[id_r]: 
      id_l -= 1
      # id_r += 1
    if id_l < 0 or id_r > n-1: 
      interval_sum = distribution[id_l:id_r].sum()*sum_val
      print( f'ERROR: HPI  n:{n}  id_l:{id_l}  id_r:{id_r}  interval_sum:{interval_sum}   ')
      break 
  if log: bin_centers = 10**bin_centers
  v_l, v_r, v_max = bin_centers[id_l], bin_centers[id_r], bin_centers[id_max]
  sum_interval = distribution[id_l:id_r].sum() 
  if print_eval: print( f'Eval f(l): {f_interp(v_l)}  f(r): {f_interp(v_r)}  sum: {sum_interval}')
  return v_l, v_r, v_max,  sum_interval 
