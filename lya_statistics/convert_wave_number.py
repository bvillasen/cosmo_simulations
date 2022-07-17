import os, sys
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from cosmology import Cosmology

# Initialize Cosmology
z_start = 1000
cosmo = Cosmology( z_start )

z = 5
current_a = 1 / ( z + 1 )
H = cosmo.get_Hubble( current_a )
k_min = 10**-2.2
k_max = 10**-0.7

k_spac_min = H * current_a * k_min / cosmo.h
k_spac_max = H * current_a * k_max / cosmo.h