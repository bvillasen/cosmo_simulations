import os, sys
from pathlib import Path
import numpy as np
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools')
from tools import *


def Delete_core_files( self, sim_id ):
 sim_dir = self.Get_Simulation_Directory( sim_id )
 files = os.listdir( sim_dir )
 for file in files:
   if file.find('core') == 0:
     print( sim_dir + file )
 
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