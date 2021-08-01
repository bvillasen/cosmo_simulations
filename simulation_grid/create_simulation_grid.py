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
from generate_grackle_uvb_file import Load_Grackle_File


SG = Simulation_Grid( parameters=Grid_Parameters, sim_params=sim_params, job_params=job_params, dir=root_dir )
SG.Create_Grid_Directory_Structure()
SG.Create_All_Parameter_Files( ics_type='cdm' )

grackle_UVB_file_name =  base_dir + 'rates_uvb/data/CloudyData_UVB_Puchwein2019_cloudy.h5' 
constant_UVB_parameters = { 'scale_He_ion':0.44, 'scale_H_ion':0.78, 'deltaZ_He':0.27, 'deltaZ_H':0.05 } 
SG.Create_UVB_Rates_Files( input_file_name=grackle_UVB_file_name, constant_parameters=constant_UVB_parameters )


figures_dir = root_dir + 'figures/'
create_directory( figures_dir ) 

# Plot the generated UVB Rates
rates_data = SG.Load_Grid_UVB_Rates()
Plot_UVB_Rates( figures_dir, SG=SG )
Plot_UVB_Rates( figures_dir, rates_data=rates_data, figure_name='UVB_rates_multiple.png' )


base_dir = root_dir + 'simulation_files/'
sim_dirs = [ base_dir + file for file in os.listdir(base_dir) if file[0]=='S' ]
sim_dirs.sort()
rates_all = {}
for sim_id, sim_dir in enumerate( sim_dirs ):
  file_name = f'{sim_dir}/UVB_rates.h5'
  rates = Load_Grackle_File( file_name )
  rates_all[sim_id] = rates
Plot_UVB_Rates( figures_dir, rates_data=rates_all, figure_name='UVB_rates_all.png' )
