import os, sys
import numpy as np
import h5py as h5
from scipy.interpolate import interp1d
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from constants_cosmo import eV_to_ergs


def sigmoid( x, alpha=1, x0=0 ):
  sig = 1 / ( 1 + np.exp( -alpha * (x + x0) ))
  return sig

def  Modify_UVB_Rates_sigmoid( uvb_rates, z_range, alpha, x0 ):
  rates_sigma = Copy_Grakle_UVB_Rates( uvb_rates )
  z_min = min( z_range )
  z_max = max( z_range )
  z = rates_sigma['UVBRates']['z']
  indices_to_change = np.where( (z>= z_min) * (z<=z_max) )[0]
  chem_key = 'k24'
  for chem_key in [ 'k24', 'k26' ]:  
    if chem_key == 'k24': heat_key = 'piHI'
    if chem_key == 'k26': heat_key = 'piHeI'
    gamma = rates_sigma['UVBRates']['Chemistry'][chem_key]
    heat  = rates_sigma['UVBRates']['Photoheating'][heat_key]
    z_mod = z[indices_to_change[0]-1:indices_to_change[-1]+2]
    gamma_mod = gamma[indices_to_change[0]-1:indices_to_change[-1]+2]
    zmax = z_mod.max()
    x = np.abs(z_mod - zmax)
    gamma_l = np.log10(gamma_mod[0])
    gamma_r = np.log10(gamma_mod[-1])
    delta_gamma = gamma_l - gamma_r
    sig = sigmoid( x, alpha=alpha, x0=x0 )
    sig -= sig.min()
    sig_res = sig / sig.max() * delta_gamma + gamma_r
    sig_res = 10**sig_res
    gamma[indices_to_change[0]-1:indices_to_change[-1]+2] = sig_res
    gamma_0 = uvb_rates['UVBRates']['Chemistry'][chem_key]
    heat_0  = uvb_rates['UVBRates']['Photoheating'][heat_key]
    heat = heat_0 * gamma / gamma_0
    rates_sigma['UVBRates']['Chemistry'][chem_key] = gamma
    rates_sigma['UVBRates']['Photoheating'][heat_key] = heat
  return rates_sigma
  
def Modify_Gamma_sigmoid(  z, gamma, z_range, alpha, x0 ):
  z_min = min( z_range )
  z_max = max( z_range )
  indices_mod = np.where( (z>= z_min) * (z<=z_max) )[0]
  z_mod = z[indices_mod[0]-1:indices_mod[-1]+2]
  gamma_mod = gamma[indices_mod[0]-1:indices_mod[-1]+2]
  zmax = z_mod.max()
  x = np.abs(z_mod - zmax)
  gamma_l = np.log10(gamma_mod[0])
  gamma_r = np.log10(gamma_mod[-1])
  delta_gamma = gamma_l - gamma_r
  sig = sigmoid( x, alpha=alpha, x0=x0 )
  sig -= sig.min()
  sig_res = sig / sig.max() * delta_gamma + gamma_r
  sig_res = 10**sig_res
  gamma_sigma = gamma.copy()
  gamma_sigma[indices_mod[0]-1:indices_mod[-1]+2] = sig_res
  if z.shape != gamma_sigma.shape:  print( 'ERROR: Shape mismatch' ) 
  return gamma_sigma


def Reaplace_Gamma_Parttial( z, gamma, change_z, change_gamma ):
  ind_sort = np.argsort( change_z )
  change_z = change_z[ind_sort]
  change_gamma = change_gamma[ind_sort]
  r_zmin, r_zmax =  change_z[0], change_z[-1]
  indices = np.where( (z>=r_zmin) * (z<=r_zmax) == True )
  original_z = z[indices] 
  gamma_replce = np.interp( original_z, change_z, change_gamma )
  gamma_new = gamma.copy()
  gamma_new[indices] = gamma_replce
  indx_last = indices[0][-1]
  gamma_new[indx_last] = np.sqrt( gamma_new[indx_last-1]*gamma_new[indx_last+1])
  return gamma_new

