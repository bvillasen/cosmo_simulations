import sys, os, time
import numpy as np
import h5py as h5
import pymc
import pickle
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from load_tabulated_data import load_power_spectrum_table, load_data_boera, load_tabulated_data_viel, load_data_boss, load_data_irsic
from data_optical_depth_HeII import data_tau_HeII_Worserc_2019
from data_thermal_history import data_thermal_history_Gaikwad_2020a, data_thermal_history_Gaikwad_2020b
from data_optical_depth import *
from matrix_functions import Merge_Matrices, rescale_matrix



##################################################################################################################################


def Write_MCMC_Results( stats, MDL, params_mcmc,  stats_file, samples_file,  output_dir  ):
  cwd = os.getcwd()
  os.chdir( output_dir )

  f = open( stats_file, 'wb' )
  pickle.dump( stats, f)
  print ( f'Saved File: {stats_file}' )
  
  samples = {} 
  for p_id in params_mcmc.keys():
    param = params_mcmc[p_id]
    samples[p_id] = {}
    samples[p_id]['name'] = param['name']
    samples[p_id]['trace'] = param['sampler'].trace() 
  
  
  f = open( samples_file, 'wb' )
  pickle.dump( samples, f)
  print ( f'Saved File: {samples_file}' )
  os.chdir( cwd )
  return samples

##################################################################################################################################

def Get_Comparable_Power_Spectrum_from_Grid( comparable_data, SG, log_ps=False, normalized_ps=False, no_use_delta_p=False ):
  
  print( 'Generating Simulation P(k) comparable data:')
  indices = comparable_data.keys()
  comparable_grid = {}
  sim_ids = SG.sim_ids
  print_norm = True
  for sim_id in sim_ids:
    comparable_grid[sim_id] = {}  
    if normalized_ps:
      sim_data = SG.Grid[sim_id]['analysis']['power_spectrum_normalized']
      if print_norm:
        label = sim_data['normalization_key']
        print( f'Loading Normalized PS: {label}' )
        print_norm = False
    else:sim_data = SG.Grid[sim_id]['analysis']['power_spectrum']
    sim_z_all = sim_data['z']
    sim_k_vals_all = sim_data['k_vals']
    sim_ps_all = sim_data['ps_mean']
    
    sim_delta_all = []
    for index in indices:
      data = comparable_data[index]
      data_z = data['z']
      data_kvals = data['k_vals']
      data_delta_vals = data['delta_ps']
      diff = np.abs( sim_z_all - data_z )
      id_sim = np.where( diff == diff.min() )[0][0]
      sim_z = sim_z_all[id_sim]
      sim_kvals = sim_k_vals_all[id_sim]
      sim_ps = sim_ps_all[id_sim]
      sim_delta = sim_ps * sim_kvals / np.pi
      if no_use_delta_p: sim_delta = sim_ps
      if log_ps: sim_delta = np.log( sim_delta ) 
      sim_delta_interp = np.interp( data_kvals, sim_kvals, sim_delta )
      diff = ( sim_delta_interp - data_delta_vals ) / data_delta_vals
      sim_delta_all.append( sim_delta_interp )
      
    comparable_grid[sim_id]['mean'] = np.concatenate( sim_delta_all )
  n_points = len(  comparable_grid[0]['mean'] )
  print ( f' N sim points: {n_points}' )
  return comparable_grid  


##################################################################################################################################

def Get_Comparable_T0_from_Grid( comparable_data, SG ):
  return Get_Comparable_Field_from_Grid( 'T0', comparable_data, SG )

def Get_Comparable_tau_from_Grid( comparable_data, SG ):
  return Get_Comparable_Field_from_Grid( 'tau', comparable_data, SG )
  
def Get_Comparable_tau_HeII_from_Grid( comparable_data, SG ):
  return Get_Comparable_Field_from_Grid( 'tau_HeII', comparable_data, SG )

def Get_Comparable_Global_from_Grid( field, SG ):
  sim_ids = SG.sim_ids
  comparable_grid = {}
  for sim_id in sim_ids:
    comparable_grid[sim_id] = {}
    sim_analysis = SG.Grid[sim_id]['analysis']
    global_prop = sim_analysis['global_properties']
    mean = np.array([ global_prop[field] ])
    comparable_grid[sim_id]['mean'] = mean
  return comparable_grid


