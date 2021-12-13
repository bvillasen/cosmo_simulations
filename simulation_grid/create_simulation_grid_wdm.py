import os, sys
import numpy as np
base_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( base_dir + 'tools')
from tools import *
#Append analysis directories to path
extend_path()
from load_grid_parameters import Grid_Parameters
from simulation_grid import Simulation_Grid
from simulation_parameters import *
from plot_uvb_rates import Plot_UVB_Rates
from uvb_functions import Load_Grackle_File

print( f'Simulation Boxes: {Lbox/1000} Mpc/h' )
time.sleep(1)

grid_header = 'Base UVB Rates are the V21 rates (modified P19)'
# constant_UVB_parameters = None
constant_UVB_parameters = { 'deltaZ_H':0.5 } 

SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, constant_params=constant_UVB_parameters, 
                      job_params=job_params, dir=root_dir, grid_header=grid_header )
SG.Create_Grid_Directory_Structure()

# Select the type of initial conditions: 'cdm' or 'wdm'
# SG.Create_All_Parameter_Files( ics_type='cdm' )

# wdm_mass = None
wdm_mass = None
z_start = 100
n_file_start = 0
SG.Create_All_Parameter_Files( ics_type='wdm', wdm_mass=wdm_mass, verbose=False, z_start=z_start, n_file_start=n_file_start )

# Create the files for the UVB rates
# grackle_UVB_file_name =  base_dir + 'rates_uvb/data/CloudyData_UVB_Puchwein2019_cloudy.h5' 
# constant_UVB_parameters = { 'scale_He_ion':0.44, 'scale_H_ion':0.78, 'deltaZ_He':0.27, 'deltaZ_H':0.05 } 
# SG.Create_UVB_Rates_Files( input_file_name=grackle_UVB_file_name, constant_parameters=constant_UVB_parameters )
# 
grackle_UVB_file_name =  base_dir + 'rates_uvb/data/UVB_rates_P19m.h5' 
SG.Create_UVB_Rates_Files( input_file_name=grackle_UVB_file_name, extend_rates_z=False,  constant_parameters=constant_UVB_parameters, verbose=False  )


figures_dir = root_dir + 'figures/'
create_directory( figures_dir ) 

# Plot the generated UVB Rates
rates_data = SG.Load_Grid_UVB_Rates()
Plot_UVB_Rates( figures_dir, SG=SG )

base_dir = root_dir + 'simulation_files/'
sim_dirs = [ base_dir + file for file in os.listdir(base_dir) if file[0]=='S' ]
sim_dirs.sort()

rates_P19m = Load_Grackle_File( grackle_UVB_file_name )

rates_all = {}
rates_all[0] = rates_P19m 
for sim_id, sim_dir in enumerate( sim_dirs ):
  file_name = f'{sim_dir}/UVB_rates.h5'
  rates = Load_Grackle_File( file_name )
  rates_all[sim_id+1] = rates
  rates_all[sim_id+1]['line_style'] = '--'
Plot_UVB_Rates( figures_dir, rates_data=rates_all, figure_name='UVB_rates_all.png' )
