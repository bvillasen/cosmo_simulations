import sys, os, time
import numpy
from filecmp import dircmp
from shutil import copyfile, copytree, move
base_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from transfer_grid_functions import *

sim_grid_dir = data_dir + 'cosmo_sims/sim_grid/'
 
# wdm_mass = 1.0 
 
# if wdm_mass == 2.0: src_grid_dir = sim_grid_dir + '1024_mwdm2p0_nsim64/' 
# if wdm_mass == 3.0: src_grid_dir = sim_grid_dir + '1024_mwdm3p0_nsim64/' 
# if wdm_mass == 4.0: src_grid_dir = sim_grid_dir + '1024_mwdm4p0_nsim64/' 
# if wdm_mass == 5.0: src_grid_dir = sim_grid_dir + '1024_mwdm5p0_nsim64/' 
# if wdm_mass == 6.0: src_grid_dir = sim_grid_dir + '1024_mwdm6p0_nsim64/' 
# dst_grid_dir = sim_grid_dir + '1024_wdmgrid_nsim320/'

# src_grid_dir = sim_grid_dir + '1024_wdmgrid_nsim200_deltaZ_n0p5/'
# dst_grid_dir = sim_grid_dir + '1024_wdmgrid_nsim600/'

src_grid_dir = sim_grid_dir + '1024_wdmgrid_nsim600/'
dst_grid_dir = sim_grid_dir + '1024_wdmgrid_nsim900/'

# constant_params = { 'wdm_mass': wdm_mass }
constant_params = None

src_params = Get_Grid_Parameter_Values( src_grid_dir, constant_params=constant_params )
dst_params = Get_Grid_Parameter_Values( dst_grid_dir )
Link_Simulation_dirctories( src_params, dst_params )

dst_ids_to_transfer = [ id for id in dst_params if dst_params[id]['src']  is not None ]
n_to_transfer = len( dst_ids_to_transfer )
print( f'N to transfer: {n_to_transfer} ' )

# directories_to_copy = [ ]
# directories_to_copy = [ 'analysis_files', 'simulation_files' ]
# directories_to_copy = [ 'skewers_files' ] 
# directories_to_copy = [ 'transmitted_flux', 'flux_power_spectrum' ]
# directories_to_copy = [ 'flux_power_spectrum' ] 
directories_to_copy = [ 'analysis_files', 'simulation_files', 'flux_power_spectrum' ] 

# directories_to_move = [ 'snapshot_files' ]
directories_to_move = []

# sim_files_to_copy = [ 'run_output.log' ]
sim_files_to_copy = [  ]