def Get_Comparable_Field_from_Grid( field, comparable_data, SG, interpolate=True ):
  print( f' Loading Comparabe from Grid: {field}')
  z_data = comparable_data['z']
  sim_ids = SG.sim_ids
  comparable_grid = {}
  for sim_id in sim_ids:
    comparable_grid[sim_id] = {}
    sim_analysis = SG.Grid[sim_id]['analysis']
    z_sim = sim_analysis['z']
    if interpolate:
      mean_sim = sim_analysis[field]
      if z_sim[0] > z_sim[-1]:  
        z_sim_sorted = z_sim[::-1]
        mean_sim = mean_sim[::-1]
      else: z_sim_sorted = z_sim
      mean_interp = np.interp( z_data, z_sim_sorted, mean_sim )
      comparable_grid[sim_id]['z'] = z_data
      comparable_grid[sim_id]['mean'] = mean_interp    
    else:  
      indices = []
      for z in z_data:
        diff = np.abs( z_sim - z )
        diff_min = diff.min()
        if diff_min > 0.03:
          print( f'Warning Z diff is large: diff:{diff_min}')
        indx = np.where(diff == diff_min)[0]
        indices.append( indx )
      indices = np.array( indices )
      comparable_grid[sim_id]['z'] = sim_analysis['z'][indices].flatten()
      comparable_grid[sim_id]['mean'] = sim_analysis[field][indices].flatten()    
  return comparable_grid
  

##################################################################################################################################

def Get_Comparable_Composite_from_Grid( fields, comparable_data, SG, log_ps=False, load_normalized_ps=False, no_use_delta_p=False ):
  fields_list = fields.split('+')

  sim_ids = SG.sim_ids
  comparable_grid_all = {}
  for field in fields_list:
    if field == 'T0':   comparable_grid_all[field] = Get_Comparable_T0_from_Grid(  comparable_data[field], SG )
    if field == 'tau':  comparable_grid_all[field] = Get_Comparable_tau_from_Grid( comparable_data[field], SG )
    if field == 'P(k)': comparable_grid_all[field] = Get_Comparable_Power_Spectrum_from_Grid( comparable_data[field]['separate'], SG, log_ps=log_ps, normalized_ps=load_normalized_ps, no_use_delta_p=no_use_delta_p )
    if field == 'tau_HeII':  comparable_grid_all[field] = Get_Comparable_tau_HeII_from_Grid( comparable_data[field], SG )
    if field == 'z_ion_H': comparable_grid_all[field] = Get_Comparable_Global_from_Grid( field, SG )
  comparable_grid = {}
  for sim_id in sim_ids:
    comparable_grid[sim_id] = {}
    mean_all = []
    for field in fields_list:
      if field == '': continue
      comparable_grid[sim_id][field] = comparable_grid_all[field][sim_id]
      mean_all.append( comparable_grid_all[field][sim_id]['mean'] )
    comparable_grid[sim_id][fields] = {'mean': np.concatenate( mean_all ) }
  return comparable_grid


##################################################################################################################################

