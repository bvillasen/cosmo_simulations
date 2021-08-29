import sys, os
import numpy as np
from scipy import interpolate as interp 
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter


def are_floats_equal( a, b, epsilon=1e-10 ):
  if np.abs( a - b ) < epsilon: return True
  else: return False
    

def Find_Parameter_Value_Near_IDs( param_id, param_value, parameters, clip_params=False ):
  param_name = parameters[param_id]['name']    
  grid_param_values = np.array(parameters[param_id]['values'])
  param_min = grid_param_values.min() 
  param_max = grid_param_values.max()
  n_param_values = len( grid_param_values )
  # print( f' Param_id:{param_id}   value:{param_value}' )
  if n_param_values == 1:
    p_val_id_l,  p_val_id_r = 0, 0
    return p_val_id_l, p_val_id_r  
  if clip_params:
    if param_value < param_min: param_value = param_min
    if param_value > param_max: param_value = param_max
  else:  
    if param_value < param_min or param_value > param_max:
      print( f'ERROR: Paramneter Value outside {param_name} Range: [ {param_min} , {param_max} ] value:{param_value}')
      exit(-1)
  if are_floats_equal( param_value, param_min ):
    p_val_id_l,  p_val_id_r = 0, 1
    return p_val_id_l, p_val_id_r
  if are_floats_equal( param_value, param_max ):
    p_val_id_l,  p_val_id_r = n_param_values-2, n_param_values-1
    return p_val_id_l, p_val_id_r
  p_val_id_l, p_val_id_r = 0, 0
  diff_l, diff_r = -np.inf, np.inf
  for v_id, p_val in enumerate(grid_param_values):
    diff = p_val - param_value
    if diff > 0 and diff < diff_r: p_val_id_r, diff_r = v_id, diff
    if diff < 0 and diff > diff_l: p_val_id_l, diff_l = v_id, diff  
  if p_val_id_l == p_val_id_r: print('ERROR: Same values for left and right')
  return p_val_id_l, p_val_id_r
  
  
def Get_Simulation_ID_From_Coordinates( sim_coords, SG ):
  grid = SG.Grid
  parameters = SG.parameters
  param_ids = parameters.keys()
  key = ''
  for param_id in param_ids:
    p_key = parameters[param_id]['key']
    key += f'_{p_key}{sim_coords[param_id]}'
  key = key[1:]
  sim_id = SG.coords[key]
  return sim_id


def Get_Value_From_Simulation( sim_coords, data_to_interpolate, field, sub_field, SG, interp_log=False ):
  sim_id = Get_Simulation_ID_From_Coordinates( sim_coords, SG )
  sim = SG.Grid[sim_id]
  param_values = sim['parameter_values']
  value = data_to_interpolate[sim_id][field][sub_field]
  if interp_log: value = np.log10(value)
  return value

def Get_Parameter_Grid( param_values, parameters, clip_params=False ):
  parameter_grid = {}
  for p_id, p_val in enumerate(param_values):
    parameter_grid[p_id] = {}
    # print( f' Param_id:{p_id}   value:{p_val}' )
    v_id_l, v_id_r = Find_Parameter_Value_Near_IDs( p_id, p_val, parameters, clip_params=clip_params )
    parameter_grid[p_id]['v_id_l'] = v_id_l
    parameter_grid[p_id]['v_id_r'] = v_id_r
    parameter_grid[p_id]['v_l'] = parameters[p_id]['values'][v_id_l]
    parameter_grid[p_id]['v_r'] = parameters[p_id]['values'][v_id_r]
  return parameter_grid
  


def Interpolate_4D( p0, p1, p2, p3, data_to_interpolate, field, sub_field, SG, clip_params=False, parameter_grid=None, param_id=None, sim_coords_before=None, interp_log=False ):
  param_values = np.array([ p0, p1, p2, p3 ])
  n_param = len(param_values)
  if param_id == None: param_id = n_param - 1
  if sim_coords_before == None:  sim_coords_before = [ -1 for param_id in range(n_param)] 
  if parameter_grid == None: parameter_grid = Get_Parameter_Grid( param_values, SG.parameters, clip_params=clip_params )
  
  sim_coords_l = sim_coords_before.copy()
  sim_coords_r = sim_coords_before.copy()
  
  v_id_l = parameter_grid[param_id]['v_id_l']
  v_id_r = parameter_grid[param_id]['v_id_r']
  p_val_l = parameter_grid[param_id]['v_l']
  p_val_r = parameter_grid[param_id]['v_r']
  sim_coords_l[param_id] = v_id_l
  sim_coords_r[param_id] = v_id_r
  p_val = param_values[param_id]
  
  if clip_params:
    if p_val < p_val_l: p_val = p_val_l
    if p_val > p_val_r: p_val = p_val_r
  else:      
    if p_val < p_val_l or p_val > p_val_r:
      print( ' ERROR: Parameter outside left and right values')
      exit()
  if p_val_l == p_val_r: delta = 0.5
  else: delta = ( p_val - p_val_l ) / ( p_val_r - p_val_l )  
  if param_id == 0:
    value_l = Get_Value_From_Simulation( sim_coords_l, data_to_interpolate, field, sub_field, SG, interp_log=interp_log )
    value_r = Get_Value_From_Simulation( sim_coords_r, data_to_interpolate, field, sub_field, SG, interp_log=interp_log )
    value_interp = delta*value_r + (1-delta)*value_l 
    return value_interp
  
  value_l = Interpolate_4D( p0, p1, p2, p3, data_to_interpolate, field, sub_field, SG, parameter_grid=parameter_grid, param_id=param_id-1, sim_coords_before=sim_coords_l, clip_params=clip_params, interp_log=interp_log )
  value_r = Interpolate_4D( p0, p1, p2, p3, data_to_interpolate, field, sub_field, SG, parameter_grid=parameter_grid, param_id=param_id-1, sim_coords_before=sim_coords_r, clip_params=clip_params, interp_log=interp_log )
  value_interp = delta*value_r + (1-delta)*value_l
  return value_interp




def interp_line_cubic( x, x_interp, y ):
  func = interp.interp1d( x, y, kind='cubic' )
  return func(x_interp)
  
  
def smooth_line( values, x_vals, log=False, n_neig=3, order=2, interpolate=False,  n_interp=1000 ):
  from scipy.signal import savgol_filter
  if log: values = np.log10(values)
  values_smooth = savgol_filter(values, n_neig, order)
  
  if interpolate:
    if log: x_vals = np.log10(x_vals)
    x_start, x_end = x_vals[0], x_vals[-1]
    x_interp = np.linspace( x_start, x_end, n_interp )
    interpolation = interp1d( x_vals, values_smooth, kind='cubic')
    values_interp = interpolation( x_interp )
  
  if log: 
    values_smooth = 10**values_smooth
    if interpolate: 
      x_interp = 10**x_interp
      values_interp = 10**values_interp
  if interpolate: return values_interp, x_interp
  return  x_vals, values_smooth  