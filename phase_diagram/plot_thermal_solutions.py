import sys, os
import numpy as np
import h5py as h5
import pylab
import pickle
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import * 
from plot_thermal_history import Plot_T0_gamma_evolution

analysis_dir = root_dir + 'analysis_files/'
output_dir = root_dir + 'figures/'
create_directory( output_dir ) 

project_name = 'reduced_heating'

input_dir  = data_dir + f'modified_uvb_rates/{project_name}/thermal_solutions/'
output_dir = data_dir + f'modified_uvb_rates/{project_name}/figures/'
create_directory( output_dir )

n_models = 4
data_all = {}

for model_id in range(n_models):

  file_name = input_dir + f'solution_{model_id}.h5'
  file = h5.File( file_name, 'r' )
  z = file['z'][...]
  temperature = file['temperature'][...]
  file.close()
  data_all[model_id] = { 'z':z, 'T0':temperature }



Plot_T0_gamma_evolution(output_dir, data_sets=data_all, fig_name='fig_T0_reduced_photoheating.png', interpolate_lines=True,  plot_interval=False, T0_min=0 )
