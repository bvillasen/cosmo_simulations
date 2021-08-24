import os, sys
from pathlib import Path
import numpy as np
import subprocess
root_dir = os.path.dirname(os.getcwd()) + '/'
sys.path.append( root_dir + 'tools')
from tools import *
#Append analysis directories to path
extend_path( root_dir )
from submit_job_scripts import Create_Submit_Job_Script_Lux, Create_Submit_Job_Script_Summit
from uvb_functions import Generate_Modified_Rates_File
from load_data import load_analysis_data
from phase_diagram_functions import fit_thermal_parameters_mcmc, get_density_temperature_values_to_fit
from simulation_parameters import system
from simulation_grid_functions import *


def Combine_List_Pair( a, b ):
  output = []
  for a_i in a:
    for b_i in b:
      if type(b_i) == list:
        add_in = [a_i] + b_i
      else:
        add_in = [ a_i, b_i]
      output.append( add_in )
  return output
  
   
class Simulation_Grid:
  n_paramters   = 0
  n_simulations = 0
  parameter_names = []
  root_dir = ''
  sim_param_indx_grid = None
  parameters = None
  Grid = None
  job_parameters = None
  simulation_parameters = None
  sim_ids = None
  
  def __init__( self, job_params=None, sim_params=None, parameters=None, dir=None ):
    print("Initializing Simulation Grid:")
    root_dir = dir
    n_param = len(parameters.keys())
    param_names = [ parameters[i]['name'] for i in range(n_param) ]
    n_sims = np.prod( [ len(parameters[i]['values']) for i in range(n_param) ] )  
    self.parameter_names = param_names
    self.n_paramters = n_param
    self.n_simulations = n_sims
    self.parameters = parameters
    self.root_dir = dir
    self.snapshots_dir  = dir + 'snapshot_files/'
    self.analysis_dir   = dir + 'analysis_files/'
    self.simulations_dir = dir + 'simulation_files/'
    self.skewers_dir    = dir + 'skewers_files/'
    self.job_parameters = job_params
    self.simulation_parameters = sim_params
    print( f" n_paramters: {self.n_paramters}")
    print( f" Paramters: {self.parameter_names}")
    print( f" n_simulations: {self.n_simulations}")
    print( f" Root Dir: {self.root_dir}")
    
    create_directory( self.root_dir )
    
    self.base_directories = [ self.snapshots_dir, self.simulations_dir, self.analysis_dir, self.skewers_dir ] 
    for directory in self.base_directories: create_directory( directory )
    
    param_keys = []
    indices_list = []
    for i in range(n_param):
      param_id = n_param - 1 - i
      param_keys.append( parameters[param_id]['key'] )
      n_vals = len( parameters[param_id]['values'] )
      indices_list.append( [ x for x in range(n_vals)] )
    
    sim_param_indx_grid = indices_list[0]
    for i in range( n_param-1 ):
      sim_param_indx_grid = Combine_List_Pair( indices_list[i+1], sim_param_indx_grid )
    assert( len(sim_param_indx_grid) == n_sims ), "N_simulations doesn't match Simulation Grid"
        
    sim_grid  = {}
    for sim_id in range( n_sims ):
      sim_grid[sim_id] = {}
      sim_grid[sim_id]['param_indices'] = sim_param_indx_grid[sim_id]
      name = 'S{0:03}'.format( sim_id )
      coords = ''
      for param_id in range(n_param):
        param = parameters[param_id]
        param_key = param['key']
        name += f'_{param_key}{sim_param_indx_grid[sim_id][param_id]}'
        coords += f'_{param_key}{sim_param_indx_grid[sim_id][param_id]}'
      sim_grid[sim_id]['key'] = name
      sim_grid[sim_id]['coords'] = coords[1:] 
    
    for sim_id in range( n_sims ):
      sim_parameters = {}
      param_indices = sim_grid[sim_id]['param_indices']
      for param_id in range(n_param):
        param = parameters[param_id]
        param_name = param['name']
        param_indx = param_indices[param_id]
        param_val = parameters[param_id]['values'][param_indx]
        sim_parameters[param_name] = param_val
      sim_grid[sim_id]['parameters'] = sim_parameters
    
    coords = {}  
    for sim_id in range( n_sims ):
      coords[sim_grid[sim_id]['coords']] = sim_id
      
    for sim_id in range( n_sims ):
      parameter_values = []
      for p_id in range(n_param):
        p_name = parameters[p_id]['name']
        p_val = sim_grid[sim_id]['parameters'][p_name]
        parameter_values.append( p_val )
      sim_grid[sim_id]['parameter_values'] = np.array( parameter_values )
        
    self.Grid = sim_grid
    self.sim_ids = self.Grid.keys()
    self.coords = coords
  
