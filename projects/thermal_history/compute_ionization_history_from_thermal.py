import sys, os, time
import numpy as np
import h5py as h5
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
from tools import *
from stats_functions import compute_distribution, get_highest_probability_interval

proj_dir = data_dir + 'projects/thermal_history/'
input_dir = proj_dir + 'data/ionization_history/'
output_dir = proj_dir + 'data/ionization_history/'
create_directory(output_dir)



def load_ionization_history( input_dir, model_id ):
  file_name = input_dir + f'solution_{model_id}.h5'
  file = h5.File( file_name, 'r' )
  z = file['z'][...]
  n_H  = file['n_H'][...] 
  n_HI = file['n_HI'][...] 
  n_e  = file['n_e'][...]
  file.close()
  x_HI = n_HI / n_H
  return z, x_HI, n_e 

model_id = 'HL'
z, x_HI_HL, n_e_HL = load_ionization_history( input_dir, model_id )

x_HI_vals, n_e_vals = [], []
for model_id in range( 16 ):
  z, x_HI, n_e = load_ionization_history( input_dir, model_id )
  x_HI_vals.append( x_HI )
  n_e_vals.append( n_e )

x_HI = np.array( x_HI_vals )
n_e = np.array( n_e_vals )
n = x_HI.shape[1]

x_HI_l, x_HI_h, n_e_l, n_e_h = [], [],[], []
for i in range(n):
  slice_xHI = x_HI[:,i]
  slice_ne = n_e[:,i]  
  x_HI_l.append( slice_xHI.min() )
  x_HI_h.append( slice_xHI.max() )
  n_e_l.append( slice_ne.min() )
  n_e_h.append( slice_ne.max() )
  
x_HI_l = np.array( x_HI_l )[::-1]
x_HI_h = np.array( x_HI_h )[::-1]
n_e_l = np.array( n_e_l )[::-1]  
n_e_h = np.array( n_e_h )[::-1]  
z = z[::-1]

n_interpolate = 10000
z_interp = np.linspace( 0, z.max(), n_interpolate )

x_HI_HL= np.interp( z_interp, z, x_HI_HL)
x_HI_l = np.interp( z_interp, z, x_HI_l)
x_HI_h = np.interp( z_interp, z, x_HI_h)
n_e_HL = np.interp( z_interp, z, n_e_HL)
n_e_l = np.interp( z_interp, z, n_e_l)
n_e_h = np.interp( z_interp, z, n_e_h)
z = z_interp

z_lim = 5.6
delta = 0.10
z_indices = z <= z_lim
x_HI_h[z_indices] *= (1 + delta )

z_r = 5.9
z_l = 5.8
delta = 0.08
z_indices = ( z >= z_l ) * ( z <= z_r )
n = z_indices.sum()
facor = np.linspace(0, delta, n)[::-1]
x_HI_l[z_indices] *= (1 - facor )

z_lim = z_l
z_indices = z <= z_lim
x_HI_l[z_indices] *= (1 - delta )

data_out = { 'z':z }
data_out['x_HI'] = {'low':x_HI_l, 'high':x_HI_h, 'HL':x_HI_HL[::-1] }
data_out['n_e'] = {'low':n_e_l, 'high':n_e_h, 'HL':n_e_HL[::-1] }


file_name = output_dir + 'best_fit_ionization.pkl'
Write_Pickle_Directory( data_out, file_name )
  
