import numpy as np



def load_data_gaikwad( data_filename ):
  table = np.loadtxt( data_filename )
  z_vals_all =  np.round(table[:,0], decimals=1 )
  z_vals = np.array(list(set(list(z_vals_all))))
  z_vals.sort()
  data_out = {}
  data_out['z_vals'] = z_vals
  for i,z in enumerate(z_vals):
    indices = np.where(z_vals_all==z)[0]
    data_z =  table[indices]
    k_vals = data_z[:,1]
    delta_power = data_z[:,2]
    delta_power_error = data_z[:,3] 
    data_out[i] = {}
    data_out[i]['z'] = z
    data_out[i]['k_vals'] = k_vals
    data_out[i]['delta_power'] = delta_power 
    data_out[i]['delta_power_error'] = delta_power_error 
    data_out[i]['power_spectrum'] = delta_power * np.pi / k_vals 
    data_out[i]['sigma_power_spectrum'] = delta_power_error * np.pi / k_vals 
  return data_out


def load_data_irsic( data_irsic_dir, print_out=True ):
  file_name = data_irsic_dir + 'data_power_spectrum.txt'
  if print_out: print( f'Loading File: {file_name}')
  table = np.loadtxt( file_name )
  file_name = data_irsic_dir + 'data_covariance_matrix.txt'
  if print_out: print( f'Loading File: {file_name}')
  table_cov = np.loadtxt( file_name )
  col_id, row_id, matrix_val = table_cov.T
  col_id = col_id.astype(int)
  row_id = row_id.astype(int)
  n_cols, n_rows = col_id.max() + 1, row_id.max() + 1
  full_cov_matrix = np.ones( [n_rows, n_cols ]) * -10000
  for i, j, val in zip( row_id, col_id, matrix_val):
    full_cov_matrix[i,j] = val
  if full_cov_matrix.min() < -999: 
    print( 'ERROR Loading covariance matrix')
    exit(-1)

  z_vals_all =  np.round(table[:,0], decimals=1 )
  z_vals = np.array(list(set(list(z_vals_all))))
  z_vals.sort()
  data_out = {}
  n_k = None
  data_out['z_vals'] = z_vals
  data_out['full_covariance'] = full_cov_matrix
  k_vals_all = None
  for i,z in enumerate(z_vals):
    indices = np.where(z_vals_all==z)[0]
    data_z =  table[indices]
    k_vals = data_z[:,1]
    if k_vals_all is None: k_vals_all = k_vals
    k_diff = np.abs( k_vals_all - k_vals ).sum()
    if k_diff > 1e-10:
      print('ERROR: Not the same k_vals for all redshifts')
      exit(-1)
    if n_k is None: n_k = len(k_vals)
    n_k_local = len(k_vals)
    if n_k_local != n_k: print('ERROR: not the same number ok k_vals')
    power_1 = data_z[:,2]
    power_2 = data_z[:,6] 
    sigma_1 = data_z[:,3]
    sigma_2 = data_z[:,4]
    power = power_1
    power[z>3.7]  = power_2[z>3.7]
    # power_error = np.sqrt( sigma_1**2 + sigma_2**2 )
    power_error = sigma_1
    local_cov_matrix = full_cov_matrix[i*n_k_local:(i+1)*n_k_local,i*n_k_local:(i+1)*n_k_local] 
    data_out[i] = {}
    data_out[i]['z'] = z
    data_out[i]['k_vals'] = k_vals
    data_out[i]['delta_power'] = power * k_vals / np.pi 
    data_out[i]['delta_power_error'] = power_error * k_vals / np.pi 
    data_out[i]['power_spectrum'] = power  
    data_out[i]['sigma_power_spectrum'] = power_error 
    data_out[i]['covariance_matrix'] = local_cov_matrix
  data_out['k_vals'] = k_vals_all
  return data_out
     

def load_data_irsic_old( data_filename ):
  table = np.loadtxt( data_filename )
  z_vals_all =  np.round(table[:,0], decimals=1 )
  z_vals = np.array(list(set(list(z_vals_all))))
  z_vals.sort()
  data_out = {}
  data_out['z_vals'] = z_vals
  for i,z in enumerate(z_vals):
    indices = np.where(z_vals_all==z)[0]
    data_z =  table[indices]
    k_vals = data_z[:,1]
    power_1 = data_z[:,2]
    power_2 = data_z[:,6] 
    sigma_1 = data_z[:,3]
    sigma_2 = data_z[:,4]
    power = power_1
    power[z>3.7]  = power_2[z>3.7]
    # power_error = sigma_1 + sigma_2
    power_error = np.sqrt( sigma_1**2 + sigma_2**2 )
    data_out[i] = {}
    data_out[i]['z'] = z
    data_out[i]['k_vals'] = k_vals
    data_out[i]['delta_power'] = power * k_vals / np.pi 
    data_out[i]['delta_power_error'] = power_error * k_vals / np.pi 
    data_out[i]['power_spectrum'] = power  
    data_out[i]['sigma_power_spectrum'] = power_error  
  return data_out


