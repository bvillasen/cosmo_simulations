import os, sys
from os import listdir
from os.path import isfile, join
import h5py as h5
import numpy as np
import subprocess
import yt
#Extend path to inclide local modules
root_dir = os.path.dirname(os.getcwd())
sub_directories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(sub_directories)
from tools import *
from ics_particles import generate_ics_particles
from ics_grid import expand_data_grid_to_cholla
from constants_cosmo import G_COSMO, Gcosmo
from internal_energy import get_temperature, get_internal_energy

correction_factor = 1.0000563343966022


# Box Size
Lbox = 50000.0    #kpc
n_points = 256
n_boxes  = 16
L_Mpc = int( Lbox / 1000)

input_dir = data_dir + f'cosmo_sims/ics/enzo/{n_points}_{L_Mpc}Mpc_test/'
output_dir = data_dir + f'cosmo_sims/ics/enzo/{n_points}_{L_Mpc}Mpc_test/'

create_directory( output_dir )
output_dir += f'ics_{n_boxes}_z100/'
create_directory( output_dir )
print(f'Input Dir: {input_dir}' )
print(f'Output Dir: {output_dir}' )

# Load Enzo Dataset
nSnap = 0
snapKey = '{0:03}'.format(nSnap)
inFileName = 'DD0{0}_v1/data0{0}'.format( snapKey)
ds = yt.load( input_dir + inFileName )
data = ds.all_data()
h = ds.hubble_constant
current_z = np.float(ds.current_redshift)
current_a = 1./(current_z + 1)

print( 'Loading Hydro Data')
data_grid = ds.covering_grid( level=0, left_edge=ds.domain_left_edge, dims=ds.domain_dimensions )
gas_density_enzo = data_grid[ ('gas', 'density')].in_units('msun/kpc**3').v*current_a**3/h**2
gas_vel_x_enzo = data_grid[('gas','velocity_x')].in_units('km/s').v
gas_vel_y_enzo = data_grid[('gas','velocity_y')].in_units('km/s').v
gas_vel_z_enzo = data_grid[('gas','velocity_z')].in_units('km/s').v
gas_U_enzo = data_grid[('gas', 'thermal_energy' )].v * 1e-10 * gas_density_enzo #km^2/s^2
# gas_u = data_grid[('gas', 'thermal_energy' )].v * 1e-10 
gas_E_enzo = 0.5 * gas_density_enzo * ( gas_vel_x_enzo*gas_vel_x_enzo + gas_vel_y_enzo*gas_vel_y_enzo + gas_vel_z_enzo*gas_vel_z_enzo ) + gas_U_enzo

print( 'Loading Particles Data')
p_mass = data[('all', 'particle_mass')].in_units('msun').v*h
p_pos_x_enzo = data[('all', 'particle_position_x')].in_units('kpc').v/current_a*h
p_pos_y_enzo = data[('all', 'particle_position_y')].in_units('kpc').v/current_a*h
p_pos_z_enzo = data[('all', 'particle_position_z')].in_units('kpc').v/current_a*h
p_vel_x_enzo = data[('all', 'particle_velocity_x')].in_units('km/s').v
p_vel_y_enzo = data[('all', 'particle_velocity_y')].in_units('km/s').v
p_vel_z_enzo = data[('all', 'particle_velocity_z')].in_units('km/s').v


field_name = 'GridDensity'
file_name = input_dir + field_name
file = h5.File( file_name, 'r' )
attrs = file.attrs

temperature = 231.44931976 #k
n_cells = attrs['Dimensions']
n_particles = n_cells.prod()
dx = attrs['dx']
h = attrs['h0']
box_size = n_cells * dx * h
if (box_size == box_size[0]).sum() != 3:
  print( 'ERROR: Box is not a cube')
  exit(-1)
