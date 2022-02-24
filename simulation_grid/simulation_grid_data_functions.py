import os, sys
from pathlib import Path
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools')
from tools import *
from load_data import load_analysis_data

  

####################################################################################################################

def Get_Data_Grid_Power_spectrum( z_vals, SG, normalized_ps=False, sim_ids=None ):
  data_grid = {}
  print_norm = True
  for id_z, z_val in enumerate( z_vals ):
    data_grid[id_z] = {}
    data_grid[id_z]['z'] = z_val
    if not sim_ids: sim_ids = SG.sim_ids
    for sim_id in sim_ids:
      if normalized_ps:
        sim_ps_data = SG.Grid[sim_id]['analysis']['power_spectrum_normalized']
        label = sim_ps_data['normalization_key']
        if print_norm: print( f'Loading Normalized: {label}' )
        print_norm = False 
      else: sim_ps_data = SG.Grid[sim_id]['analysis']['power_spectrum']
      sim_z_vals = sim_ps_data['z']
      diff_z = np.abs( sim_z_vals - z_val )
      diff_min = diff_z.min()
      if diff_min > 0.05: print( f'Warning: Large Z difference: {diff_min}')
      index = np.where( diff_z == diff_min )[0][0]
      k_vals = sim_ps_data['k_vals'][index]
      ps_vals = sim_ps_data['ps_mean'][index]
      delta_ps = ps_vals * k_vals / np.pi
      data_grid[id_z][sim_id] = { 'P(k)':{} } 
      data_grid[id_z][sim_id]['P(k)']['mean'] = delta_ps
      data_grid[id_z][sim_id]['P(k)']['k_vals'] = k_vals
  return data_grid


####################################################################################################################
def Get_Data_Grid_Global( fields, SG, sim_ids=None ):
  if not sim_ids: sim_ids = SG.sim_ids
  data_grid = {}
  for sim_id in sim_ids:
    data_grid[sim_id] = {}
    for field in fields:
      data_grid[sim_id][field] = {}
      data_grid[sim_id][field]['mean'] = SG.Grid[sim_id]['analysis']['global_properties'][field]
  return data_grid

####################################################################################################################
  
def Get_Data_Grid( fields, SG, sim_ids=None, z_fields_min=None ):
  if not sim_ids: sim_ids = SG.sim_ids
  data_grid = {}
  for sim_id in sim_ids:
    data_grid[sim_id] = {}
    z = SG.Grid[sim_id]['analysis']['z']
    if z_fields_min is not None:
      z_indices = z >= z_fields_min
      z = z[z_indices]
    data_grid[sim_id]['z'] = z
    for field in fields:
      data_grid[sim_id][field] = {}
      field_mean = SG.Grid[sim_id]['analysis'][field]
      if z_fields_min is not None:
        field_mean = field_mean[z_indices]
      data_grid[sim_id][field]['mean'] = field_mean
  return data_grid

####################################################################################################################

def Get_Data_Grid_thermal( fields, SG, sim_ids=None ):
  if not sim_ids: sim_ids = SG.sim_ids
  data_grid = {}
  for sim_id in sim_ids:
    data_grid[sim_id] = {}
    data_grid[sim_id]['z'] = SG.Grid[sim_id]['analysis']['thermal']['z']
    for field in fields:
      data_grid[sim_id][field] = {}
      data_grid[sim_id][field]['mean'] = SG.Grid[sim_id]['analysis']['thermal'][field]
  return data_grid
####################################################################################################################
  
