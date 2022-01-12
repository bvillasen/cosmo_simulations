import os, sys
import numpy as np
import pymc
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from interpolation_functions import Interpolate_4D, Interpolate_3D
from stats_functions import compute_distribution, get_highest_probability_interval

############################################################################################################


def Sample_Fields_from_Trace( fields_list, param_samples, data_grid, SG, hpi_sum=0.7, n_samples=None, params_HL=None, sample_log=False , output_trace=False):

  if sample_log: print( 'WARNING: Sampling Log Space')
  fields_list = [ field for field in fields_list if field != 'P(k)' ]
  print(f'\nSampling Fields: {fields_list}')
  param_ids = param_samples.keys()
  n_param = len(param_ids )
  param_samples_array = np.array([ param_samples[i]['trace'] for i in range(n_param) ] ).T

  if not n_samples: n_samples = len( param_samples[0]['trace'] )
  print(f' N Samples: {n_samples}')


  samples_out = {}
  for field in fields_list:
    print(f' Sampling Field: {field}')
    samples = []
    for i in range( n_samples ):
      p_vals = param_samples_array[i]
      if n_param == 3: interp = Interpolate_3D(  p_vals[0], p_vals[1], p_vals[2], data_grid, field, 'mean', SG, clip_params=True, interp_log=sample_log ) 
      if n_param == 4: interp = Interpolate_4D(  p_vals[0], p_vals[1], p_vals[2], p_vals[3], data_grid, field, 'mean', SG, clip_params=True, interp_log=sample_log ) 
      samples.append( interp )
    if field  in ['z_ion_H']:
      samples = np.array( samples )
      mean = samples.mean()
      sigma = np.std( samples )
      n_bins = 1000
      distribution, bin_centers = compute_distribution( samples, n_bins, log=False )
      fill_sum = hpi_sum
      v_l, v_r, v_max, sum = get_highest_probability_interval( bin_centers, distribution, fill_sum, log=log_hpi, n_interpolate=1000)
      lower = v_l
      higher = v_r
      trace = samples
    else:
      samples = np.array( samples ).T
      mean = np.array([ vals.mean() for vals in samples ])
      sigma = [ ]
      lower, higher = [], []
      for i in range( len( samples ) ):
        sigma.append( np.sqrt(  ( (samples[i] - mean[i])**2).mean()  ) )
        values = samples[i]
        n_bins = 1000
        distribution, bin_centers = compute_distribution( values, n_bins, log=False )
        fill_sum = hpi_sum
        log_hpi = True
        if field in  ['gamma', 'T0', 'z_ion_H' ] : log_hpi = False
        if sample_log: log_hpi = False
        v_l, v_r, v_max, sum = get_highest_probability_interval( bin_centers, distribution, fill_sum, log=log_hpi, n_interpolate=1000)
        lower.append( v_l )
        higher.append( v_r )
      trace = samples.T
      sigma  = np.array( sigma )
      lower  = np.array( lower )
      higher = np.array( higher )
    samples_stats = {}
    samples_stats['mean']   = mean
    if output_trace: samples_stats['trace'] = trace
    # samples_stats['sigma']  = sigma
    if 'z' in data_grid[0][field]: samples_stats['z'] = data_grid[0][field]['z']
    samples_stats['lower']  = lower
    samples_stats['higher'] = higher
    if params_HL is not None:
      for key in params_HL:
        p_vals = params_HL[key]
        if n_param == 3: interp_HL = Interpolate_3D(  p_vals[0], p_vals[1], p_vals[2], data_grid, field, 'mean', SG, clip_params=True, interp_log=sample_log ) 
        if n_param == 4: interp_HL = Interpolate_4D(  p_vals[0], p_vals[1], p_vals[2], p_vals[3], data_grid, field, 'mean', SG, clip_params=True, interp_log=sample_log ) 
        samples_stats[key] = interp_HL
    
    if sample_log:
      for key in samples_stats:
        if key == 'z': continue
        samples_stats[key] = 10**samples_stats[key]
    samples_out[field] = samples_stats
  return samples_out



############################################################################################################

