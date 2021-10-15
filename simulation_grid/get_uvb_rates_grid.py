import os, sys
import numpy as np
from scipy.interpolate import interp1d
base_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( base_dir + 'tools')
from tools import *
#Append analysis directories to path
extend_path()
from load_grid_parameters import Grid_Parameters
from simulation_grid import Simulation_Grid
from simulation_parameters import *
from plot_uvb_rates import Plot_UVB_Rates
from uvb_functions import Load_Grackle_File, Copy_Grakle_UVB_Rates

output_dir = root_dir

SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )


grackle_UVB_file_name =  base_dir + 'rates_uvb/data/CloudyData_UVB_Puchwein2019_cloudy.h5' 
rates_P19 = Load_Grackle_File( grackle_UVB_file_name )

rates_grid = {}

def interpoalate_1D( x_new, x_0, y_0 ):
    y_0 = np.log10( y_0 )
    interp_func = interp1d( x_0, y_0, fill_value='extrapolate' )
    rate_extrap = interp_func(x_new)
    rate_extrap = 10**rate_extrap
    return rate_extrap

selected_ids = []

for sim_id in SG.sim_ids:
  params = SG.Grid[sim_id]['parameters']
  modified_rates = Copy_Grakle_UVB_Rates( rates_P19 )
  scale_H   = params['scale_H']
  scale_He  = params['scale_He']
  deltaZ_H  = params['deltaZ_H']
  deltaZ_He = params['deltaZ_He']
  if deltaZ_H == 0.2 and scale_H == 1: selected_ids.append(sim_id)
  ion_HI   = modified_rates['UVBRates']['Chemistry']['k24']
  ion_HeI  = modified_rates['UVBRates']['Chemistry']['k26']
  ion_HeII = modified_rates['UVBRates']['Chemistry']['k25']
  heat_HI  = modified_rates['UVBRates']['Photoheating']['piHI']
  heat_HeI  = modified_rates['UVBRates']['Photoheating']['piHeI']
  heat_HeII = modified_rates['UVBRates']['Photoheating']['piHeII'] 
  ion_HI   *= scale_H
  ion_HeI  *= scale_H
  ion_HeII *= scale_He
  heat_HI   *= scale_H
  heat_HeI  *= scale_H
  heat_HeII *= scale_He
  z_0 = modified_rates['UVBRates']['z']
  z_H = z_0.copy() 
  z_He = z_0.copy()
  z_min, z_max = z_0.min(), z_0.max()
  z_H  += deltaZ_H
  z_He += deltaZ_He
  if deltaZ_H  > 0: 
    add_z_H  = np.arange(z_min, deltaZ_H,  0.1)
    add_ion_HI   = interpoalate_1D( add_z_H,  z_0+deltaZ_H, ion_HI )
    add_ion_HeI  = interpoalate_1D( add_z_H,  z_0+deltaZ_H, ion_HeI )
    add_heat_HI   = interpoalate_1D( add_z_H,  z_0+deltaZ_H, heat_HI )
    add_heat_HeI  = interpoalate_1D( add_z_H,  z_0+deltaZ_H, heat_HeI )
    z_H  = np.concatenate([ add_z_H, z_H ])
    ion_HI   = np.concatenate([ add_ion_HI,   ion_HI ])
    ion_HeI  = np.concatenate([ add_ion_HeI,  ion_HeI ])
    heat_HI  = np.concatenate([ add_heat_HI,  heat_HI ])
    heat_HeI = np.concatenate([ add_heat_HeI, heat_HeI ])
  if deltaZ_He > 0: 
    add_z_He = np.arange(z_min, deltaZ_He, 0.1)
    add_ion_HeII  = interpoalate_1D( add_z_He, z_0+deltaZ_He, ion_HeII ) 
    add_heat_HeII = interpoalate_1D( add_z_He, z_0+deltaZ_He, heat_HeII ) 
    z_He  = np.concatenate([ add_z_He, z_He ])
    ion_HeII  = np.concatenate([ add_ion_HeII,  ion_HeII ])
    heat_HeII = np.concatenate([ add_heat_HeII, heat_HeII ])
    
  modified_rates['UVBRates']['Chemistry']['k24'] = ion_HI
  modified_rates['UVBRates']['Chemistry']['k26'] = ion_HeI
  modified_rates['UVBRates']['Chemistry']['k25'] = ion_HeII
  modified_rates['UVBRates']['Photoheating']['piHI']   = heat_HI
  modified_rates['UVBRates']['Photoheating']['piHeI']  = heat_HeI
  modified_rates['UVBRates']['Photoheating']['piHeII'] = heat_HeII
  modified_rates['UVBRates']['z_H'] = z_H
  modified_rates['UVBRates']['z_He'] = z_He
  
  rates_grid[sim_id] = modified_rates


file_name = root_dir + 'grid_uvb_rates_noextend.pkl'
Write_Pickle_Directory( rates_grid, file_name )

# base_dir = root_dir + 'simulation_files/'
# sim_dirs = [ base_dir + file for file in os.listdir(base_dir) if file[0]=='S' ]
# sim_dirs.sort()
# 
# 
# rates_all = {}
# for sim_id, sim_dir in enumerate( sim_dirs ):
#   file_name = f'{sim_dir}/UVB_rates.h5'
#   rates = Load_Grackle_File( file_name )
#   rates_all[sim_id+1] = rates
# 
# file_name = output_dir + 'grid_uvb_rates.pkl'
# Write_Pickle_Directory( rates_all, file_name )