def Load_Grackle_File( grackle_file_name, print_out=True ):
  if print_out: print( f'Loadig File: {grackle_file_name}')
  grackle_file = h5.File( grackle_file_name, 'r' )

  data_out = {}
  root_key = 'UVBRates'
  data_root = grackle_file[root_key]
  data_out[root_key] = {}
  data_out[root_key]['z'] = data_root['z'][...]
  keys_gk = ['Chemistry', 'Photoheating' ]
  for key_gk in keys_gk:
    data_gk = data_root[key_gk]
    data_out[root_key][key_gk] = {}
    for key in data_gk.keys():
      data_out[root_key][key_gk][key] = data_gk[key][...]
  grackle_file.close()
  return data_out
  
  
def Shift_UVB_Rates( delta_z, rates, param_name, interp_log=False, kind='linear', extrapolate='constant' ):
  keys_He = { 'Chemistry':['k25'], 'Photoheating':['piHeII']}
  keys_H  = { 'Chemistry':['k24', 'k26'], 'Photoheating':['piHI', 'piHeI']}
  if param_name == 'shift_H': keys = keys_H
  elif param_name == 'shift_He': keys = keys_He
  else:
    print( "ERROR: Wrong parameter name for UVB rates shift")
    exit(-1)
  z_0 = rates['z'].copy()
  z_new = z_0 + delta_z
  root_keys = [ 'Chemistry', 'Photoheating' ]
  for root_key in root_keys:
    for key in keys[root_key]:
      rate_0 = rates[root_key][key].copy()
      z_min = z_0.min()
      z_max = z_0.max()
      if interp_log: rate_0 = np.log10( rate_0 )
      rate_new = np.interp( z_0, z_new, rate_0 )
      if extrapolate == 'spline':
        rate_log = np.log10(rate_0)
        z_max = z_new.min()
        if z_max > z_0.min():
          indices_extrp = z_0 <= z_max
          z_extrap = z_0[indices_extrp]
          interp_func = interp1d( z_new, rate_log, fill_value='extrapolate' )
          rate_extrap = interp_func(z_extrap)
          rate_new[indices_extrp] = 10**rate_extrap
      if interp_log: rate_new = 10**rate_new
      rates[root_key][key] = rate_new
      

      # indx_l = np.where( z_0 == z_min )[0]
      # indx_r = np.where( z_0 == z_max )[0]
      # rate_l = rate_0[indx_l]
      # rate_r = rate_0[indx_r]
      # if kind == 'linear':
      # interp_func = interp1d( z_0, rate_0, bounds_error=False, fill_value=(rate_l, rate_r), kind=kind )
      # z_hr = np.linspace( z_min, z_max, 1000 )
      # rate_hr = interp_func( z_hr )
      # z_new_hr = z_hr + delta_z
      # rate_new = np.interp( z_0, z_new_hr, rate_hr )  
      # rate_new = interp_func( z_0 )


  


def Extend_Redshift( max_delta_z, z ):
  z_new = [z[0]]
  n_z = len( z )
  for i in range( n_z-1 ):
    z_l = z_new[-1]
    z_r = z[i+1]
    while( z_r - z_l ) > max_delta_z:
      z_new.append( 0.5*(z_l + z_r) )
      z_l = z_new[-1]
    z_new.append( z_r )
  z_new = np.array( z_new )
  return z_new
  
def Interpoate_Rate( z_new, z_0, rate, interp_log=False ):
  if interp_log: rate = np.log10(rate)
  rate_new = np.interp( z_new, z_0, rate )
  if interp_log: rate_new = 10**rate_new
  return rate_new 
  
def Copy_Grakle_UVB_Rates( rates_data ):
  grackle_keys = { 'Photoheating':['piHI', 'piHeI', 'piHeII'], 'Chemistry':['k24', 'k25', 'k26'] }
  output_rates = { 'UVBRates':{} }
  output_rates['UVBRates']['z'] = rates_data['UVBRates']['z'].copy()
  for grackle_key in grackle_keys:
    output_rates['UVBRates'][grackle_key] = {}
    field_keys = grackle_keys[grackle_key]
    for field_key in field_keys:
      output_rates['UVBRates'][grackle_key][field_key] = rates_data['UVBRates'][grackle_key][field_key].copy()
  return output_rates  
  