n_transferred = 0
for dst_id in dst_ids_to_transfer:
  # if n_transferred > 0: continue
  dst_data = dst_params[dst_id]
  dst_root_dir = dst_data['root_dir']
  dst_name = dst_data['name']
  src_id = dst_data['src']['id']
  src_root_dir = dst_data['src']['root_dir']
  src_name = dst_data['src']['name']
  print( f'\nCopying {src_name} -> {dst_name}' )

  if 'snapshot_files' in  directories_to_move:
    src_dir = src_root_dir + f'snapshot_files/{src_name}/'
    dst_dir = dst_root_dir + f'snapshot_files/{dst_name}/'
    print( f' src dir: {src_dir}' )
    print( f' dst dir: {dst_dir}' )
    src_content = os.listdir( src_dir )
    dst_content_0 = os.listdir( dst_dir )
    if len( dst_content_0 ) == 0: 
      os.rmdir( dst_dir )
      print( ' Moving Directory')
      dst_result = move( src_dir, dst_dir )
    dst_content = os.listdir( dst_dir )
    n_files_src = len( src_content )
    n_files_dst = len( dst_content )
    if n_files_src != n_files_dst:
      print( 'ERROR: Number of files in src and dst directories differs' )
      time.sleep(2)
    
  if 'analysis_files' in  directories_to_copy:
    src_dir = src_root_dir + f'analysis_files/{src_name}/'
    dst_dir = dst_root_dir + f'analysis_files/{dst_name}/'
    print( f' src dir: {src_dir}' )
    print( f' dst dir: {dst_dir}' )
    dst_content = os.listdir( dst_dir )
    if len( dst_content ) == 0: 
      os.rmdir( dst_dir )
      dst_result = copytree( src_dir, dst_dir )
    dir_comparison = dircmp( src_dir, dst_dir )
    # comparison_result = dir_comparison.report()
    diff_files = dir_comparison.diff_files
    if len( diff_files ) > 0: 
      print( 'ERROR: Found diff_files > 0')
      time.sleep(2)
      
  if 'transmitted_flux' in  directories_to_copy:
    dst_transmitted_flux_dir = dst_root_dir + f'transmitted_flux'
    if not os.path.isdir( dst_transmitted_flux_dir ): create_directory( dst_transmitted_flux_dir )
    src_dir = src_root_dir + f'transmitted_flux/{src_name}/'
    dst_dir = dst_root_dir + f'transmitted_flux/{dst_name}/'
    print( f' src dir: {src_dir}' )
    print( f' dst dir: {dst_dir}' )
    if os.path.isdir( dst_dir ):
      dst_content = os.listdir( dst_dir )
      if len( dst_content ) == 0: 
        os.rmdir( dst_dir )
        dst_result = copytree( src_dir, dst_dir )
    else: dst_result = copytree( src_dir, dst_dir )
    dir_comparison = dircmp( src_dir, dst_dir )
    diff_files = dir_comparison.diff_files
    if len( diff_files ) > 0: 
      print( 'ERROR: Found diff_files > 0')
      time.sleep(2)

  if 'flux_power_spectrum' in  directories_to_copy:
    dst_ps_dir = dst_root_dir + f'flux_power_spectrum'
    if not os.path.isdir( dst_ps_dir ): create_directory( dst_ps_dir )
    src_dir = src_root_dir + f'flux_power_spectrum/{src_name}/'
    dst_dir = dst_root_dir + f'flux_power_spectrum/{dst_name}/'
    print( f' src dir: {src_dir}' )
    print( f' dst dir: {dst_dir}' )
    if os.path.isdir( dst_dir ):
      dst_content = os.listdir( dst_dir )
      if len( dst_content ) == 0: 
        os.rmdir( dst_dir )
        dst_result = copytree( src_dir, dst_dir )
    else: dst_result = copytree( src_dir, dst_dir )
    dir_comparison = dircmp( src_dir, dst_dir )
    diff_files = dir_comparison.diff_files
    if len( diff_files ) > 0: 
      print( 'ERROR: Found diff_files > 0')
      time.sleep(2)
      

  if 'skewers_files' in directories_to_copy:
    src_dir = src_root_dir + f'skewers_files/{src_name}/'
    dst_dir = dst_root_dir + f'skewers_files/{dst_name}/'
    print( f' src dir: {src_dir}' )
    print( f' dst dir: {dst_dir}' )
    dst_content = os.listdir( dst_dir )
    if len( dst_content ) == 0: 
      os.rmdir( dst_dir )
      dst_result = copytree( src_dir, dst_dir )
    dir_comparison = dircmp( src_dir, dst_dir )
    # comparison_result = dir_comparison.report()
    diff_files = dir_comparison.diff_files
    if len( diff_files ) > 0: 
      print( 'ERROR: Found diff_files > 0')
      time.sleep(2)
  

  if 'simulation_files' in directories_to_copy:
    src_dir = src_root_dir + f'simulation_files/{src_name}/'
    if os.path.isdir( src_dir + 'original' ): src_dir = src_dir + 'original/' 
    dst_dir = dst_root_dir + f'simulation_files/{dst_name}/original/'
    print( f' src dir: {src_dir}' )
    print( f' dst dir: {dst_dir}' )
    create_directory( dst_dir, print_out=False )
    dst_content = os.listdir( dst_dir )
    if len( dst_content ) == 0: 
      os.rmdir( dst_dir )
      dst_result = copytree( src_dir, dst_dir )
    dir_comparison = dircmp( src_dir, dst_dir )
    # comparison_result = dir_comparison.report()
    diff_files = dir_comparison.diff_files
    if len( diff_files ) > 0: 
      print( 'ERROR: Found diff_files > 0')
    if len( sim_files_to_copy  ) > 0:
      for file_name in sim_files_to_copy:
        src_file = dst_root_dir + f'simulation_files/{dst_name}/original/' + file_name
        dst_file = dst_root_dir + f'simulation_files/{dst_name}/' + file_name
        copyfile( src_file, dst_file )
    
  n_transferred += 1

print( f'\nSuccessfully transfered {n_transferred} simulations')

    