def Get_Comparable_Tau_HeII( rescale_tau_HeII_sigma = 1.0, systematic_uncertainties=None, data_covariance=None, simulated_tau_HeII=None ):
  
  print( 'Loading HeII_tau Data')

  systematic = None
  if systematic_uncertainties is not None:
    systematic = {}
    for apply_uncertanty in systematic_uncertainties:
      if apply_uncertanty in [ 'all',  ]:
        for uncertanty_name in systematic_uncertainties[apply_uncertanty]:
          uncertanty_group = systematic_uncertainties[apply_uncertanty][uncertanty_name]
          for uncertanty_type in uncertanty_group:
            uncertanty = uncertanty_group[uncertanty_type]
            print( f' Applying systematic uncertanty: {uncertanty_name}: {uncertanty_type} ')
            if uncertanty_type == 'fractional':
              systematic[uncertanty_type] = uncertanty 
            
            
  comparable_z, comparable_tau, comparable_sigma = [], [], []
  data_set = data_tau_HeII_Worserc_2019
  
  if simulated_tau_HeII is not None:
    data_set = simulated_tau_HeII
    print('WARNING: Using simulated tau_HeII data')
    time.sleep(3)
  
  z   = data_set['z']
  tau = data_set['tau']
  sigma = data_set['tau_sigma'] 
  if systematic is not None:
    sigma_total_squared = sigma**2
    for systematic_type in systematic:
      if systematic_type == 'fractional':
        fraction = systematic['fractional']
        sigma_systematic = tau * fraction
        sigma_total_squared += sigma_systematic**2
        
    sigma_total = np.sqrt( sigma_total_squared )
    # print( (sigma_total - sigma) / sigma )    
    sigma = sigma_total 
    
  if rescale_tau_HeII_sigma != 1.0:
    print( f' Rescaling tau HeII sigma by {rescale_tau_HeII_sigma} ')
    sigma *= rescale_tau_HeII_sigma 
  comparable = {}
  comparable['z']     = z
  comparable['mean']  = tau
  comparable['sigma'] = sigma
  if data_covariance is not None:
    covariance_type = data_covariance['type']
    if covariance_type == 'sigma':
      n_samples = len(sigma)
      print( f' WARNING: Building tau_HeII covariance matrix from sigma only. n_samples:{n_samples}')
      cov_matrix = np.zeros( [n_samples, n_samples])
      for i in range( n_samples):
        cov_matrix[i,i] = sigma[i]**2
      comparable['covariance_matrix'] = cov_matrix
    else:
      print( f'ERROR: Covariance type {covariance_type} not implemented')
      exit(-1)  
  
  return comparable

##################################################################################################################################

def Get_Comparable_Tau( z_min, z_max, factor_sigma_tau_becker=1, factor_sigma_tau_keating=1  ):
  comparable_z, comparable_tau, comparable_sigma = [], [], []

  # Add data Becker 2013
  data_set = data_optical_depth_Becker_2013
  z   = data_set['z']
  tau = data_set['tau']
  sigma = data_set['tau_sigma'] * factor_sigma_tau_becker
  indices = z < 5
  comparable_z.append(z[indices][::2])
  comparable_tau.append(tau[indices][::2])
  comparable_sigma.append(sigma[indices][::2])

  # Add data Jiani
  # data_set = data_optical_depth_Jiani
  # z   = data_set['z']
  # tau = data_set['tau']
  # sigma = data_set['tau_sigma'] * factor_sigma_tau
  # indices = z < 4.3
  # comparable_z.append(z[indices])
  # comparable_tau.append(tau[indices])
  # comparable_sigma.append(sigma[indices])

  # Add data Bosman
  # data_set = data_optical_depth_Bosman_2018
  # z   = data_set['z']
  # tau = data_set['tau']
  # sigma = data_set['tau_sigma'] * factor_sigma_tau
  # indices = z > 4.3
  # comparable_z.append(z[indices])
  # comparable_tau.append(tau[indices])
  # comparable_sigma.append(sigma[indices])

  # Add data Bosman
  data_set = data_optical_depth_Bosman_2021
  print( data_set )
  z   = data_set['z']
  tau = data_set['tau']
  sigma = data_set['tau_sigma'] 
  indices = z <= 6.02
  comparable_z.append(z[indices])
  comparable_tau.append(tau[indices])
  comparable_sigma.append(sigma[indices])

  # # Add data Keating 2020
  # data_set = data_optical_depth_Keating_2020
  # z   = data_set['z']
  # tau = data_set['tau']
  # sigma = data_set['tau_sigma'] * factor_sigma_tau_keating
  # indices = z > 4.3
  # comparable_z.append(z[indices])
  # comparable_tau.append(tau[indices])
  # comparable_sigma.append(sigma[indices])
  z     = np.concatenate( comparable_z )
  mean  = np.concatenate( comparable_tau )
  sigma = np.concatenate( comparable_sigma )
  indices = ( z >= z_min ) * ( z <= z_max )
  comparable = {}
  comparable['z']     = z[indices]
  comparable['mean']  = mean[indices]
  comparable['sigma'] = sigma[indices]
  return comparable