def Sample_Power_Spectrum_from_Trace( param_samples, data_grid, SG, hpi_sum=0.7, n_samples=None, params_HL=None, output_trace=False ):  
  print(f'\nSampling Power Spectrum')
  ps_samples = {}
  param_ids = param_samples.keys()
  n_param = len(param_ids )
  param_samples_array = np.array([ param_samples[i]['trace'] for i in range(n_param) ] ).T
  if not n_samples: n_samples = len( param_samples[0]['trace'] )
  print(f' N Samples: {n_samples}')
  n_z_ids = len( data_grid.keys() )
  for id_z in range( n_z_ids ):
    print_line_flush( f' Sampling z_id: {id_z+1}/{n_z_ids}')
    ps_data = data_grid[id_z]
    ps_samples[id_z] = {}
    ps_samples[id_z]['z'] = ps_data['z']

    samples = []
    for i in range( n_samples ):
      p_vals = param_samples_array[i]
      if n_param == 3: ps_interp = Interpolate_3D(  p_vals[0], p_vals[1], p_vals[2], ps_data, 'P(k)', 'mean', SG, clip_params=True ) 
      if n_param == 4: ps_interp = Interpolate_4D(  p_vals[0], p_vals[1], p_vals[2], p_vals[3], ps_data, 'P(k)', 'mean', SG, clip_params=True ) 
      if ( ps_interp < 0 ).sum() > 0: 
        print(f'Negative Power Spectrum for parameters: {p_vals}')
        print( ps_interp )
        exit(-1)  
      samples.append( ps_interp )
    samples = np.array( samples ).T
    ps_mean = np.array([ ps_vals.mean() for ps_vals in samples ])
    ps_sigma = [ ]
    ps_lower, ps_higher = [], []
    for i in range( len( samples ) ):
      ps_sigma.append( np.sqrt(  ( (samples[i] - ps_mean[i])**2).mean()  ) )
      values = samples[i]
      n_bins = 100
      distribution, bin_centers = compute_distribution( values, n_bins, log=True )
      fill_sum = hpi_sum
      v_l, v_r, v_max, sum = get_highest_probability_interval( bin_centers, distribution, fill_sum, log=True, n_interpolate=500)
      ps_lower.append( v_l )
      ps_higher.append( v_r )
    trace = samples.T
    ps_sigma  = np.array( ps_sigma )
    ps_lower  = np.array( ps_lower )
    ps_higher = np.array( ps_higher )
    ps_samples[id_z]['mean'] = ps_mean
    ps_samples[id_z]['sigma'] = ps_sigma
    ps_samples[id_z]['k_vals'] = ps_data[0]['P(k)']['k_vals']
    ps_samples[id_z]['lower'] = ps_lower
    ps_samples[id_z]['higher'] = ps_higher
    if output_trace: ps_samples[id_z]['trace'] = trace
    if params_HL is not None:
      for key in params_HL:
        p_vals = params_HL[key]
        if n_param == 3: ps_HL = Interpolate_3D(  p_vals[0], p_vals[1], p_vals[2], ps_data, 'P(k)', 'mean', SG, clip_params=True ) 
        if n_param == 4: ps_HL = Interpolate_4D(  p_vals[0], p_vals[1], p_vals[2], p_vals[3], ps_data, 'P(k)', 'mean', SG, clip_params=True ) 
        ps_samples[id_z][key] = ps_HL
  print( '\n' )
  return ps_samples
  



############################################################################################################

def get_mcmc_model( comparable_data, comparable_grid, fields_to_fit, sub_field, SG, use_covariance_matrix=False  ):
  params = SG.parameters
  n_param = len( params )
  print( f'Geting MCMC model for {n_param} parameters ')
  model, param_mcmc = None, None
  if n_param == 4:
    model, params_mcmc =  mcmc_model_4D( comparable_data, comparable_grid, fields_to_fit, 'mean', SG, use_covariance_matrix=use_covariance_matrix )
  if n_param == 3:
    model, params_mcmc =  mcmc_model_3D( comparable_data, comparable_grid, fields_to_fit, 'mean', SG, use_covariance_matrix=use_covariance_matrix )
  return model, params_mcmc  


############################################################################################################