def Get_Data_Grid_Composite( fields_list,  SG, z_vals=None, load_normalized_ps=False, sim_ids=None, load_uvb_rates=False, z_fields_min=None, files_to_load=None ):
  # fields_list = fields.split('+')
  data_grid_all = {}
  for field in fields_list:
    if field == 'T0':    data_grid_all[field] = Get_Data_Grid( [field], SG, sim_ids=sim_ids, z_fields_min=z_fields_min ) 
    elif field == 'gamma': data_grid_all[field] = Get_Data_Grid( [field], SG, sim_ids=sim_ids, z_fields_min=z_fields_min ) 
    elif field == 'tau':   data_grid_all[field] = Get_Data_Grid( [field], SG, sim_ids=sim_ids, z_fields_min=z_fields_min ) 
    elif field == 'P(k)':  data_grid_all[field] = Get_Data_Grid_Power_spectrum( z_vals, SG, normalized_ps=load_normalized_ps, sim_ids=sim_ids )
    elif field == 'tau_HeII':  data_grid_all[field] = Get_Data_Grid( [field], SG, sim_ids=sim_ids, z_fields_min=z_fields_min ) 
    elif field == 'z_ion_H':  data_grid_all[field] = Get_Data_Grid_Global( [field], SG, sim_ids=sim_ids ) 
    elif field == 'HI_frac':  data_grid_all[field] = Get_Data_Grid_thermal( [field], SG, sim_ids=sim_ids )
    elif field == 'n_e':  data_grid_all[field] = Get_Data_Grid_thermal( [field], SG, sim_ids=sim_ids ) 
    else: print( f'Field not recognized: {field}' )
  data_grid = {}
  if not sim_ids: sim_ids = SG.sim_ids
  
  for sim_id in sim_ids:  
    data_grid[sim_id] = {}
    for field in fields_list:
     if field == 'P(k)' or field == '': continue
     if field in [ 'z_ion_H' ]:
       mean = data_grid_all[field][sim_id][field]['mean']
       data_grid[sim_id][field] = {'mean':mean }
     else:
       z = data_grid_all[field][sim_id]['z']
       mean = data_grid_all[field][sim_id][field]['mean']
       data_grid[sim_id][field] = {'mean':mean, 'z':z }

  if load_uvb_rates:
    photoheating_keys    = [ 'piHI', 'piHeI', 'piHeII' ]
    photoionization_keys = [ 'k24', 'k25', 'k26' ]

    key_names = { 'piHI': 'photoheating_HI',   'piHeI': 'photoheating_HeI',  'piHeII': 'photoheating_HeII', 
    'k24': 'photoionization_HI', 'k26': 'photoionization_HeI', 'k25': 'photoionization_HeII' }
     
    for sim_id in sim_ids:
      for key in photoheating_keys:
        z = SG.Grid[sim_id]['UVB_rates']['z']
        rates = SG.Grid[sim_id]['UVB_rates']['Photoheating'][key]
        key_name = key_names[key]
        data_grid[sim_id][key_name] = {}
        data_grid[sim_id][key_name]['mean'] = rates
        data_grid[sim_id][key_name]['z'] = z
        
      for key in photoionization_keys:
        z = SG.Grid[sim_id]['UVB_rates']['z']
        rates = SG.Grid[sim_id]['UVB_rates']['Chemistry'][key]
        key_name = key_names[key]
        data_grid[sim_id][key_name] = {}
        data_grid[sim_id][key_name]['mean'] = rates
        data_grid[sim_id][key_name]['z'] = z
    
  if 'P(k)' in fields_list:  return data_grid, data_grid_all['P(k)']
  else:                      return data_grid


####################################################################################################################
    

def Get_PS_Range( self, sim_id=0, kmin=None, kmax=None ):
  data_ps = self.Grid[sim_id]['analysis']['power_spectrum']
  z = data_ps['z']
  k_min = data_ps['k_min']
  k_max = data_ps['k_max']
  if kmin != None: k_min = np.array([ max( k_min_i, kmin ) for k_min_i in k_min ]) 
  if kmax != None: k_max = np.array([ min( k_max_i, kmax ) for k_max_i in k_max ])
  ps_range = { 'z':z, 'k_min':k_min, 'k_max':k_max }
  return ps_range


####################################################################################################################
    