##################################################################################################################################

def Get_Comparable_T0_Gaikwad():
  print( 'Loading T0 Data: ')
  data_sets = [ data_thermal_history_Gaikwad_2020b, data_thermal_history_Gaikwad_2020a ]
  z = np.concatenate( [ds['z'] for ds in data_sets ])
  data_mean  = np.concatenate( [ds['T0'] for ds in data_sets ])
  data_sigma = np.concatenate( [( ds['T0_sigma_plus'] + ds['T0_sigma_minus'] )*0.5  for ds in data_sets ] )
  comparable = {}
  comparable['z'] = z
  comparable['mean'] = data_mean
  comparable['sigma'] = data_sigma
  print( f' N data points: {len(data_mean)} ' )
  return comparable

##################################################################################################################################

def Get_Comparable_Power_Spectrum( ps_data_dir, z_min, z_max, data_sets, ps_range, verbose=False, log_ps=False, systematic_uncertainties=None, print_systematic=False, 
                                   no_use_delta_p=False,  simulated_data_param=None, data_covariance=None, simulated_data=None, simulated_ps=None ):
  print( f'Loading P(k) Data:' )
  dir_boss = ps_data_dir + 'data_power_spectrum_boss/'
  data_boss = load_data_boss( dir_boss )
  
  dir_irsic = ps_data_dir + 'data_power_spectrum_irsic_2017/'
  data_irsic = load_data_irsic( dir_irsic, print_out=verbose )

  data_filename = ps_data_dir + 'data_power_spectrum_walther_2019/data_table.txt'
  data_walther = load_power_spectrum_table( data_filename )

  dir_data_boera = ps_data_dir + 'data_power_spectrum_boera_2019/'
  data_boera = load_data_boera( dir_data_boera, corrected=False, print_out=verbose )
  data_boera_c = load_data_boera( dir_data_boera, corrected=True, print_out=verbose )
  
  data_dir_viel = ps_data_dir + 'data_power_spectrum_viel_2013/'
  data_viel = load_tabulated_data_viel( data_dir_viel)
  
  data_dir = { 'Boss':data_boss, 'Walther':data_walther, 'Boera':data_boera, 'Viel':data_viel, 'Irsic':data_irsic, 'BoeraC':data_boera_c }
  
  if simulated_ps is not None:
    data_dir_simulated = {}
    for data_name in data_sets:
      print( f'Using simulated data sampled as: {data_name}' )
      data_dir_simulated[data_name] = simulated_ps[data_name]
    print( 'WARNING: Using Simulated P(k) data')
    time.sleep(3)
    data_dir = data_dir_simulated
      
      
  if simulated_data_param is not None:
    data_file_name = simulated_data_param['data_file_name']
    simulated_data = Load_Pickle_Directory( data_file_name )
    data_dir['Simulated'] = simulated_data
    
  if data_covariance is not None:  print( ' WARNING: Loading Data Covariance Matrices')
  
  data_kvals, data_ps, data_ps_sigma, data_indices, data_z  = [], [], [], [], []
  covariance_matrices = []  
  sim_z, sim_kmin, sim_kmax = ps_range['z'], ps_range['k_min'], ps_range['k_max']
  systematic = None
  if systematic_uncertainties is not None:
    systematic = {}
    for apply_uncertanty in systematic_uncertainties:
      if apply_uncertanty in [ 'all', 'P(k)' ]:
        for uncertanty_name in systematic_uncertainties[apply_uncertanty]:
          if uncertanty_name in ['modify_diagonal_only']: continue
          uncertanty_group = systematic_uncertainties[apply_uncertanty][uncertanty_name]
          if uncertanty_name == 'resolution':
            resolution_file_name = uncertanty_group['file_name']
            resolution_correction = Load_Pickle_Directory( resolution_file_name )
            uncertanty_type = uncertanty_group['type']
            print( f' Applying systematic uncertanty: {uncertanty_name}: {uncertanty_type} ')
            systematic['resolution'] = {'correction':resolution_correction, 'type':uncertanty_type }
          else:  
            for uncertanty_type in uncertanty_group:
              uncertanty = uncertanty_group[uncertanty_type]
              print( f' Applying systematic uncertanty: {uncertanty_name}: {uncertanty_type} {uncertanty}')
              if uncertanty_type == 'fractional':
                systematic[uncertanty_type] = uncertanty 
              
  ps_data = {}
  data_id = 0
  for data_index, data_name in enumerate(data_sets):
    print( f' Loading P(k) Data: {data_name}' )
    data_set = data_dir[data_name]
    covariance_type = None
    covariance_matrix_global = None
    if data_covariance is not None and data_name in data_covariance['type']:
      covariance_type = data_covariance['type'][data_name]
      cross_elements_factor = data_covariance['cross_elements_factor'][data_name]
      sigma_factor = data_covariance['sigma_factor'][data_name]
      print( f' Loading Covariance Matrix: {covariance_type}  cross_elements_factor: {cross_elements_factor}  sigma_factor: {sigma_factor}')
      if covariance_type == 'global':  covariance_matrix_global = data_set['full_covariance']
       
      
    keys = data_set.keys()
    cov_matrix_local = None
    for index in keys:
      if index in ['k_vals', 'z_vals', 'full_covariance']: continue
      data = data_set[index]
      z = data['z']
      adjust_covariance_size = False
      if z >= z_min and z <= z_max:
        diff = np.abs( sim_z - z )
        id_min = np.where( diff == diff.min() )[0][0]
        z_sim = sim_z[id_min]
        kmin = sim_kmin[id_min]
        kmax = sim_kmax[id_min]
        k_vals = data['k_vals']
        k_indices = np.where( (k_vals >= kmin) & (k_vals <= kmax) )
        if len(k_indices[0]) != len(k_vals):
          if verbose: print( f' WARNING: Not all k values are loaded n_k:{len(k_vals)}  n_loaded:{len(k_indices[0])}')
          adjust_covariance_size = True
        k_vals = k_vals[k_indices]
        delta_ps = data['delta_power'][k_indices]
        delta_ps_sigma = data['delta_power_error'][k_indices]
        if covariance_type == 'local' and not no_use_delta_p:
          print('ERROR: Covariance Matrix only available when fitting P(k) not Delta(Kk')
          exit(-1)
          
        if no_use_delta_p:
          # Use P(k) instead of Delta_P(k)
          if verbose: print( f' Adjusting covariance matrix')
          if verbose: print( 'WARNING: Using P(k) instead of Delta_P(k)' )
          delta_ps = delta_ps / k_vals * np.pi
          delta_ps_sigma = delta_ps_sigma / k_vals * np.pi
          if covariance_type == 'local': 
            cov_matrix_local = data['covariance_matrix']
            if adjust_covariance_size:
              n_samples = len(k_indices[0])
              cov_matrix_adjusted = np.zeros([n_samples, n_samples])
              for i in range(n_samples):
                for j in range(n_samples):
                  indx_i, indx_j = k_indices[0][i], k_indices[0][j]
                  cov_matrix_adjusted[i,j] = cov_matrix_local[indx_i, indx_j]
              cov_matrix_local = cov_matrix_adjusted
            ny, nx = cov_matrix_local.shape
            if len(k_vals) != ny: 
              print( 'ERROR: P(k) vector does not have the same size as covariance matrix')
              exit(-1) 
        
        # if data_name == 'Walther' and rescaled_walther:
        #   rescale_z = rescale_walter_alphas[index]['z']
        #   rescale_alpha = rescale_walter_alphas[index]['alpha']
        #   print( f'  Rescaling z={rescale_z:.1f}    alpha={rescale_alpha:.3f} ')
        #   delta_ps *= rescale_alpha
        
        if systematic is not None:
          sigma_total_squared = delta_ps_sigma**2
          for systematic_type in systematic:
            if systematic_type == 'fractional':
              fraction = systematic['fractional']
              sigma_systematic = delta_ps * fraction
              sigma_total_squared += sigma_systematic**2
              if print_systematic: print( f'{systematic_type} Fraction:{fraction}  :  {sigma_systematic/ delta_ps_sigma}' )
            if systematic_type == 'resolution':
              correction_type = systematic['resolution']['type']
              correction_all = systematic['resolution']['correction']
              z_vals = correction_all['z_vals']
              z_diff = np.abs( z_vals - z )
              if z_diff.min( ) > 5e-2:
                print( f'Large z difference when applying resolution sigma: {z_diff.min()} ')
              z_indx = np.where( z_diff == z_diff.min() )[0]
              if len( z_indx ) > 1 : 
                print( 'WARNING: Multiple z_indices')
                exit(-1)
              correction = correction_all[z_indx[0]]
              # print( correction.keys())
              correction_k = correction['k_vals']
              correction_delta = np.abs(correction['delta']) * correction_k / np.pi
              correction_fractional = correction['delta_fraction']
              if correction_type == 'delta':
                sigma_correction = np.interp( k_vals, correction_k, correction_delta )
                if print_systematic: print( f'{systematic_type}: {sigma_correction / delta_ps_sigma}' )
              else: 
                print('Type of correction not implemented')
                exit(-1) 
              sigma_total_squared += sigma_correction**2
              
              
          sigma_total = np.sqrt( sigma_total_squared )
          # print( (sigma_total - delta_ps_sigma) / delta_ps_sigma )    
          delta_ps_sigma = sigma_total 
          
          
        ps_data[data_id] = {'z':z, 'k_vals':k_vals, 'delta_ps':delta_ps, 'delta_ps_sigma':delta_ps_sigma }
    
        data_z.append( z )
        data_kvals.append( k_vals )
        data_ps.append( delta_ps )
        data_ps_sigma.append( delta_ps_sigma )

        #Append covariance matrix
        if cov_matrix_local is not None: 
          cov_matrix_local = rescale_matrix( cov_matrix_local, cross_elements_factor, 'cross_only')
          cov_matrix_local *= sigma_factor**2
          print( f'Multiplied local covariance matrix by sigma factor: {sigma_factor}' )
          covariance_matrices.append(cov_matrix_local) 
          ps_data[data_id]['cov_matrix'] = cov_matrix_local
          
        data_id += 1
    if covariance_matrix_global is not None: 
      covariance_matrix_global = rescale_matrix( covariance_matrix_global, cross_elements_factor, 'cross_only')
      covariance_matrix_global *= sigma_factor**2
      print( f'Multiplied global covariance matrix by sigma factor: {sigma_factor}' )
      covariance_matrices.append(covariance_matrix_global) 
  
  k_vals_all         = np.concatenate( data_kvals )
  delta_ps_all       = np.concatenate( data_ps )
  delta_ps_sigma_all = np.concatenate( data_ps_sigma )
  ps_data_out = {'P(k)':{}, 'separate':ps_data }
  ps_data_out['P(k)']['k_vals'] = k_vals_all
  ps_data_out['P(k)']['mean']   = delta_ps_all
  ps_data_out['P(k)']['sigma']  = delta_ps_sigma_all
  if len(covariance_matrices) > 0:
    print( f'Loaded {len(covariance_matrices)} covariance matrices')
    cov_matrices_all = Merge_Matrices( covariance_matrices )
    # Rescaale to reflect the systematic error added to sigma
    n = cov_matrices_all.shape[0]
    diagonal = cov_matrices_all.diagonal()
    sigma = delta_ps_sigma_all
    diagonal_only = False
    if  systematic_uncertainties is not None and 'modify_diagonal_only' in systematic_uncertainties['P(k)']  and systematic_uncertainties['P(k)']['modify_diagonal_only']: 
      diagonal_only = True
      print( ' WARNING: Systematic uncertainties modyfy only the diagonal of the covariance matrix')
      for i in range(n):
        for j in range(n):
          if diagonal_only and i != j: continue
          sigma_0 = np.sqrt(diagonal[i] * diagonal[j])
          sigma_1 = sigma[i] * sigma[j]
          cov_matrices_all[i,j] *= sigma_1 / sigma_0 
      cov_matrices_all *= sigma_factor**2
    ps_data_out['P(k)']['covariance_matrix']  = cov_matrices_all
  n_data_points = len( k_vals_all )
  print( f' N data points: {n_data_points}' )
  return ps_data_out


