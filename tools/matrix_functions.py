import numpy as np


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