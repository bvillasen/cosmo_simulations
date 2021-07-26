import sys, os
import numpy as np
import h5py as h5
import pickle
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *

grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
output_dir = grid_dir + f'sim_properties/'
create_directory( output_dir )

sim_dirs = [ dir for dir in os.listdir(grid_dir)  if dir[0] == 'S' ]
sim_dirs.sort()
n_sims = len( sim_dirs )

n_files = 56


sim_properties = {}
sim_id = 0
for sim_id in range( n_sims ):
  sim_dir = sim_dirs[sim_id]
  sim_prop = {}
  file_name =  grid_dir + f'/reduced_files/{sim_dir}/uvb_params.txt'
  file = open( file_name, 'r' )
  for line in file.readlines():
    p_name, val = line.split('=')
    p_val = float(val.split(' ')[0])
    sim_prop[p_name] = p_val
  file_name =  grid_dir + f'/reduced_files/{sim_dir}/UVB_rates.h5'
  file = h5.File( file_name, 'r' )
  uvb_rates = file['UVBRates']
  uvb_z = uvb_rates['z'][...]
  Gamma_HI   = uvb_rates['Chemistry']['k24'][...]
  Gamma_HeII = uvb_rates['Chemistry']['k26'][...]
  Gamma_HeI  = uvb_rates['Chemistry']['k25'][...]
  Heat_HI   = uvb_rates['Photoheating']['piHI'][...]
  Heat_HeI  = uvb_rates['Photoheating']['piHeI'][...]
  Heat_HeII = uvb_rates['Photoheating']['piHeII'][...]
  file.close()
  sim_prop['uvb'] = { 'z':uvb_z, 'Gamma_HI':Gamma_HI, 'Gamma_HeI':Gamma_HeI, 'Gamma_HeII':Gamma_HeII, 'Heat_HI':Heat_HI, 'Heat_HeI':Heat_HeI, 'Heat_HeII':Heat_HeII   }
  file_name =  grid_dir + f'/reduced_files/{sim_dir}/thermal_solution/solution.h5'
  file = h5.File( file_name, 'r' )
  th_z = file['z'][...][::-1]
  n_H  = file['n_H'][...][::-1]
  n_HI = file['n_HI'][...][::-1]
  n_He  = file['n_He'][...][::-1]
  n_HeII = file['n_HeII'][...][::-1]
  HI_frac = n_HI / n_H
  HeII_frac = n_HeII / n_He
  sim_prop['thermal'] = { 'z':th_z, 'HI_frac':HI_frac, 'HeII_frac':HeII_frac   }
  sim_z, sim_tau_HI, sim_tau_HeII, sim_T0, sim_gamma = [], [], [], [], []
  for n_file in range(10,n_files):
    file_name =  grid_dir + f'/reduced_files/{sim_dir}/analysis_files/{n_file}_analysis.h5'
    file = h5.File( file_name, 'r' )
    z = file.attrs['current_z'][0]
    lya_stats = file['lya_statistics']
    F_HI   = lya_stats.attrs['Flux_mean_HI'][0]
    F_HeII = lya_stats.attrs['Flux_mean_HeII'][0]
    tau_HI   = -np.log( F_HI )
    tau_HeII = -np.log( F_HeII )
    sim_z.append( z )
    sim_tau_HI.append( tau_HI )
    sim_tau_HeII.append( tau_HeII )
    file.close()
    file_name = grid_dir + f'/reduced_files/{sim_dir}/analysis_files/fit_mcmc_delta_0_1.0/fit_{n_file}.pkl'
    data_pd = Load_Pickle_Directory( file_name )
    T0 = data_pd['T0']['mean']
    gamma = data_pd['gamma']['mean']
    sim_T0.append( 10**T0 )
    sim_gamma.append( gamma + 1 )
  sim_z = np.array( sim_z )
  sim_tau_HI   = np.array( sim_tau_HI )
  sim_tau_HeII = np.array( sim_tau_HeII )
  sim_T0 = np.array( sim_T0 )
  sim_gamma = np.array( sim_gamma )
  sim_prop['z']        = sim_z[::-1]
  sim_prop['tau_HI']   = sim_tau_HI[::-1]
  sim_prop['tau_HeII'] = sim_tau_HeII[::-1]
  sim_prop['T0']       = sim_T0[::-1]
  sim_prop['gamma']    = sim_gamma[::-1]
  sim_properties[sim_id] = sim_prop




header_fields = 'sim_id beta_He beta_H delta_z_He delta_z_H T0[K] gamma tau_HI tau_HeII HI_fraction Gamma_HI[1/s] Gamma_HeII[1/s] Heating_HI[eV/s] Heating_HeII[eV/s] HeII_fraction'
current_z = 2.0


z_vals = [ 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0 ]
z_vals = [ 4.0 ]
for current_z in z_vals:
  header = f'Redshift {current_z} \n'
  for i, field in enumerate( header_fields.split(' ')):
    header += f'column {i}: {field} \n' 
  header = header[:-2]   

  sim_prop_all = []
  for sim_id in range(n_sims):
    sim_prop = sim_properties[sim_id]
    sim_prop_out = [ sim_id,  ]
    for key in [ 'scale_He', 'scale_H', 'deltaZ_He', 'deltaZ_H' ]:
      sim_prop_out.append( sim_prop[key] )
    for key in [ 'T0', 'gamma', 'tau_HI', 'tau_HeII' ]:
      z = sim_prop['z']
      vals = sim_prop[key]
      val = np.interp( current_z, z, vals )
      sim_prop_out.append( val )
    HI_frac = np.interp( current_z, sim_prop['thermal']['z'], sim_prop['thermal']['HI_frac']  )
    HI_frac = min( 1.0, HI_frac )
    HeII_frac = np.interp( current_z, sim_prop['thermal']['z'], sim_prop['thermal']['HeII_frac']  )
    HeII_frac = min( 1.0, HeII_frac )
    sim_prop_out.append( HI_frac )
    for key in [ 'Gamma_HI', 'Gamma_HeII', 'Heat_HI', 'Heat_HeII' ]:
      z = sim_prop['uvb']['z']
      vals = sim_prop['uvb'][key]
      val = np.interp( current_z, z, vals )
      sim_prop_out.append( val )
    if HeII_frac < 0: print( f'HeII_frac: {HeII_frac}' )
    if HI_frac < 0: print( f'HI_frac: {HI_frac}' )
    sim_prop_out.append( HeII_frac )  
    sim_prop_all.append( sim_prop_out )

  sim_prop_all = np.array( sim_prop_all )

  output_file_name = output_dir + f'properties_z_{current_z}_HeII.txt'
  np.savetxt( output_file_name, sim_prop_all, header=header )
  print( f'Saved File: {output_file_name}' )
