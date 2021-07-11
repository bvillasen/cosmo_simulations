import sys, os, time
import numpy as np
import matplotlib.pyplot as plt


z_vals = np.array([ 2., 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2,  4.6, 5.0, 5.4 ])[::-1]
a_vals = 1./(z_vals + 1)

# 
# outfile_name = 'outputs_cosmo_10.txt'
# np.savetxt( outfile_name, a_vals )



z_vals = np.array([ 0.0, 0.2, 0.5, 0.7, 1, 2, 5,  10, 50, 100 ])[::-1]
a_vals = 1./(z_vals + 1)


z_vals = np.array([ 2.0, 2.4, 2.6, 3.0, 3.6, 4.0, 5.0 ])[::-1]
a_vals = 1./(z_vals + 1)

z_vals = np.arange( 4.8, 6.5, 0.1 )[::-1]
a_vals = 1./(z_vals + 1)

np.savetxt( '/home/bruno/Desktop/cosmo_outputs_high_redshift.txt', a_vals )