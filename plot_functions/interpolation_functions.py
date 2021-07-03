import numpy as np
from scipy import interpolate as interp 


def interp_line_cubic( x, x_interp, y ):
  func = interp.interp1d( x, y, kind='cubic' )
  return func(x_interp)