def mcmc_model_4D( comparable_data, comparable_grid, field, sub_field, SG, use_covariance_matrix=False ):
  print( '\nRunning MCMC Sampler')
  parameters = SG.parameters
  param_ids = parameters.keys()
  params_mcmc = {}
  for param_id in param_ids:
    param_name = parameters[param_id]['name']
    param_vals = parameters[param_id]['values']
    print(f' Fitting: {param_name}  {param_vals}')
    param_min = min(param_vals)
    param_max = max(param_vals)
    param_mid = ( param_max + param_min ) / 2.
    param_mcmc = pymc.Uniform(param_name, param_min, param_max, value=param_mid )
    params_mcmc[param_id] = {}
    params_mcmc[param_id]['sampler'] = param_mcmc
    params_mcmc[param_id]['name'] = param_name
  @pymc.deterministic( plot=False )
  def mcmc_model_4D( comparable_grid=comparable_grid, SG=SG, p0=params_mcmc[0]['sampler'], p1=params_mcmc[1]['sampler'], p2=params_mcmc[2]['sampler'], p3=params_mcmc[3]['sampler']   ):
    mean_interp = Interpolate_4D( p0, p1, p2, p3, comparable_grid, field, sub_field, SG ) 
    return mean_interp
  mean  = comparable_data[field]['mean']
  sigma = comparable_data[field]['sigma']
  if use_covariance_matrix:
    print( 'WARNING: Using covariance matrix for the likelihood calculation')
    cov_matrix = comparable_data[field]['cov_matrix']
    precision_matrix = np.linalg.inv( cov_matrix )
    densObsrv = pymc.MvNormal( field, mu=mcmc_model_4D, tau=precision_matrix, value=mean, observed=True)
  else:  
    densObsrv = pymc.Normal(field, mu=mcmc_model_4D, tau=1./(sigma**2), value=mean, observed=True)
  return locals(), params_mcmc
   

############################################################################################################


def mcmc_model_3D( comparable_data, comparable_grid, field, sub_field, SG):
  print( '\nRunning MCMC Sampler')
  parameters = SG.parameters
  param_ids = parameters.keys()
  params_mcmc = {}
  for param_id in param_ids:
    param_name = parameters[param_id]['name']
    param_vals = parameters[param_id]['values']
    print(f' Fitting: {param_name}  {param_vals}')
    param_min = min(param_vals)
    param_max = max(param_vals)
    param_mid = ( param_max + param_min ) / 2.
    param_mcmc = pymc.Uniform(param_name, param_min, param_max, value=param_mid )
    params_mcmc[param_id] = {}
    params_mcmc[param_id]['sampler'] = param_mcmc
    params_mcmc[param_id]['name'] = param_name
  @pymc.deterministic( plot=False )
  def mcmc_model_3D( comparable_grid=comparable_grid, SG=SG, p0=params_mcmc[0]['sampler'], p1=params_mcmc[1]['sampler'], p2=params_mcmc[2]['sampler']   ):
    mean_interp = Interpolate_3D( p0, p1, p2, comparable_grid, field, sub_field, SG ) 
    return mean_interp
  densObsrv = pymc.Normal(field, mu=mcmc_model_3D, tau=1./(comparable_data[field]['sigma']**2), value=comparable_data[field]['mean'], observed=True)
  return locals(), params_mcmc
   
  
############################################################################################################

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
  p_vals = p_vals.flatten()
  return p_vals 

############################################################################################################


def Get_Params_mean( param_samples ):
  mean_vals = []
  for p_id in param_samples:
    trace = param_samples[p_id]['trace']
    mean_vals.append( trace.mean() )
  mean_vals = np.array( mean_vals ) 
  return mean_vals
  
############################################################################################################


def Get_1D_Likelihood_max( param_samples, n_bins_1D=100 ):
  max_vals = []
  for p_id in param_samples:
    trace = param_samples[p_id]['trace']
    hist, bin_edges = np.histogram( trace, bins=n_bins_1D ) 
    bin_centers = ( bin_edges[:-1] + bin_edges[1:] ) / 2.
    max_id = np.where( hist == hist.max() )[0][0]
    max_val = bin_centers[max_id]
    max_vals.append( max_val )
  max_vals = np.array( max_vals ) 
  return max_vals