###############################################################################################    
  Load_Grid_UVB_Rates = Load_Grid_UVB_Rates
  Load_Simulation_UVB_Rates = Load_Simulation_UVB_Rates
  Delete_simulation_core_files = Delete_simulation_core_files
  Delete_grid_core_files = Delete_grid_core_files
  Fit_Simulation_Phase_Diagram_MPI = Fit_Simulation_Phase_Diagram_MPI
  Fit_Grid_Phase_Diagram_MPI = Fit_Grid_Phase_Diagram_MPI

###############################################################################################    
  def Create_Grid_Directory_Structure( self ):
    n_sims = self.n_simulations
    for base_directory in self.base_directories:
      for sim_id in range( n_sims ):
        sim_name = self.Grid[sim_id]['key']
        dir_name = base_directory + sim_name
        create_directory( dir_name, print_out=False )
    print( 'Grid Directory Structure Created')

###############################################################################################    
  def Get_Simulation_Directory( self, sim_id ):
    simulations_dir = self.simulations_dir
    if simulations_dir[-1] != '/': simulations_dir += '/'
    simulation = self.Grid[sim_id]
    name = simulation['key']
    sim_dir = simulations_dir + name + '/'
    return sim_dir    
    
###############################################################################################    
  def Create_All_Parameter_Files( self, save_file=True, ics_type='cdm' ):
    print("Creating Parameter Files:")
    for sim_id in self.Grid.keys():
      self.Create_Simulation_Parameter_File( sim_id, save_file=save_file, ics_type=ics_type )
      self.Write_Grid_Parameters( sim_id )

###############################################################################################    
  def Create_Simulation_Parameter_File( self, sim_id, save_file=True, ics_type='cdm' ):
    sim_dir = self.Get_Simulation_Directory( sim_id )
    sim_params = self.simulation_parameters.copy()
    sim_params['UVB_rates_file'] = sim_dir + 'UVB_rates.h5'
    # sim_params['outdir'] = sim_dir + 'snapshot_files/'
    root_dir = self.root_dir
    if root_dir[-1] != '/': root_dir += '/'
    simulation = self.Grid[sim_id]
    name = self.Grid[sim_id]['key'] 
    sim_params['outdir']      = self.snapshots_dir + name + '/'
    sim_params['analysisdir'] = self.analysis_dir  + name + '/'
    sim_params['skewersdir']  = self.skewers_dir   + name + '/'
    
    if ics_type == 'cdm': input_dir = sim_params['indir']
    if ics_type == 'wdm':
      from simulation_parameters import Get_ICs_dir_wdm
      wdm_mass = simulation['parameters']['wdm_mass']
      input_dir = Get_ICs_dir_wdm( wdm_mass, sim_params )
      n_points = sim_params['nx']
      if n_points == 1024: input_dir = input_dir + f'/ics_128_z16/'
    sim_params['indir'] = input_dir
        
    if save_file:
      file_name = sim_dir + 'param.txt'
      file = open( file_name, 'w' )
      for key in sim_params.keys():
        string = f'{key}={sim_params[key]} \n'
        file.write( string )
      file.close()
      print( f' Saved File: {file_name}' )
      
###############################################################################################
  def Write_Grid_Parameters( self, sim_id ):
      sim_dir = self.Get_Simulation_Directory( sim_id )
      sim_params = self.Grid[sim_id]['parameters']
      file_name = sim_dir + 'grid_params.txt'
      file = open( file_name, 'w' )
      for key in sim_params.keys():
        string = f'{key}={sim_params[key]} \n'
        file.write( string )
      file.close()
      print( f' Saved File: {file_name}' )

###############################################################################################
  def Get_Simulation_Parameter_Values( self, sim_id ):
    param = self.parameters
    n_param = self.n_paramters
    simulation = self.Grid[sim_id]
    parameter_indices = simulation['param_indices']
    param_values = {}
    for param_id in range( n_param ):
      param_name = param[param_id]['name']
      param_indx = parameter_indices[param_id]
      param_values[param_name] = param[param_id]['values'][param_indx]
    return param_values