def Load_Power_Spectum_Data( self, sim_id, indices, FPS_correction=None, custom_data=None ):
  input_dir = self.Get_Analysis_Directory( sim_id )
  indices.sort()
  sim_data = {}
  z_vals = []
  data_ps_mean = []
  data_kvals = []
  data_kmin, data_kmax = [], [] 
  data_cov_matrices = []
  # print( f'Loading power spectrum sim_id: {sim_id}'  )
  
  if custom_data is not None:
    custom_dir = custom_data['root_dir']
    custom_file_base_name = custom_data['file_base_name']
    stats_file_base_name = custom_data['stats_base_name']
    
    sim_key = self.Grid[sim_id]['key']
    custom_input_dir =  f'{custom_dir}/{sim_key}/' 
    # print( f'Loading custom P(k): {custom_input_dir}')
    custom_ps_files = [ f for f in os.listdir(custom_input_dir) if custom_file_base_name in f ]
    custom_file_indices = [ int( (f.split('_')[-1]).split('.')[0] ) for f in custom_ps_files  ]
    custom_file_indices.sort()
    for file_indx in custom_file_indices:
      file_name = f'{custom_file_base_name}_{file_indx:03}.h5'
      ps_file = h5.File( custom_input_dir + file_name, 'r' )
      z = ps_file.attrs['current_z']
      k_vals = ps_file['k_vals'][...]
      ps_mean = ps_file['ps_mean'][...]
      ps_file.close()
      
      if stats_file_base_name is not None:
        stats_file_name = f'{stats_file_base_name}_{file_indx:03}.pkl'
        stats = Load_Pickle_Directory( custom_input_dir + stats_file_name, print_out=False )
        stats_z = stats['current_z']
        if np.abs( stats_z - z ) > 1e-10: print( 'ERROR: Redshift mismatch from stats and ps file')
        ps_sigma = stats['sigma']
        cov_matrix = stats['covariance_matrix']
        sigma_diff = np.abs( ( np.sqrt( cov_matrix.diagonal() ) - ps_sigma ) / ps_sigma )
        if ( sigma_diff > 1e-10 ).any(): print( 'ERROR: Sigma and covariance diagonal mismatch')
        stats_k = stats['k_vals']
        k_diff = np.abs( stats_k - k_vals ) / k_vals
        if ( sigma_diff > 1e-10 ).any(): print( 'ERROR: K vals mismatch from stats and P(k) file')
        stats_ps = stats['ps_mean']
        ps_diff = np.abs( stats_ps - ps_mean ) / ps_mean
        if ( sigma_diff > 1e-10 ).any(): print( 'ERROR: P(k) mean mismatch from stats and P(k) file')
        dsata_cov_matrices.append( cov_matrix)
    
      z_vals.append(z)
      data_kvals.append( k_vals )
      data_ps_mean.append( ps_mean )
      data_kmin.append( k_vals.min() )
      data_kmax.append( k_vals.max() )
    z_vals = np.array( z_vals )
    data_kmin, data_kmax = np.array( data_kmin ), np.array( data_kmax )
    data_ps = { 'z':z_vals, 'k_min':data_kmin, 'k_max':data_kmax, 'k_vals':data_kvals, 'ps_mean':data_ps_mean }
    if stats_file_base_name is not None: data_ps['covariance_matrix'] = data_cov_matrices 
    self.Grid[sim_id]['analysis']['power_spectrum'] = data_ps
    return
      
  if FPS_correction is not None:
    correction_z_vals = FPS_correction['z_vals'] 
  
  for n_file in indices:
    n_file = int(n_file)
    data = load_analysis_data( n_file, input_dir, phase_diagram=False, lya_statistics=True, load_skewer=False, load_fit=False )
    z = data['cosmology']['current_z']
    k_vals  = data['lya_statistics']['power_spectrum']['k_vals']
    ps_mean = data['lya_statistics']['power_spectrum']['ps_mean']
    if FPS_correction is not None:
      z_diff = np.abs( correction_z_vals - z )
      if z_diff.min() < 5e-2:  
        z_indx = np.where( z_diff == z_diff.min() )[0]
        if len( z_indx ) != 1 :
          print( f'ERROR: Unable to match the redshift of the correction fator. {z} -> {correction_z_vals[z_indx]}  ')
          exit(-1)
        z_indx = z_indx[0]
        correction = FPS_correction[z_indx]
        correction_k_vals = correction['k_vals']
        correction_ps_factor = correction['delta_factor']
        indices = correction_ps_factor > 1
        new =  correction_ps_factor[indices] - 1
        correction_ps_factor[indices] = 1 + new * 4
        k_diff = np.abs( k_vals - correction_k_vals )
        # print( f'{z} {correction_ps_factor}')
        if k_diff.sum() > 1e-6:
           print(f'ERROR: Large k difference for FPS correction: {k_diff.sum()}.')
           exit(-1)
        ps_mean = ps_mean / correction_ps_factor
        if ( ps_mean < 0 ).sum() > 0:
          print( f'Negative Power Spectrum: {ps_mean}')
          exit()
    
    z_vals.append(z)
    data_kvals.append( k_vals )
    data_ps_mean.append( ps_mean )
    data_kmin.append( k_vals.min() )
    data_kmax.append( k_vals.max() )
  z_vals = np.array( z_vals )
  data_kmin, data_kmax = np.array( data_kmin ), np.array( data_kmax )
  data_ps = { 'z':z_vals, 'k_min':data_kmin, 'k_max':data_kmax, 'k_vals':data_kvals, 'ps_mean':data_ps_mean }
  self.Grid[sim_id]['analysis']['power_spectrum'] = data_ps
  
    
####################################################################################################################

