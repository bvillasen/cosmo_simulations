import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab

base_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from plot_uvb_rates import Plot_HI_Photoionization
from uvb_functions import *
from colors import *

black_background = False

proj_dir = data_dir + 'projects/thermal_history/'
output_dir = proj_dir + 'figures/'
if black_background: output_dir += 'black_background/'
create_directory( output_dir ) 

# param_vals = {}
# param_vals[0] = [ 0.36, 0.57 ]
# param_vals[1] = [ 0.75, 0.79 ]
# param_vals[2] = [ 0.21, 0.38 ]
# param_vals[3] = [ 0.02, 0.17 ]

param_vals = {}
param_vals[0] = [ 0.38, 0.60 ]
param_vals[1] = [ 0.72, 0.74 ]
param_vals[2] = [ 0.18, 0.34 ]
param_vals[3] = [ 0.18, 0.2 ]

  
param_combinations = Get_Parameters_Combination( param_vals )  

grackle_file_name = base_dir + 'rates_uvb/data/CloudyData_UVB_Puchwein2019_cloudy.h5'
rates_P19 = Load_Grackle_File( grackle_file_name )
max_delta_z = 0.1
rates_P19 = Extend_Rates_Redshift( max_delta_z, rates_P19, log=False )



rates_all = {}
for id, p_vals in enumerate(param_combinations):
  rates_data = Copy_Grakle_UVB_Rates( rates_P19 )
  uvb_parameters = { 'scale_He':p_vals[0], 'scale_H':p_vals[1], 'deltaZ_He':p_vals[2], 'deltaZ_H':p_vals[3] }
  uvb_rates = Modify_Rates_From_Grackle_File( uvb_parameters,  rates_data=rates_data, extrapolate='spline' )
  rates_all[id] = uvb_rates


keys = { 'Chemistry':[ 'k24', 'k26', 'k25' ], 'Photoheating':[ 'piHI', 'piHeI', 'piHeII' ] }


z = rates_all[0]['UVBRates']['z'] 
n_points = len(z)

rates_range  = {}
for root_key in keys:
  rates_range[root_key] = {}
  for key in keys[root_key]:
    rates_max, rates_min = [], []
    for z_indx in range(n_points):
      vmax, vmin = -np.inf, np.inf
      for rates_id in rates_all:
        rates = rates_all[rates_id]
        rate_vals = rates['UVBRates'][root_key][key]
        rate_val = rate_vals[z_indx]
        vmax = max( vmax, rate_val )
        vmin = min( vmin, rate_val )          
      rates_max.append( vmax )
      rates_min.append( vmin )
    rates_range[root_key][key] = { 'z':z, 'max': np.array(rates_max), 'min':np.array(rates_min) }

# params_HL = { 'scale_He':0.45, 'scale_H':0.77, 'deltaZ_He':0.31, 'deltaZ_H':0.1 }
params_HL = { 'scale_He':0.47, 'scale_H':0.71, 'deltaZ_He':0.25, 'deltaZ_H':0.19 }
rates_data = Copy_Grakle_UVB_Rates( rates_P19 )
rates_HL = Modify_Rates_From_Grackle_File( params_HL,  rates_data=rates_data, extrapolate='spline' )


line_color = 'k'
if black_background: line_color = purples[1]

rates_data = {}
ion_HI = rates_HL['UVBRates']['Chemistry']['k24']
high = rates_range['Chemistry']['k24']['max']
low  = rates_range['Chemistry']['k24']['min']
# indices = z > 6.2
# high[indices] *= 10
# z_l, z_m, z_r = 1.5, 2.0, 2.4
# indices_l = ( z >= z_l ) * ( z <= z_m )
# n = indices_l.sum()
# v_m = 1.04
# factor_l = np.linspace( 1, v_m, n )
# indices_r = ( z >= z_m ) * ( z <= z_r )
# n = indices_r.sum()
# factor_r = np.linspace( v_m, 1, n )
# high[indices_l] *= factor_l
# high[indices_r] *= factor_r 
rates_data[0] = { 'z':z, 'photoionization':ion_HI, 'higher':high, 'lower':low, 'label':'Best-Fit to HM12' }
rates_data[0]['line_color'] = line_color
rates_data[0]['ls'] = '-'
rates_data[0]['lw'] = 3.5

grackle_file_name = base_dir + 'rates_uvb/data/CloudyData_UVB_Puchwein2019_cloudy.h5'
rates_P19 = Load_Grackle_File( grackle_file_name )
rates_P19 = Extend_Rates_Redshift( max_delta_z, rates_P19, log=False )



params_HL = { 'scale_He':0.45, 'scale_H':0.77, 'deltaZ_He':0.31, 'deltaZ_H':0.1 }
rates_data_0 = Copy_Grakle_UVB_Rates( rates_P19 )
rates_HL = Modify_Rates_From_Grackle_File( params_HL,  rates_data=rates_data_0, extrapolate='spline' )

x0 = 0
z_range = ( 4.8, 6.12 )
alpha = 2.5
input_rates = Copy_Grakle_UVB_Rates( rates_HL )
rates_sigmoid = Modify_UVB_Rates_sigmoid( input_rates, z_range, alpha, x0 )
ion_HI_sig = rates_sigmoid['UVBRates']['Chemistry']['k24']

# z_l, z_r = 4.4, 5.0
# indices = ( z >= z_l ) * ( z <= z_r )
# n = indices.sum()
# factor = np.linspace( 1)

ion_HI_sig *= 1.04
z_l = 4.6
indices = z <= z_l 
ion_HI_sig[indices] = ion_HI[indices]

z_r = 6.1
indices = z >= z_r 
ion_HI_sig[indices] = ion_HI[indices]

grackle_file_name = base_dir + 'rates_uvb/data/CloudyData_UVB_HM2012.h5'
rates_HM12 = Load_Grackle_File( grackle_file_name )
rates_HM12 = Extend_Rates_Redshift( max_delta_z, rates_HM12, log=False )


params_HL = { 'scale_He':1, 'scale_H':1, 'deltaZ_He':0., 'deltaZ_H':0. }
rates_HM12 = Modify_Rates_From_Grackle_File( params_HL,  rates_data=rates_HM12, extrapolate='spline' )
z = rates_HM12['UVBRates']['z']
ion = rates_HM12['UVBRates']['Chemistry']['k24']
rates_data[1] = { 'z':z, 'photoionization':ion, 'label':'HM12' }
rates_data[1]['line_color'] = 'C4'
rates_data[1]['ls'] = '-'
rates_data[1]['lw'] = 3.5

Plot_HI_Photoionization( output_dir, rates_data=rates_data, figure_name='Gamma_HI_hm12', show_low_z=True, black_background=black_background )