###############################################################################################
  def Create_UVB_Rates_Files( self, max_delta_z=0.1, input_file_name=None, input_UVB_rates=None, constant_parameters=None, extend_rates_z=True ):
    print("Creating UVB Rates Files:")
    for sim_id in self.Grid.keys():
      self.Create_UVB_Rates_File( sim_id, max_delta_z=max_delta_z, input_file_name=input_file_name, input_UVB_rates=input_UVB_rates, constant_parameters=constant_parameters, extend_rates_z=extend_rates_z )
      
###############################################################################################
  def Create_UVB_Rates_File( self, sim_id, max_delta_z=0.1, input_UVB_rates=None, input_file_name=None, constant_parameters=None, extend_rates_z=True ):
    simulation = self.Grid[sim_id]
    param_values =  self.Get_Simulation_Parameter_Values( sim_id )
    sim_dir = self.Get_Simulation_Directory( sim_id )
    out_file_name = sim_dir + 'UVB_rates.h5'
    if constant_parameters is not None:
      for p_name in constant_parameters:
        param_values[p_name] = constant_parameters[p_name]
    Generate_Modified_Rates_File(  out_file_name, param_values, max_delta_z=max_delta_z, input_file_name=input_file_name, input_UVB_rates=input_UVB_rates, extend_rates_z=extend_rates_z  )

###############################################################################################    
  def Submit_Grid_Jobs( self, n_submit=None, partition=None ):
    sim_ids = self.sim_ids
    self.Get_Grid_Status()
    n_submitted = 0
    for sim_id in sim_ids:
      status = self.Grid[sim_id]['status']
      # print( f' {sim_id}: {status}')
      if n_submit != None:
        if n_submitted >= n_submit: continue
      if status in ['failed', 'error', 'not submitted']:
        print( f'Submiting: {sim_id}')
        self.Submit_Simulation_Job( sim_id, partition=partition )
        n_submitted += 1
    print( f'Jobs Submitted: {n_submitted} ')

###############################################################################################    
  def Create_Submit_Job_Script( self, sim_id, save_file=True, partition='gpuq' ):
    root_dir = self.root_dir
    if root_dir[-1] != '/': root_dir += '/'
    simulation = self.Grid[sim_id]
    name = simulation['key']
    job_params = self.job_parameters.copy()
    job_params['name'] = name
    job_params['sim_directory'] = self.Get_Simulation_Directory( sim_id )
    job_params['partition'] = partition
    if system == 'Lux': Create_Submit_Job_Script_Lux( job_params, save_file=save_file )
    if system == 'Summit': Create_Submit_Job_Script_Summit( job_params, save_file=save_file )
    
###############################################################################################    
  def Submit_Simulation_Job( self, sim_id, partition=None ):
    sim_dir = self.Get_Simulation_Directory( sim_id )
    job = self.job_parameters
    if system == 'Summit':
      self.Create_Submit_Job_Script( sim_id, save_file=True )
      cwd = os.getcwd()
      os.chdir( sim_dir )
      command = f'bsub submit_job_summit.lsf'
    
    if system == 'Lux':
      if partition == None: partition = job['partition']
      partition_key = partition
      self.Create_Submit_Job_Script( sim_id, save_file=True, partition=partition )
      print( f'Submiting job to queue: {partition}')
      cwd = os.getcwd()
      os.chdir( sim_dir )
      if partition == 'comp-astro': partition_key = 'comp'
      if partition == 'gpuq':       partition_key = 'gpu'
      exclude_comand = '' 
      for node in job['exclude']:
        exclude_comand += node + ','
      if exclude_comand != '': exclude_comand = exclude_comand[:-1]
      command = f'submit_script {partition_key} submit_job_lux {exclude_comand}'
    # print( f'Changed Directory to: {sim_dir}')
    print( f' Submitting: {command}' )
    os.system( command )
    f = open("run_output.log", "a")
    f.write('Job Submitted.\n')
    f.close()
    os.chdir( cwd ) 

###############################################################################################    
  def Find_Simulation_In_Queue( self, sim_id, queue ):
    sim_key = 'S{0:03}'.format(sim_id)
    sim_in_queue = False
    queue_line = None
    for line in queue:
      indx = line.find( sim_key )
      if indx >= 0:
        sim_in_queue =  True
        queue_line = line
        break
    return sim_in_queue, queue_line

