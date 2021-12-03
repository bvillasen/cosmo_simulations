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
from load_enzo_ics_file import Load_File_Attrs, Load_Gas_Field, Load_Particles_Field

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
gas_E_enzo = 0.5 * gas_density_enzo * ( gas_vel_x_enzo*gas_vel_x_enzo + gas_vel_y_enzo*gas_vel_y_enzo + gas_vel_z_enzo*gas_vel_z_enzo ) + gas_U_enzo


temperature = 231.44931976   #k
file_attrs = Load_File_Attrs( input_dir )
file_attrs['Lbox'] = Lbox 

gas_density = Load_Gas_Field( 'density', input_dir, attrs=file_attrs )
gas_vel_x = Load_Gas_Field( 'vel_x', input_dir, attrs=file_attrs )
gas_vel_y = Load_Gas_Field( 'vel_y', input_dir, attrs=file_attrs )
gas_vel_z = Load_Gas_Field( 'vel_z', input_dir, attrs=file_attrs )
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



print( 'Loading Particles Data')
# p_mass = data[('all', 'particle_mass')].in_units('msun').v*h
p_pos_x_enzo = data[('all', 'particle_position_x')].in_units('kpc').v/current_a*h
p_pos_y_enzo = data[('all', 'particle_position_y')].in_units('kpc').v/current_a*h
p_pos_z_enzo = data[('all', 'particle_position_z')].in_units('kpc').v/current_a*h
p_vel_x_enzo = data[('all', 'particle_velocity_x')].in_units('km/s').v
p_vel_y_enzo = data[('all', 'particle_velocity_y')].in_units('km/s').v
p_vel_z_enzo = data[('all', 'particle_velocity_z')].in_units('km/s').v



p_pos_x = Load_Particles_Field( 'pos_x', input_dir, attrs=file_attrs )
p_pos_y = Load_Particles_Field( 'pos_y', input_dir, attrs=file_attrs )
p_pos_z = Load_Particles_Field( 'pos_z', input_dir, attrs=file_attrs )
p_vel_x = Load_Particles_Field( 'vel_x', input_dir, attrs=file_attrs )
p_vel_y = Load_Particles_Field( 'vel_y', input_dir, attrs=file_attrs )
p_vel_z = Load_Particles_Field( 'vel_z', input_dir, attrs=file_attrs )



p_pos_x.sort()
p_pos_x_enzo.sort()
diff_pos_x = ( p_pos_x - p_pos_x_enzo ) / p_pos_x_enzo 

p_pos_y.sort()
p_pos_y_enzo.sort()
diff_pos_y = ( p_pos_y - p_pos_y_enzo ) / p_pos_y_enzo 

p_pos_z.sort()
p_pos_z_enzo.sort()
diff_pos_z = ( p_pos_z - p_pos_z_enzo ) / p_pos_z_enzo 

p_vel_x.sort()
p_vel_x_enzo.sort()
diff_vel_x = ( p_vel_x - p_vel_x_enzo ) / p_vel_x_enzo 

p_vel_y.sort()
p_vel_y_enzo.sort()
diff_vel_y = ( p_vel_y - p_vel_y_enzo ) / p_vel_y_enzo 

p_vel_z.sort()
p_vel_z_enzo.sort()
diff_vel_z = ( p_vel_z - p_vel_z_enzo ) / p_vel_z_enzo 



print( f'Diff particles pos_x: min:{diff_pos_x.min()}  max:{diff_pos_x.max()}' )
print( f'Diff particles pos_y: min:{diff_pos_y.min()}  max:{diff_pos_y.max()}' )
print( f'Diff particles pos_z: min:{diff_pos_z.min()}  max:{diff_pos_z.max()}' )

print( f'Diff particles vel_x: min:{diff_vel_x.min()}  max:{diff_vel_x.max()}' )
print( f'Diff particles vel_y: min:{diff_vel_y.min()}  max:{diff_vel_y.max()}' )
print( f'Diff particles vel_z: min:{diff_vel_z.min()}  max:{diff_vel_z.max()}' )