def load_data_boss( data_filename ):
  table = np.loadtxt( data_filename )
  z_vals_all =  np.round(table[:,0], decimals=1 )
  z_vals = np.array(list(set(list(z_vals_all))))
  z_vals.sort()
  data_out = {}
  data_out['z_vals'] = z_vals
  for i,z in enumerate(z_vals):
    indices = np.where(z_vals_all==z)[0]
    data_z =  table[indices]
    k_vals = data_z[:,1]
    power = data_z[:,2]
    power_error = data_z[:,3]
    data_out[i] = {}
    data_out[i]['z'] = z
    data_out[i]['k_vals'] = k_vals
    data_out[i]['delta_power'] = power * k_vals / np.pi 
    data_out[i]['delta_power_error'] = power_error * k_vals / np.pi 
    data_out[i]['power_spectrum'] = power  
    data_out[i]['sigma_power_spectrum'] = power_error  
  return data_out
  
def load_data_boera( dir_data_boera, corrected=False, print_out=True ):
  z_vals = np.array([ 4.2, 4.6, 5.0 ])
  k_vals_all = None
  data_out = {}
  data_out['z_vals'] = z_vals
  for data_index in range(3):
    file_name = dir_data_boera + 'data_table_{0}.txt'.format( data_index )
    if print_out: print( f'Loading File: {file_name}') 
    data  = np.loadtxt( file_name )
    k_vals = 10**data[:,0]
    if k_vals_all is None: k_vals_all = k_vals
    k_diff = np.abs( k_vals_all - k_vals ).sum()
    if k_diff > 1e-10:
      print('ERROR: Not the same k_vals for all redshifts')
      exit(-1)
    power_vals = data[:,1]
    if corrected: power_vals = data[:,2]
    power_error = data[:,3]
    delta_power = k_vals * power_vals / np.pi
    delta_power_error = k_vals * power_error / np.pi
    data_out[data_index] = {}
    z = z_vals[data_index]
    file_name = dir_data_boera + f'Cov_Matrixz={z}.dat'
    if print_out: print( f'Loading File: {file_name}') 
    file = open( file_name, 'rb' )
    cov_matrix = np.load( file )
    nx, ny = cov_matrix.shape
    diagonal = np.array([ cov_matrix[i,i] for i in range(nx) ])
    diff = ( np.sqrt(diagonal) - power_error ) / power_error
    # print(diff)
    data_out[data_index]['z'] = z
    data_out[data_index]['k_vals'] = k_vals
    data_out[data_index]['delta_power'] = delta_power
    data_out[data_index]['delta_power_error'] = delta_power_error
    data_out[data_index]['power_spectrum'] = power_vals
    data_out[data_index]['power_spectrum_error'] = power_error
    data_out[data_index]['covariance_matrix'] = cov_matrix
  data_out['k_vals'] = k_vals_all
  return data_out

def load_power_spectrum_table( data_filename, kmax=100 ):
  table = np.loadtxt( data_filename )
  z_vals_all =  np.round(table[:,0], decimals=1 )
  z_vals = np.array(list(set(list(z_vals_all))))
  z_vals.sort()
  data_out = {}
  data_out['z_vals'] = z_vals
  for i,z in enumerate(z_vals):
    indices = np.where(z_vals_all==z)[0]
    data_z =  table[indices]
    k_vals = data_z[:,1]
    indices = k_vals <= kmax
    k_vals = k_vals[indices]
    delta_power = data_z[:,2][indices]
    delta_power_error = data_z[:,3][indices]
    power_spectrum       = delta_power       / k_vals * np.pi
    sigma_power_spectrum = delta_power_error / k_vals * np.pi
    data_out[i] = {}
    data_out[i]['z'] = z
    data_out[i]['k_vals'] = k_vals
    data_out[i]['delta_power'] = delta_power
    data_out[i]['delta_power_error'] = delta_power_error
    data_out[i]['power_spectrum']       = power_spectrum
    data_out[i]['sigma_power_spectrum'] = sigma_power_spectrum
  return data_out


def load_tabulated_data_colums( filename, n_cols ):
  data = np.loadtxt(  filename, delimiter=',' )
  n_total = data.shape[0]
  n_per_col = n_total // n_cols
  # print("Loaded {0} colums {1} points ".format(n_cols, n_per_col))
  data_cols = []
  for i in range( n_cols ):
    col = data[i*n_per_col:(i+1)*n_per_col,:]
    data_cols.append(col)
    
  data_cols = np.array( data_cols )
  x_vals = np.zeros(n_per_col)
  for i in range(n_cols):
    x_vals += data_cols[i,:,0]
  x_vals /= n_cols
  mean_vals  = data_cols[0,:,1]
  plus_vals  = data_cols[1,:,1]
  minus_vals = data_cols[2,:,1]
  data_out = {}
  data_out['x'] = x_vals
  data_out['mean'] = mean_vals
  data_out['plus'] = plus_vals
  data_out['minus'] = minus_vals
  return data_out
# 
# data = load_tabulated_data_colums( indir, filename, n_cols)



def load_tabulated_data_viel( data_dir ):
  z_vals = np.array([ 4.2, 4.6, 5.0, 5.4  ])
  data_out = {}
  data_out['z_vals'] = z_vals

  for index in range(len(z_vals)):
    filename = data_dir + '{0}.csv'.format(index)
    data = load_tabulated_data_colums( filename, 3 )
    k_vals = data['x']
    delta_power = data['mean']
    delta_power_plus = data['plus']
    delta_power_minus = data['minus']
    delta_power_error = delta_power_plus - delta_power
    data_out[index] = {}
    data_out[index]['z'] = z_vals[index]
    data_out[index]['k_vals'] = k_vals
    data_out[index]['delta_power'] = delta_power
    data_out[index]['delta_power_error'] = delta_power_error
  return data_out