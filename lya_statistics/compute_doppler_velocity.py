import sys, os, time
import numpy as np
from scipy.special import erf
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
import constants_cgs as cgs


def get_Doppler_parameter( T, chem_type='HI' ):
  if chem_type == 'HI':   M = cgs.M_p
  if chem_type == 'HeII': M = 4 * cgs.M_p
  b = np.sqrt( 2* cgs.K_b / M * T )
  return b


T = 10e3

b = get_Doppler_parameter( T ) /1e5

k = 2 * np.pi / b