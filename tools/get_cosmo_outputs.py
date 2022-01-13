import sys, os, time
import numpy as np
import matplotlib.pyplot as plt
from tools import *

output_dir = home_dir + 'Desktop/' 

n_snaps = 200
z_start, z_end = 100, 0
a_start, a_end = 1/(z_start+1), 1/(z_end+1),
a_vals = np.linspace( a_start, a_end, n_snaps )
outfile_name = output_dir + f'outputs_cosmo_z_{z_start}_{z_end}_{n_snaps}.txt'
np.savetxt( outfile_name, a_vals )
print( f'Saved File: {outfile_name}' )

z_vals = np.array([ 10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0 ])
a_vals = 1./(z_vals + 1)
outfile_name = output_dir + f'outputs_cosmo_testing.txt'
np.savetxt( outfile_name, a_vals )
print( f'Saved File: {outfile_name}' )


# z_vals = np.array([ 2., 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2,  4.6, 5.0, 5.4 ])[::-1]
# a_vals = 1./(z_vals + 1)

# 
# outfile_name = 'outputs_cosmo_10.txt'
# np.savetxt( outfile_name, a_vals )



# z_vals = np.array([ 0.0, 0.2, 0.5, 0.7, 1, 2, 5,  10, 50, 100 ])[::-1]
# a_vals = 1./(z_vals + 1)
# 
# 
# z_vals = np.array([ 2.0, 2.4, 2.6, 3.0, 3.6, 4.0, 5.0 ])[::-1]
# a_vals = 1./(z_vals + 1)
# 
# z_vals = np.arange( 4.8, 6.5, 0.1 )[::-1]
# a_vals = 1./(z_vals + 1)

# n_vals = 100
# z_start, z_end = 6, 0
# a_start, a_end = 1/(z_start+1), 1/(z_end+1)  
# a_vals = np.linspace( a_start, a_end, n_vals )
# 
# file_name = output_dir + 'cosmo_outputs_z_6_0_100.txt'
# np.savetxt( file_name, a_vals )
# print( f'Saved File: {file_name}' )