##################################################################################################################################

def Get_Comparable_Composite( fields, z_min, z_max, verbose=False, ps_parameters=None, tau_parameters=None, log_ps=False, 
                              z_reion=None, factor_sigma_tauHeII=1.0, systematic_uncertainties=None, no_use_delta_p=False,  
                              simulated_data_param=None, data_covariance=None, simulated_data=None  ):
  
  rescaled_walther = False
  rescale_walter_file = None
  if ps_parameters is not None:
    ps_data_dir = ps_parameters['data_dir']
    data_ps_sets = ps_parameters['data_sets'] 
    ps_range = ps_parameters['range']

  factor_sigma_tau_becker  = 1.0
  factor_sigma_tau_keating = 1.0
  if tau_parameters is not None:
    factor_sigma_tau_becker  = tau_parameters['factor_sigma_becker']
    factor_sigma_tau_keating = tau_parameters['factor_sigma_keating']
    
  fields_list = fields.split('+')
  mean_all, sigma_all = [], []
  comparable_all = {}
  covariance_matrices = []
  for field in fields_list:
    append_comparable = False
    if field == 'P(k)':
      if data_covariance is not None and 'P(k)' in data_covariance: pk_data_covariance = data_covariance['P(k)']
      else: pk_data_covariance = None
      simulated_ps = None
      if simulated_data is not None and 'P(k)' in simulated_data: simulated_ps = simulated_data['P(k)']
      comparable_ps = Get_Comparable_Power_Spectrum( ps_data_dir, z_min, z_max, data_ps_sets, ps_range, verbose=verbose, log_ps=log_ps, systematic_uncertainties=systematic_uncertainties, no_use_delta_p=no_use_delta_p,  simulated_data_param=simulated_data_param, data_covariance=pk_data_covariance, simulated_ps=simulated_ps  )
      comparable_ps_all = comparable_ps['P(k)']
      comparable_ps_separate = comparable_ps['separate']
      comparable_all['P(k)'] = { 'all':comparable_ps_all, 'separate':comparable_ps_separate }
      print('Added comparable P(k) separate')
      mean_all.append( comparable_ps_all['mean'] )
      sigma_all.append( comparable_ps_all['sigma'] )
      if 'covariance_matrix' in comparable_ps_all: 
        covariance_matrices.append(comparable_ps_all['covariance_matrix'])
    if field == 'T0':  
      comparable_field = Get_Comparable_T0_Gaikwad()
      append_comparable = True
    if field == 'tau': 
      comparable_field = Get_Comparable_Tau( z_min, z_max, factor_sigma_tau_becker=factor_sigma_tau_becker, factor_sigma_tau_keating=factor_sigma_tau_keating )
      append_comparable = True
    if field == 'tau_HeII': 
      tau_data_covariance = None
      simulated_tau_HeII = None
      if data_covariance is not None and 'tau_HeII' in data_covariance: tau_data_covariance = data_covariance['tau_HeII']
      if simulated_data is not None and 'tau_HeII' in simulated_data: simulated_tau_HeII = simulated_data['tau_HeII']
      comparable_field = Get_Comparable_Tau_HeII( rescale_tau_HeII_sigma=factor_sigma_tauHeII,  systematic_uncertainties=systematic_uncertainties, data_covariance=tau_data_covariance, simulated_tau_HeII=simulated_tau_HeII )
      append_comparable = True
    if field == 'z_ion_H':
      mean  = np.array([z_reion['z']])
      sigma = np.array([z_reion['sigma']])
      comparable_field = { 'mean':mean, 'sigma':sigma }
      # print( f'Comaparable z_ion_H: {comparable_field}' )
      append_comparable = True
    if append_comparable:
      comparable_all[field] = comparable_field
      mean_all.append( comparable_field['mean'] )
      sigma_all.append( comparable_field['sigma'] )
      if 'covariance_matrix' in comparable_field: covariance_matrices.append( comparable_field['covariance_matrix'])
  comparable_all[fields] = { 'mean':np.concatenate(mean_all), 'sigma':np.concatenate(sigma_all) }  
  if len( covariance_matrices ) > 0:
     cov_matrix_all = Merge_Matrices( covariance_matrices )
     comparable_all[fields]['covariance_matrix'] = cov_matrix_all
  return comparable_all
  