def Extend_Rates_Redshift( max_delta_z, grackle_data ):
  data_out = {}
  root_key = 'UVBRates'
  data_root = grackle_data[root_key].copy()
  z_0 =  data_root['z'][...]
  z_new = Extend_Redshift( max_delta_z, z_0)
  data_out[root_key] = {}
  data_out[root_key]['z'] = z_new
  keys_gk = ['Chemistry', 'Photoheating' ]
  for key_gk in keys_gk:
    data_gk = data_root[key_gk]
    data_out[root_key][key_gk] = {}
    for key in data_gk.keys():
      rate = data_gk[key][...]
      rate_new = Interpoate_Rate( z_new, z_0, rate )
      data_out[root_key][key_gk][key] = rate_new
  return data_out


def Modify_UVB_Rates( parameter_values, rates, extrapolate='constant' ):
  input_rates = rates.copy()
  rates_modified = Modify_Rates_From_Grackle_File( parameter_values, rates_data=input_rates, input_file_name=None, extrapolate=extrapolate )
  uvb_rates = rates_modified['UVBRates']
  z = uvb_rates['z']
  heat_HI   = uvb_rates['Photoheating']['piHI']
  heat_HeI  = uvb_rates['Photoheating']['piHeI']
  heat_HeII = uvb_rates['Photoheating']['piHeII']
  ion_HI   = uvb_rates['Chemistry']['k24']
  ion_HeI  = uvb_rates['Chemistry']['k26']
  ion_HeII = uvb_rates['Chemistry']['k25']
  rates_modified =  {}
  rates_modified['z'] = z
  rates_modified['photoheating_HI'] = heat_HI 
  rates_modified['photoheating_HeI'] = heat_HeI 
  rates_modified['photoheating_HeII'] = heat_HeII 
  rates_modified['photoionization_HI'] = ion_HI 
  rates_modified['photoionization_HeI'] = ion_HeI 
  rates_modified['photoionization_HeII'] = ion_HeII 
  return rates_modified
  

def Modify_Rates_From_Grackle_File(  parameter_values, max_delta_z = 0.1, rates_data=None, input_file_name=None, extrapolate='constant', extend_rates_z=True, print_out=True ):
  skip_parameters = [ 'wdm_mass' ]
  
  if not rates_data:
    grackle_data = Load_Grackle_File( input_file_name, print_out=print_out )
    rates = Copy_Grakle_UVB_Rates(grackle_data)  
    if extend_rates_z:
      print( f'Extending Rates Redshift  max_delta_z:{max_delta_z}' )
      rates_data = Extend_Rates_Redshift( max_delta_z, rates )
    else: rates_data = rates
    
    
  info = 'Rates for '
  for p_name in parameter_values.keys():
    if p_name in skip_parameters: continue
    p_val = parameter_values[p_name]
    info += f' {p_name}:{p_val}' 
  
    if p_name == 'scale_H':
      rates_data['UVBRates']['Chemistry']['k24'] *= p_val
      rates_data['UVBRates']['Chemistry']['k26'] *= p_val
      rates_data['UVBRates']['Photoheating']['piHI'] *= p_val
      rates_data['UVBRates']['Photoheating']['piHeI'] *= p_val
  
    elif p_name == 'scale_He':
      rates_data['UVBRates']['Chemistry']['k25'] *= p_val
      rates_data['UVBRates']['Photoheating']['piHeII'] *= p_val

    elif p_name == 'scale_H_ion':
      rates_data['UVBRates']['Chemistry']['k24'] *= p_val
      rates_data['UVBRates']['Chemistry']['k26'] *= p_val
    
    elif p_name == 'scale_H_heat':
      rates_data['UVBRates']['Photoheating']['piHI'] *= p_val
      rates_data['UVBRates']['Photoheating']['piHeI'] *= p_val
  
    elif p_name == 'scale_He_ion':  rates_data['UVBRates']['Chemistry']['k25'] *= p_val
    elif p_name == 'scale_He_heat': rates_data['UVBRates']['Photoheating']['piHeII'] *= p_val
 
    elif p_name == 'deltaZ_H':  Shift_UVB_Rates( p_val, rates_data['UVBRates'], 'shift_H', extrapolate=extrapolate )
    elif p_name == 'deltaZ_He': Shift_UVB_Rates( p_val, rates_data['UVBRates'], 'shift_He', extrapolate=extrapolate )
    
    elif p_name == 'scale_H_Eheat':
      if 'scale_H_ion' in parameter_values: scale_H_ion = parameter_values['scale_H_ion']
      else:
        scale_H_ion = 1 
        print('WARNING: Using scale_H_ion = 1')
      scale_H_heat = scale_H_ion * p_val
      rates_data['UVBRates']['Photoheating']['piHI']  *= scale_H_heat
      rates_data['UVBRates']['Photoheating']['piHeI'] *= scale_H_heat
    
    elif p_name == 'scale_He_Eheat':
      if 'scale_He_ion' in parameter_values: scale_He_ion = parameter_values['scale_He_ion']
      else:
        scale_He_ion = 1 
        print('WARNING: Using scale_He_ion = 1')
      scale_He_heat = scale_He_ion * p_val
      rates_data['UVBRates']['Photoheating']['piHeII'] *= scale_He_heat
        
    else: print(f'ERROR: parameter name {p_name} not recognized' )
  rates_data['UVBRates']['info'] = info
  return rates_data


