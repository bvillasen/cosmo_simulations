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
  
def Get_Data_Grid( fields, SG, sim_ids=None ):
  if not sim_ids: sim_ids = SG.sim_ids
  data_grid = {}
  for sim_id in sim_ids:
    data_grid[sim_id] = {}
    data_grid[sim_id]['z'] = SG.Grid[sim_id]['analysis']['z']
    for field in fields:
      data_grid[sim_id][field] = {}
      data_grid[sim_id][field]['mean'] = SG.Grid[sim_id]['analysis'][field]
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
  
def Get_Data_Grid_Composite( fields_list,  SG, z_vals=None, load_normalized_ps=False, sim_ids=None, load_uvb_rates=False ):
  # fields_list = fields.split('+')
  data_grid_all = {}
  for field in fields_list:
    if field == 'T0':    data_grid_all[field] = Get_Data_Grid( [field], SG, sim_ids=sim_ids ) 
    elif field == 'gamma': data_grid_all[field] = Get_Data_Grid( [field], SG, sim_ids=sim_ids ) 
    elif field == 'tau':   data_grid_all[field] = Get_Data_Grid( [field], SG, sim_ids=sim_ids ) 
    elif field == 'P(k)':  data_grid_all[field] = Get_Data_Grid_Power_spectrum( z_vals, SG, normalized_ps=load_normalized_ps, sim_ids=sim_ids )
    elif field == 'tau_HeII':  data_grid_all[field] = Get_Data_Grid( [field], SG, sim_ids=sim_ids ) 
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
    
def Load_Power_Spectum_Data( self, sim_id, indices ):
  input_dir = self.Get_Analysis_Directory( sim_id )
  indices.sort()
  sim_data = {}
  z_vals = []
  data_ps_mean = []
  data_kvals = []
  data_kmin, data_kmax = [], [] 
  
  for n_file in indices:
    n_file = int(n_file)
    data = load_analysis_data( n_file, input_dir, phase_diagram=False, lya_statistics=True, load_skewer=False, load_fit=False )
    z = data['cosmology']['current_z']
    k_vals  = data['lya_statistics']['power_spectrum']['k_vals']
    ps_mean = data['lya_statistics']['power_spectrum']['ps_mean']
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

def Load_Sim_Analysis_Data( self, sim_id, load_pd_fit=True, mcmc_fit_dir=None, load_thermal=False ):
  str = f' Loading Simulation Analysis: {sim_id}' 
  print_line_flush( str )
  
  input_dir = self.Get_Analysis_Directory( sim_id )
  files = [f for f in listdir(input_dir) if (isfile(join(input_dir, f)) and ( f.find('_analysis') > 0) ) ]
  indices = [ '{0:03}'.format( int(file.split('_')[0]) ) for file in files ]
  indices.sort()
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
    data = load_analysis_data( n_file, input_dir, phase_diagram=False, lya_statistics=True, load_skewer=False, load_fit=load_pd_fit, mcmc_fit_dir=mcmc_fit_dir )
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

def Load_Analysis_Data( self, sim_ids=None, load_pd_fit=True, mcmc_fit_dir=None, load_thermal=False  ):
  if sim_ids == None:  
    sim_ids = self.Grid.keys()
    indx_0 = list( sim_ids )[0]
  else: indx_0 = sim_ids[0]
  
  for sim_id in sim_ids:
    self.Load_Simulation_Analysis_Data( sim_id, load_pd_fit=load_pd_fit, mcmc_fit_dir=mcmc_fit_dir, load_thermal=load_thermal  )
  
  indices = self.Grid[indx_0]['analysis']['ps_available_indices']
  available_indices = []
  for n in indices:
    available = True
    for sim_id in sim_ids:
      if n not in self.Grid[sim_id]['analysis']['ps_available_indices']: available = False
    if available: available_indices.append( n )
  
  for sim_id in sim_ids:
    self.Load_Simulation_Power_Spectum_Data( sim_id, available_indices )
  print('\n')