###############################################################################################    
  def Cancel_Simulation_Job( self, sim_id ):
    status = self.Get_Simulation_Status( sim_id )
    queue = self.Get_Queue_Staus()
    sim_in_queue, q_line = self.Find_Simulation_In_Queue( sim_id, queue )
    if sim_in_queue:
      elem = q_line[0]
      while elem == " ":
        q_line = q_line[1:]
        elem = q_line[0]
      job_id = q_line.split( ' ')[0]
      if system == 'Lux': command = f'scancel {job_id}'
      if system == 'Summit': command = f'bkill {job_id}'
      print( command )
      os.system( command )
###############################################################################################          
  def Cancel_Grid_Jobs( self, avoid=[] ):
    sim_ids = self.sim_ids
    for sim_id in sim_ids:
      if sim_id in avoid: continue
      self.Cancel_Simulation_Job( sim_id )

###############################################################################################    
  def Get_Simulation_Status( self, sim_id ):
    sim_dir = self.Get_Simulation_Directory( sim_id )
    file_name = sim_dir + 'run_output.log'
    file_path = Path( file_name)
    if file_path.is_file():
      file = open( file_name, 'r' )
      lines = file.readlines()
      if len(lines) == 0:
        status = 'failed'
      else:
        last_line = lines[-1]
        if last_line.find('Job Submitted') >= 0:
          status = 'submitted'
        elif last_line.find('Starting calculations') >= 0: 
          status = 'running'
        elif last_line.find('Simulation completed successfully.') >= 0: 
          status = 'finished'
        else: status = 'error'
    else:
      status = 'not submitted'
    return status


###############################################################################################    
  def Get_Queue_Staus( self ):
    if system == 'Lux': command = [ 'squeue', '--user=brvillas' ]
    if system == 'Summit': command = [ 'bjobs' ]
    if system == 'Shamrock': return ''
    queue = str( subprocess.check_output( command ) )
    queue = queue.split('\\n')
    return queue
    
###############################################################################################
  def Get_Grid_Status( self, check_queue=True ):
    print( '\nGrid Status: ')
    if check_queue:  queue = self.Get_Queue_Staus()
    sim_ids = self.Grid.keys()
    n = len(sim_ids)
    submitted, running, error, finished, failed = 0, 0, 0, 0, 0
    n_zero_pad = len( str(max(list(sim_ids)) ) )
    for sim_id in sim_ids:
      queue_line = ''
      status = self.Get_Simulation_Status( sim_id )
      self.Grid[sim_id]['status'] = status
      if status == 'submitted': 
        submitted += 1
        sim_in_queue, q_line = self.Find_Simulation_In_Queue( sim_id, queue )
        if sim_in_queue:
          elem = q_line[0]
          while elem == " ":
            q_line = q_line[1:]
            elem = q_line[0]
          queue_line = q_line
        else:
          status = 'failed'
          failed += 1
      if status == 'running': 
        submitted += 1
        sim_in_queue, q_line = self.Find_Simulation_In_Queue( sim_id, queue )
        if sim_in_queue:
          running += 1
          elem = q_line[0]
          while elem == " ":
            q_line = q_line[1:]
            elem = q_line[0]
          queue_line = q_line
        else:
          status = 'failed'
          failed += 1
      if status == 'finished': 
        submitted += 1
        finished += 1
      if status == 'error':
        error += 1
      # print( ' id: {sim_id:0{n_zero_pad}}   status: {status}   {queue_line}'.format(sim_id=sim_id, n_zero_pad=n_zero_pad, status=status, queue_line=queue_line ))
      n_spaces = n_zero_pad - len( str(sim_id))
      spaces = ' '*n_spaces
      print( f' id: {spaces}{sim_id}  status: {status}   {queue_line}' )
      # print( ' id: {sim_id:0{n_zero_pad}}   status: {status}   {queue_line}'.format(sim_id=sim_id, n_zero_pad=n_zero_pad, status=status, queue_line=queue_line ))
      self.Grid[sim_id]['status'] = status
    print( f'Submitted: {submitted} / {n}' )
    print( f'Running:   {running} / {n}' )
    print( f'Finished:  {finished} / {n}' )
    print( f'Failed:    {failed} / {n}' )
    print( f'Error:     {error} / {n}' )
          