box_size = box_size[0]
H0 = h * 100
a_start = attrs['a_start']
z_start = 1 / a_start -1
Omega_b = attrs['omega_b']
Omega_m = attrs['omega_m']
Omega_l = attrs['omega_v']
# v_factor = attrs['vfact'] / 1.11593191              # The number is a factor to match the velocities obtained when loading the sim snapshot with yt
# v_unit = 1.0/(1.225e2*np.sqrt(Omega_m/a_start))   
# Gcosmo *= 0.9999434393004225  # The number is a factor to match the particle mass obtained when loading the sim snapshot with yt
rho_crit = 3*(H0*1e-3)**2/(8*np.pi* Gcosmo) / h / h  * correction_factor # h^2 Msun kpc^-3 
rho_mean = rho_crit * Omega_m
rho_mean_dm  = rho_crit * ( Omega_m - Omega_b )
rho_mean_gas = rho_crit * Omega_b
factor = Omega_b/Omega_m 
dm_particle_mass =  rho_mean_dm * (Lbox)** 3  / n_particles
L_unit = Lbox / H0 / (1+z_start)
rho_0 = 3 * Omega_m * (100* H0*1e-3 )**2 / ( 8 * np.pi * Gcosmo )
time_unit = 1/np.sqrt(  4 * np.pi * Gcosmo * rho_0 * (1+z_start)**3 )
vel_unit = L_unit / time_unit 

print( f'\nCosmological Parameters:' )
print( f'Dimensions: {n_cells} ' )
print( f'Lbox: {Lbox:.1f} Mpc/h' )
print( f'z_start: {z_start:.1f}' )
print( f'H0: {H0:.2f}' )
print( f'Omega_b: {Omega_b:.4f}' )
print( f'Omega_m: {Omega_m:.4f}' )
print( f'Omega_l: {Omega_l:.4f}' )
print( f'rho_mean: {rho_mean:.2f}' )
print( f'rho_mean_gas: {rho_mean_gas:.2f}' )
print( f'Temperature: {temperature:.2f}' )
print( f'N particles: {n_particles} ' )
print( f'Particle mass: {dm_particle_mass:.2e} Msun/h' )

print( f'Loading Field: {field_name}' )
gas_overdensity = file[field_name][...][0].T / factor
gas_density = rho_mean_gas * gas_overdensity
file.close()

field_name = 'GridVelocities_x'
print( f'Loading Field: {field_name}' )
file_name = input_dir + field_name
file = h5.File( file_name, 'r' )
gas_vel_x = file[field_name][...][0].T * vel_unit
file.close()

field_name = 'GridVelocities_y'
print( f'Loading Field: {field_name}' )
file_name = input_dir + field_name
file = h5.File( file_name, 'r' )
gas_vel_y = file[field_name][...][0].T * vel_unit
file.close()

field_name = 'GridVelocities_z'
print( f'Loading Field: {field_name}' )
file_name = input_dir + field_name
file = h5.File( file_name, 'r' )
gas_vel_z = file[field_name][...][0].T * vel_unit
file.close()

gas_U = get_internal_energy( temperature ) * gas_density
gas_E = 0.5*gas_density*( gas_vel_x*gas_vel_x + gas_vel_y*gas_vel_y + gas_vel_z*gas_vel_z ) + gas_U

diff_gas_dens = ( gas_density - gas_density_enzo ) / gas_density_enzo
diff_gas_vel_x = ( gas_vel_x - gas_vel_x_enzo ) / gas_vel_x_enzo
diff_gas_vel_y = ( gas_vel_y - gas_vel_y_enzo ) / gas_vel_y_enzo
diff_gas_vel_z = ( gas_vel_z - gas_vel_z_enzo ) / gas_vel_z_enzo
diff_gas_U = ( gas_U - gas_U_enzo ) / gas_U_enzo
diff_gas_E = ( gas_E - gas_E_enzo ) / gas_E_enzo

print( f'Diff gas density: min:{diff_gas_dens.min()}  max:{diff_gas_dens.max()}' )
print( f'Diff gas vel_x: min:{diff_gas_vel_x.min()}  max:{diff_gas_vel_x.max()}' )
print( f'Diff gas vel_y: min:{diff_gas_vel_y.min()}  max:{diff_gas_vel_y.max()}' )
print( f'Diff gas vel_z: min:{diff_gas_vel_z.min()}  max:{diff_gas_vel_z.max()}' )
print( f'Diff internal_energy: min:{diff_gas_U.min()}  max:{diff_gas_U.max()}' )
print( f'Diff total_energy:    min:{diff_gas_E.min()}  max:{diff_gas_E.max()}' )



delta_x = 1. / n_points
field_name = 'ParticleDisplacements_x'
print( f'Loading Field: {field_name}' )
file_name = input_dir + field_name
file = h5.File( file_name, 'r' )
p_delta_x = file[field_name][...][0].T
file.close()
ones_1d = np.ones( n_points )
p_pos_x = np.meshgrid( ones_1d, ones_1d, ones_1d )[0]
for slice_id in range(n_points):
  p_pos_x[slice_id,:, :] *= (slice_id + 0.5) * delta_x