# 
# 
# 
# 
# files_to_copy = []
# 
# # files_to_copy = ['run_output.log', 'param.txt', 'uvb_params.txt']
# # directories_to_copy = [ 'analysis_files' ]
# 
# files_to_copy = []
# directories_to_copy = [ ]
# 
# copy_simulation_directory = False
# 
# 
# 
# n_copied, n_skipped = 0, 0
# n_dst_sims = len( dst_params )
# dst_ids_to_transfer = range( n_dst_sims )
# # dst_ids_to_transfer = [ 64 ]
# 
# for sim_id in dst_ids_to_transfer:
#   dst_sim = dst_params[sim_id]
#   dst_dir = dst_sim['dir']
#   src_dir = dst_sim['src_dir']
#   if src_dir:
#     src_id = dst_sim['src_id']
#     src_sim  = src_params[src_id]
#     failed = False 
#     for param_name in dst_sim['parameters']:
#       if dst_sim['parameters'][param_name] != src_sim['parameters'][param_name]:
#         print( "ERROR: Parameters dont match {dst_sim['parameters']}, {src_sim['parameters']}") 
#         failed = True
#     if failed: break
# 
#     print( f"\nCopying: {src_sim['parameters']} ->  {dst_sim['parameters']}  ")
# 
# 
#     src_dir_short = src_dir[src_dir.find('sim_grid')+9:]+'/'
#     dst_dir_short = dst_dir[dst_dir.find('sim_grid')+9:]+'/' 
#     for file in files_to_copy:
#       copyfile(src_dir + '/' + file, dst_dir + '/' + file )
#       print( f' Copied  {src_dir_short+file} -> {dst_dir_short+file} ' )
# 
# 
#     for dir in directories_to_copy:
#       dst_indir = dst_dir + '/' + dir 
#       dst_dir_content = os.listdir(dst_indir)
#       if len(dst_dir_content) == 0:
#         print( f' Deleting Empty: {dst_indir}')
#         os.rmdir( dst_dir + '/' + dir )
#         print( f' Copying  {src_dir_short+dir} -> {dst_dir_short+dir} ' )  
#         copytree(src_dir + '/' + dir, dst_indir )
#         print( f' Copied   {src_dir_short+dir} -> {dst_dir_short+dir} ' )  
# 
# 
#     if move_reduced_snapshots:
#       src_red_dir = src_reduced_snapshots + src_sim['name']
#       dst_red_dir = dst_reduced_snapshots + dst_sim['name']
#       src_red_short = src_red_dir[src_red_dir.find('sim_grid')+9:]+'/'
#       dst_red_short = dst_red_dir[dst_red_dir.find('sim_grid')+9:]+'/'
#       print( f' Moving  {src_red_short} -> {dst_red_short} ' ) 
#       src_exits = os.path.isdir( src_red_dir)
#       if not src_exits: 
#         print( f'ERROR: Directory Doesnt Exists: { src_red_dir} ')
#         break
#       dst_exits = os.path.isdir( dst_red_dir)
#       if dst_exits: 
#         print( f'ERROR: Directory Exists: {dst_red_dir} ')
#         break
#       files = os.listdir( src_red_dir )
#       n_files = len(files)
#       print( f' N Files in src dir: {n_files} ' )
#       if n_files != 1920:
#         print( 'ERROR: n_files != 1920 ')
#         break
#       move( src_red_dir, dst_red_dir )
#       # print ( f'{src_red_dir} -> {dst_red_dir} ')
#       files = os.listdir( dst_red_dir )
#       n_files = len(files)
#       print( f' N Files in dst dir: {n_files} ' )
#       if n_files != 1920:
#         print( 'ERROR: n_files != 1920 ')
#         break
# 
#     if copy_reduced_files:
#       src_red_dir = src_reduced + src_sim['name']
#       dst_red_dir = dst_reduced + dst_sim['name']
#       src_red_short = src_red_dir[src_red_dir.find('sim_grid')+9:]+'/'
#       dst_red_short = dst_red_dir[dst_red_dir.find('sim_grid')+9:]+'/' 
#       dst_dir_content = os.listdir(dst_red_dir)
#       # print(dst_dir_content )
#       dst_analysis = dst_red_dir + '/analysis_files'
#       dst_mcmc = dst_red_dir + "/analysis_files/fit_mcmc"
#       copy_directory = False
#       empty_mcmc = False
#       if os.path.isdir( dst_analysis ):
#         if os.path.isdir( dst_mcmc ):
#           if len( os.listdir(dst_mcmc) ) == 0:
#             empty_mcmc = True
#             print( f' Deleting Empty: {dst_red_dir + "/analysis_files/fit_mcmc"}')
#             os.rmdir( dst_red_dir + '/analysis_files/fit_mcmc' )
#             copy_directory = True
#         if len( os.listdir(dst_analysis) ) == 0:
#           print( f' Deleting Empty: {dst_red_dir + "/analysis_files"}')
#           os.rmdir( dst_red_dir + '/analysis_files' )
#           copy_directory = True
#   # 
#       if copy_directory:
#         print( f' Deleting Empty: { dst_red_dir }')
#         os.rmdir( dst_red_dir )
#         copytree(src_red_dir, dst_red_dir )
#         print( f' Copied  {src_red_short} -> {dst_red_short} ' )
#       else: print( f'Skipped: {dst_red_dir}' )
#       # time.sleep(0.1)
# 
#     if copy_power_spectrum_files:
#       src_ps_dir = src_ps + src_sim['name']
#       dst_ps_dir = dst_ps + dst_sim['name']
#       src_ps_short = src_ps_dir[src_ps_dir.find('sim_grid')+9:]+'/'
#       dst_ps_short = dst_ps_dir[dst_ps_dir.find('sim_grid')+9:]+'/' 
#       dst_dir_content = os.listdir(dst_ps_dir)
#       if len(dst_dir_content) == 0:
#         os.rmdir( dst_ps_dir )
#         copytree(src_ps_dir, dst_ps_dir )
#         print( f' Copied  {src_ps_short} -> {dst_ps_short} ' )
#         time.sleep( 0.1 )
# 
# 
# 
#     n_copied += 1
#   else:
#     n_skipped += 1
# 
# 
# 
# print( f'\nSuccessfully Transfered Grid:   n_copied:{n_copied}    n_skipped:{n_skipped}')
# 
# 
