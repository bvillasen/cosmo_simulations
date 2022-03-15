import numpy as np

def rescale_matrix( matrix, factor, type):
  ni, nj = matrix.shape
  for i in range(ni):
    for j in range(nj):
      if type == 'cross_only': 
        if i == j: continue
      elif type == 'diagonal_only': 
        if i != j: continue
      else: 
        print( f'Rescale Matrix type {type} not implemented' )
        return None
      matrix[i,j] *= factor
  return matrix 


def Normalize_Covariance_Matrix( cov_matrix ):
  ny, nx = cov_matrix.shape
  if nx != ny:
    print('ERROR: Matrix is not square')
    return None 
  norm_matrix = cov_matrix.copy()
  for i in range(ny):
    for j in range(nx):
      norm_matrix[i,j] = cov_matrix[i,j] / np.sqrt( cov_matrix[i,i] * cov_matrix[j,j] )
  return norm_matrix
  
def Merge_Matrices( matrices ):
  # Merge cov matrices into a single one
  n_total = 0  
  for matrix in matrices:
    ny, nx = matrix.shape
    n_total += nx

  matrix_merge = np.zeros((n_total, n_total))
  offset = 0
  for matrix in matrices:
    ny, nx = matrix.shape
    matrix_merge[offset:offset+ny,offset:offset+nx] = matrix
    offset += ny
  return matrix_merge