def Load_Sim_Analysis_Data( self, sim_id, load_pd_fit=True, mcmc_fit_dir=None, load_thermal=False, files_to_load=None, custom_data=None, load_phase_diagram=False ):
  str = f' Loading Simulation Analysis: {sim_id}' 
  print_line_flush( str )
  
  input_dir = self.Get_Analysis_Directory( sim_id )
  files = [f for f in listdir(input_dir) if (isfile(join(input_dir, f)) and ( f.find('_analysis') > 0) ) ]
  indices = [ '{0:03}'.format( int(file.split('_')[0]) ) for file in files ]
  indices.sort()
  if files_to_load is not None: indices = files_to_load
  n_files = len( files )
  sim_data = {}
  
  sim_data['z']      = []
  sim_data['T0']     = []
  sim_data['gamma']  = []
  sim_data['F_mean'] = []
  sim_data['tau'] = []
  sim_data['tau_HeII'] = []
  sim_data['ps_mean']  = []
  sim_data['ps_kvals'] = []
  z_power_spectrum = []
  data_ps_mean = []
  data_kvals = []
  data_kmin, data_kmax = [], []
  ps_available_indices = []
  
  for n_file in indices:
    n_file = int(n_file)
    data = load_analysis_data( n_file, input_dir, phase_diagram=load_phase_diagram, lya_statistics=True, load_skewer=False, load_fit=load_pd_fit, mcmc_fit_dir=mcmc_fit_dir )
    z = data['cosmology']['current_z']
    if load_pd_fit:
      T0 =    data['phase_diagram']['fit']['T0']
      gamma = data['phase_diagram']['fit']['gamma']
    F_mean = data['lya_statistics']['Flux_mean']
    tau = data['lya_statistics']['tau']
    tau_HeII = data['lya_statistics']['tau_HeII']
    k_vals  = data['lya_statistics']['power_spectrum']['k_vals']
    ps_mean = data['lya_statistics']['power_spectrum']['ps_mean']
    if ps_mean is not None and z < 5.5:
      ps_available_indices.append(n_file)
    sim_data['ps_kvals'].append( k_vals )
    sim_data['ps_mean'].append( ps_mean )
    sim_data['z'].append(z)
    if load_pd_fit:
      sim_data['T0'].append(T0)
      sim_data['gamma'].append(gamma)
    sim_data['F_mean'].append(F_mean)
    sim_data['tau'].append(tau)
    sim_data['tau_HeII'].append(tau_HeII)
  sim_data['z'] = np.array( sim_data['z'] )
  if load_pd_fit:
    sim_data['T0'] = np.array( sim_data['T0'] )
    sim_data['gamma'] = np.array( sim_data['gamma'] )
  sim_data['F_mean'] = np.array( sim_data['F_mean'] )
  sim_data['tau'] = np.array( sim_data['tau'] )
  sim_data['tau_HeII'] = np.array( sim_data['tau_HeII'] )  
  sim_data['ps_available_indices'] = ps_available_indices
  if load_thermal:
    sim_dir = self.Get_Simulation_Directory(sim_id)
    thermal_dir = sim_dir + 'thermal_solution/'
    file_name = thermal_dir + 'global_properties.pkl'
    global_properties = Load_Pickle_Directory( file_name, print_out=False )
    sim_data['global_properties'] = global_properties
    solution = h5.File( thermal_dir + 'solution.h5', 'r'  )
    n_stride = 100
    z = solution['z'][...][::n_stride]
    # print( solution.keys())
    nH = solution['n_H'][...][::n_stride]
    nHI = solution['n_HI'][...][::n_stride]
    HI_frac = nHI / nH 
    HI_frac[HI_frac > 1.0] = 1.0
    HI_frac[HI_frac < 1e-10] = 1e-10 
    ne = solution['n_e'][...][::n_stride]
    thermal = { 'z':z, 'HI_frac':HI_frac,  'n_e':ne }
    sim_data['thermal'] = thermal
  self.Grid[sim_id]['analysis'] = sim_data


####################################################################################################################

def Load_Analysis_Data( self, sim_ids=None, load_pd_fit=True, mcmc_fit_dir=None, load_thermal=False, FPS_correction=None, files_to_load=None, custom_data=None, load_phase_diagram=False  ):
  if sim_ids == None:  
    sim_ids = self.Grid.keys()
    indx_0 = list( sim_ids )[0]
  else: indx_0 = sim_ids[0]
  
  custom_ps_data = None
  if custom_data is not None and 'P(k)' in custom_data:
    custom_ps_data = custom_data['P(k)']
    print( f' WARNING: Loading custom P(k) data: \n  Dir: {custom_ps_data["root_dir"]} \n  file_base_name: {custom_ps_data["file_base_name"]}' )
  
  
  for sim_id in sim_ids:
    self.Load_Simulation_Analysis_Data( sim_id, load_pd_fit=load_pd_fit, mcmc_fit_dir=mcmc_fit_dir, load_thermal=load_thermal, files_to_load=files_to_load, custom_data=custom_data, load_phase_diagram=load_phase_diagram  )
  
  indices = self.Grid[indx_0]['analysis']['ps_available_indices']
  available_indices = []
  for n in indices:
    available = True
    for sim_id in sim_ids:
      if n not in self.Grid[sim_id]['analysis']['ps_available_indices']: available = False
    if available: available_indices.append( n )
  
  print('')
  if FPS_correction is not None:
    print( ' WARNING: Applying correction factor to FPS. ')
  for sim_id in sim_ids:
    print_line_flush( f' Loading Flux Power Spectrum: {sim_id} ')
    
    self.Load_Simulation_Power_Spectum_Data( sim_id, available_indices, FPS_correction=FPS_correction, custom_data=custom_ps_data )
  print('\n')

