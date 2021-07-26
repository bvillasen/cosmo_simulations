import os, sys
from pathlib import Path
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools')
from tools import *
# from phase_diagram_functions import fit_thermal_parameters_mcmc, get_density_temperature_values_to_fit


def Fit_Grid_Phase_Diagram_MPI( self, n_mpi=30, n_nodes=1 ):
  print("Fitting Phase Diagram:")
  for sim_id in self.Grid.keys():
    self.Fit_Simulation_Phase_Diagram_MPI( sim_id, n_mpi=n_mpi, n_nodes=n_nodes )

def Fit_Simulation_Phase_Diagram_MPI( self, sim_id, n_mpi=30,  n_nodes=1  ):
  print( f' Fitting Simulation: {sim_id}')
  sim_dir = self.Get_Simulation_Directory( sim_id )
  input_dir = sim_dir + 'analysis_files/'
  cwd = os.getcwd()
  run_file = cwd + '/phase_diagram/fit_phase_diagram_mpi.py'
  parameters = sim_dir + 'analysis_files/'
  n_per_node = n_mpi // n_nodes + 1
  command = f'mpirun -n {n_mpi} --map-by ppr:{n_per_node}:node --oversubscribe python {run_file} {parameters}'
  print( f' Submitting: {command}' )
  os.system( command )

def Delete_grid_core_files( self ):
 sim_ids = self.sim_ids
 for sim_id in sim_ids:
   self.Delete_simulation_core_files( sim_id )
 
def Delete_simulation_core_files( self, sim_id ):
 sim_dir = self.Get_Simulation_Directory( sim_id )
 files = os.listdir( sim_dir )
 for file in files:
   if file.find('core') == 0:
     print( f'Removing: {sim_dir + file} ' )
     os.remove( sim_dir + file )
 
def Load_Grid_UVB_Rates( self ):
  print( 'Loading UVB Rates Files')
  sim_ids = self.Grid.keys()
  for sim_id in sim_ids:
    self.Load_Simulation_UVB_Rates( sim_id )
  
  
def Load_Simulation_UVB_Rates( self, sim_id ):
  sim_dir = self.Get_Simulation_Directory( sim_id )
  file_name = sim_dir + 'UVB_rates.h5'
  print( f' Loading File: {file_name}')
  file = h5.File( file_name, 'r' )
  rates = file['UVBRates']
  rates_out = {}
  for root_key in rates.keys():
    rates_out[root_key] = {}
    data_group = rates[root_key]
    if root_key in [ 'Chemistry', 'Photoheating']:
      for key in data_group.keys():
        rates_out[root_key][key] = data_group[key][...]
    else:
      rates_out[root_key] = data_group[...]
  self.Grid[sim_id]['UVB_rates'] = rates_out