def Write_Rates_Grackle_File( out_file_name, rates, print_out=True ):
  root_key = 'UVBRates'
  info = rates[root_key]['info']
  if print_out: print( f'  Writing {info}' )
  
  len_info = len(info)
  type_info = f'|S{len_info}'
  info = np.array(info, dtype=type_info )
  out_file = h5.File( out_file_name, 'w' )
  root_group = out_file.create_group( root_key )
  root_group.create_dataset( 'Info', data=info )
  root_group.create_dataset( 'z', data=rates[root_key]['z'] )
  data_keys = [ 'Chemistry', 'Photoheating' ]
  for data_key in data_keys:
    group_data = rates[root_key][data_key] 
    data_group = root_group.create_group( data_key )
    for key in group_data.keys():
      data_group.create_dataset( key, data=group_data[key] )
  out_file.close()
  if print_out: print( f' Saved File: {out_file_name}')
      
  
      
def Generate_Modified_Rates_File( out_file_name, parameter_values, max_delta_z=0.1, input_file_name=None, input_UVB_rates=None, extend_rates_z=True, print_out=True ):      
  rates = Modify_Rates_From_Grackle_File( parameter_values, max_delta_z=max_delta_z, input_file_name=input_file_name, rates_data=input_UVB_rates, extend_rates_z=extend_rates_z, print_out=print_out )
  Write_Rates_Grackle_File( out_file_name, rates, print_out=print_out )
      


def Load_Grackle_UVB_File( file_name ):
  file = h5.File( file_name, 'r' )

  rates = file['UVBRates']
  info = rates['Info'][...]
  z = rates['z'][...]

  rates_out = {}
  rates_out['z'] = z

  rates_out['ionization'] = {}
  chemistry = rates['Chemistry']
  rates_out['ionization']['HI']   = chemistry['k24'][...]
  rates_out['ionization']['HeI']  = chemistry['k26'][...]
  rates_out['ionization']['HeII'] = chemistry['k25'][...]

  rates_out['heating'] = {}
  heating = rates['Photoheating'] 
  rates_out['heating']['HI']   = heating['piHI'][...] * eV_to_ergs
  rates_out['heating']['HeI']  = heating['piHeI'][...] * eV_to_ergs
  rates_out['heating']['HeII'] = heating['piHeII'][...] * eV_to_ergs
  return rates_out