p_pos_x += p_delta_x
p_pos_x = p_pos_x.flatten() 
p_pos_x[p_pos_x < 0] += 1 
p_pos_x[p_pos_x > 1] -= 1
p_pos_x *= Lbox 
p_pos_x.sort() 
p_pos_x_enzo.sort()
diff_pos_x = ( p_pos_x - p_pos_x_enzo ) / p_pos_x_enzo 
print( f'Diff particles pos_x: min:{diff_pos_x.min()}  max:{diff_pos_x.max()}' )


delta_y = 1. / n_points
field_name = 'ParticleDisplacements_y'
print( f'Loading Field: {field_name}' )
file_name = input_dir + field_name
file = h5.File( file_name, 'r' )
p_delta_y = file[field_name][...][0].T
file.close()
ones_1d = np.ones( n_points )
p_pos_y = np.meshgrid( ones_1d, ones_1d, ones_1d )[0]
for slice_id in range(n_points):
  p_pos_y[:,slice_id, :] *= (slice_id + 0.5) * delta_y
p_pos_y += p_delta_y
p_pos_y = p_pos_y.flatten() 
p_pos_y[p_pos_y < 0] += 1 
p_pos_y[p_pos_y > 1] -= 1
p_pos_y *= Lbox 
p_pos_y.sort() 
p_pos_y_enzo.sort()
diff_pos_y = ( p_pos_y - p_pos_y_enzo ) / p_pos_y_enzo 
print( f'Diff particles pos_y: min:{diff_pos_y.min()}  max:{diff_pos_y.max()}' )



delta_z = 1. / n_points
print( f'Loading Field: {field_name}' )
field_name = 'ParticleDisplacements_z'
file_name = input_dir + field_name
file = h5.File( file_name, 'r' )
p_delta_z = file[field_name][...][0].T
file.close()
ones_1d = np.ones( n_points )
p_pos_z = np.meshgrid( ones_1d, ones_1d, ones_1d )[0]
for slice_id in range(n_points):
  p_pos_z[:, :, slice_id] *= (slice_id + 0.5) * delta_z
p_pos_z += p_delta_z
p_pos_z = p_pos_z.flatten() 
p_pos_z[p_pos_z < 0] += 1 
p_pos_z[p_pos_z > 1] -= 1
p_pos_z *= Lbox 
p_pos_z.sort() 
p_pos_z_enzo.sort()
diff_pos_z = ( p_pos_z - p_pos_z_enzo ) / p_pos_z_enzo 
print( f'Diff particles pos_z: min:{diff_pos_z.min()}  max:{diff_pos_z.max()}' )


field_name = 'ParticleVelocities_x'
print( f'Loading Field: {field_name}' )
file_name = input_dir + field_name
file = h5.File( file_name, 'r' )
p_vel_x = file[field_name][...][0].T
file.close()
p_vel_x = p_vel_x.flatten() * vel_unit
p_vel_x.sort() 
p_vel_x_enzo.sort()
diff_vel_x = ( p_vel_x - p_vel_x_enzo ) / p_vel_x_enzo 
print( f'Diff particles vel_x: min:{diff_vel_x.min()}  max:{diff_vel_x.max()}' )

field_name = 'ParticleVelocities_y'
print( f'Loading Field: {field_name}' )
file_name = input_dir + field_name
file = h5.File( file_name, 'r' )
p_vel_y = file[field_name][...][0].T
file.close()
p_vel_y = p_vel_y.flatten() * vel_unit
p_vel_y.sort() 
p_vel_y_enzo.sort()
diff_vel_y = ( p_vel_y - p_vel_y_enzo ) / p_vel_y_enzo 
print( f'Diff particles vel_y: min:{diff_vel_y.min()}  max:{diff_vel_y.max()}' )

field_name = 'ParticleVelocities_z'
print( f'Loading Field: {field_name}' )
file_name = input_dir + field_name
file = h5.File( file_name, 'r' )
p_vel_z = file[field_name][...][0].T
file.close()
p_vel_z = p_vel_z.flatten() * vel_unit
p_vel_z.sort() 
p_vel_z_enzo.sort()
diff_vel_z = ( p_vel_z - p_vel_z_enzo ) / p_vel_z_enzo 
print( f'Diff particles vel_z: min:{diff_vel_z.min()}  max:{diff_vel_z.max()}' )
