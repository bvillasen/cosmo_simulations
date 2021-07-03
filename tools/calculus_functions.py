import numpy as np





def Get_Centered_First_Derivative( vals, dx ):
  n = len(vals)
  n_ghost = 1
  vals_extended = np.zeros( n + 2*n_ghost )
  vals_extended[n_ghost:n+n_ghost] = vals
  vals_extended[:n_ghost] = vals[-n_ghost:]
  vals_extended[-n_ghost:] = vals[:n_ghost] 
  vals_r = vals_extended[n_ghost+1:]
  vals_l = vals_extended[:-(n_ghost+1)]
  deriv  = ( vals_r - vals_l ) / ( 2* dx )
  return deriv
  
  
def Get_Centered_Second_Derivative( vals, dx ):
  n = len(vals)
  n_ghost = 1
  vals_extended = np.zeros( n + 2*n_ghost )
  vals_extended[n_ghost:n+n_ghost] = vals
  vals_extended[:n_ghost] = vals[-n_ghost:]
  vals_extended[-n_ghost:] = vals[:n_ghost] 
  vals_r = vals_extended[n_ghost+1:]
  vals_l = vals_extended[:-(n_ghost+1)]
  deriv  = ( vals_r + vals_l - 2*vals ) / ( dx**2 )
  return deriv

# 
# x = np.linspace( 0, 2*np.pi, 1000 )[:-1]
# dx = x[1] - x[0]
# sin_x = np.sin( x )
# cos_x = np.cos( x )
# 
# 
# vals = sin_x
# deriv = Get_Centered_First_Derivative( vals, dx )
# deriv2 = Get_Centered_Second_Derivative( vals, dx )
# diff = ( deriv - cos_x ) / cos_x
# diff2 = ( deriv2 + sin_x ) / sin_x
