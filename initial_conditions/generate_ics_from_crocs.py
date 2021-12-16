import os, sys
from os import listdir
from os.path import isfile, join
import h5py as h5
import numpy as np
import subprocess
#Extend path to inclide local modules
root_dir = os.path.dirname(os.getcwd())
sub_directories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(sub_directories)
from tools import *
from ics_particles import generate_ics_particles
from ics_grid import expand_data_grid_to_cholla
from internal_energy import get_internal_energy
from constants_cosmo import Gcosmo
from read_gic import ReadFileHeader, ReadDen, ReadXV

type = 'particles'

# Box Size
Lbox = 40000.0    #kpc/h
n_points = 1024
n_boxes  = 16
L_Mpc = int( Lbox / 1000)

dark_matter_only_simulation = True

# file_base_name = 'rei20A_mr1'
# file_base_name = 'rei20A_mr2'
file_base_name = 'rei40A_mr2'
simulation_dir = data_dir + f'cosmo_sims/crocs_comparison/{file_base_name}/'
input_dir  = simulation_dir + f'ics_crocs/'
output_dir = simulation_dir + f'ics/'
create_directory( output_dir )

# Load gas fields
# gas_dens = ReadDen( input_dir + file_base_name + '_B.den')
# header, (gas_vel_x, gas_vel_y, gas_vel_z) = ReadXV(input_dir + file_base_name + '_B.vel')

data_key = 'M'
header, (p_pos_x, p_pos_y, p_pos_z) = ReadXV(input_dir + file_base_name + f'_{data_key}.pos')
header, (p_vel_x, p_vel_y, p_vel_z) = ReadXV(input_dir + file_base_name + f'_{data_key}.vel')

p_pos_x = p_pos_x.flatten() * 1e3
p_pos_y = p_pos_y.flatten() * 1e3
p_pos_z = p_pos_z.flatten() * 1e3
p_pos_x[p_pos_x<0] += Lbox
p_pos_y[p_pos_y<0] += Lbox
p_pos_z[p_pos_z<0] += Lbox
p_pos_x[p_pos_x>Lbox] -= Lbox
p_pos_y[p_pos_y>Lbox] -= Lbox
p_pos_z[p_pos_z>Lbox] -= Lbox

p_pos_x[p_pos_x == Lbox] -= Lbox * 1e-6
p_pos_x[p_pos_x == 0]    += Lbox * 1e-6
p_pos_y[p_pos_y == Lbox] -= Lbox * 1e-6
p_pos_y[p_pos_y == 0]    += Lbox * 1e-6
p_pos_z[p_pos_z == Lbox] -= Lbox * 1e-6
p_pos_z[p_pos_z == 0]    += Lbox * 1e-6

p_vel_x = p_vel_x.flatten()
p_vel_y = p_vel_y.flatten()
p_vel_z = p_vel_z.flatten()


n_particles = len(p_pos_x)
print( f'N particles: {n_particles} ' )

a_start = header['abeg']
z_start = 1/a_start - 1
Omega_dm = header['OmegaD']
Omega_b = header['OmegaB']
Omega_m = Omega_dm + Omega_b
Omega_l = header['OmegaL']
h = header['h100']
H0 = h * 100
rho_crit = 3 * (H0 *1e-3) **2 / ( 8 * np.pi * Gcosmo ) / h / h
rho_mean_gas = rho_crit * Omega_b
rho_mean_dm = rho_crit * Omega_dm
rho_mean = rho_crit * Omega_m
if dark_matter_only_simulation: rho_mean_dm = rho_mean

dm_particle_mass =  rho_mean * (Lbox)** 3  / n_particles #Msun/h

data_ics = { 'dm':{}, 'gas':{} }
data_ics['current_a'] = a_start
data_ics['current_z'] = z_start
#
# if type == 'hydro':
#   gas_density = Load_Gas_Field( 'density', input_dir, attrs=file_attrs )
#   gas_vel_x = Load_Gas_Field( 'vel_x', input_dir, attrs=file_attrs )
#   gas_vel_y = Load_Gas_Field( 'vel_y', input_dir, attrs=file_attrs )
#   gas_vel_z = Load_Gas_Field( 'vel_z', input_dir, attrs=file_attrs )
#   gas_U = get_internal_energy( temperature ) * gas_density
#   gas_E = 0.5*gas_density*( gas_vel_x*gas_vel_x + gas_vel_y*gas_vel_y + gas_vel_z*gas_vel_z ) + gas_U
#
#   data_ics['gas']['density'] = gas_density
#   data_ics['gas']['momentum_x'] = gas_density * gas_vel_x
#   data_ics['gas']['momentum_y'] = gas_density * gas_vel_y
#   data_ics['gas']['momentum_z'] = gas_density * gas_vel_z
#   data_ics['gas']['GasEnergy'] = gas_U
#   data_ics['gas']['Energy'] = gas_E
#
#
if type == 'particles':

  data_ics['dm']['p_mass'] = dm_particle_mass
  data_ics['dm']['pos_x'] = p_pos_x
  data_ics['dm']['pos_y'] = p_pos_y
  data_ics['dm']['pos_z'] = p_pos_z
  data_ics['dm']['vel_x'] = p_vel_x
  data_ics['dm']['vel_y'] = p_vel_y
  data_ics['dm']['vel_z'] = p_vel_z




if n_boxes == 1: proc_grid  = [ 1, 1, 1 ]
if n_boxes == 2: proc_grid  = [ 2, 1, 1 ]
if n_boxes == 8: proc_grid  = [ 2, 2, 2 ]
if n_boxes == 16: proc_grid = [ 4, 2, 2 ]
if n_boxes == 32: proc_grid = [ 4, 4, 2 ]
if n_boxes == 64: proc_grid = [ 4, 4, 4 ]
if n_boxes == 128: proc_grid = [ 8, 4, 4 ]

n_snapshot = 0
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_points, n_points, n_points ]
output_base_name = '{0}_particles.h5'.format( n_snapshot )
generate_ics_particles(data_ics, output_dir, output_base_name, proc_grid, box_size, grid_size)

output_base_name = '{0}.h5'.format( n_snapshot )
# if hydro: expand_data_grid_to_cholla( proc_grid, data_ics['gas'], output_dir, output_base_name )
