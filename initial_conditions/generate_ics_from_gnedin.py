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
from read_gic import ReadFileHeader, ReadDen, ReadXV

# hydro, particles = False, False
# args = sys.argv
# n_args = len(args)
# if n_args == 1:
#   print( 'Missing type: hydro or particles')
#   exit(-1)
# 
# type = args[1]
# if type == 'hydro': hydro = True
# if type == 'particles': particles = True

# Box Size
Lbox = 50000.0    #kpc/h
n_points = 1024
n_boxes  = 16
L_Mpc = int( Lbox / 1000)

input_dir = data_dir + f'cosmo_sims/ics/gnedin/IC/'
# output_dir = data_dir + f'cosmo_sims/ics/{n_points}_{L_Mpc}Mpc/'

file_base_name = 'rei20A_mr1'


d = ReadDen( input_dir + file_base_name + '_B.den')
# d_dm = ReadDen( input_dir + file_base_name + '_D.den')
(x,y,z) = ReadXV(input_dir + file_base_name + '_D.pos')
# (vx_0,vy_0,vz_0) = ReadXV(input_dir + file_base_name + '_B.vel')
# (vx_1,vy_1,vz_1) = ReadXV(input_dir + file_base_name + '_D.vel')


# path = input_dir 
# d = ReadDen(path+"/rei20A_mr1_B.den")
# (x,y,z) = ReadXV(path+"/rei20A_mr1_D.pos")
# 
# import matplotlib.pyplot as plt
# 
# fig = plt.figure(figsize=(8,4))
# 
# ax1 = fig.add_subplot(1,2,1)
# ax2 = fig.add_subplot(1,2,2)
# 
# ax1.imshow(d[0,:,:],origin="lower")
# ax2.scatter(x[0],y[0],s=1)
# 
# fig.savefig( input_dir+'fig.png')

# plt.show()

# 
# import matplotlib.pyplot as plt
# 
# fig = plt.figure(figsize=(8,4))
# 
# ax1 = fig.add_subplot(1,2,1)
# ax2 = fig.add_subplot(1,2,2)
# 
# ax1.imshow(d[0,:,:],origin="lower")
# ax2.scatter(x[0],y[0],s=1)
# 
# 
# plt.show()

# create_directory( output_dir )
# output_dir += f'ics_{n_boxes}_z100/'
# create_directory( output_dir )
# print(f'Input Dir: {input_dir}' )
# print(f'Output Dir: {output_dir}' )

# data_ics = { 'dm':{}, 'gas':{} }
# data_ics['current_a'] = file_attrs['a_start']
# data_ics['current_z'] = file_attrs['z_start']
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
# if type == 'particles':
#   p_pos_x = Load_Particles_Field( 'pos_x', input_dir, attrs=file_attrs )
#   p_pos_y = Load_Particles_Field( 'pos_y', input_dir, attrs=file_attrs )
#   p_pos_z = Load_Particles_Field( 'pos_z', input_dir, attrs=file_attrs )
#   p_vel_x = Load_Particles_Field( 'vel_x', input_dir, attrs=file_attrs )
#   p_vel_y = Load_Particles_Field( 'vel_y', input_dir, attrs=file_attrs )
#   p_vel_z = Load_Particles_Field( 'vel_z', input_dir, attrs=file_attrs )
# 
#   data_ics['dm']['p_mass'] = file_attrs['dm_particle_mass']
#   data_ics['dm']['pos_x'] = p_pos_x
#   data_ics['dm']['pos_y'] = p_pos_y
#   data_ics['dm']['pos_z'] = p_pos_z
#   data_ics['dm']['vel_x'] = p_vel_x
#   data_ics['dm']['vel_y'] = p_vel_y
#   data_ics['dm']['vel_z'] = p_vel_z
# 
# 
# 
# 
# if n_boxes == 1: proc_grid  = [ 1, 1, 1 ]
# if n_boxes == 2: proc_grid  = [ 2, 1, 1 ]
# if n_boxes == 8: proc_grid  = [ 2, 2, 2 ]
# if n_boxes == 16: proc_grid = [ 4, 2, 2 ]
# if n_boxes == 32: proc_grid = [ 4, 4, 2 ]
# if n_boxes == 64: proc_grid = [ 4, 4, 4 ]
# if n_boxes == 128: proc_grid = [ 8, 4, 4 ]
# 
# n_snapshot = 0
# box_size = [ Lbox, Lbox, Lbox ]
# grid_size = [ n_points, n_points, n_points ]
# output_base_name = '{0}_particles.h5'.format( n_snapshot )
# if particles: generate_ics_particles(data_ics, output_dir, output_base_name, proc_grid, box_size, grid_size)
# 
# output_base_name = '{0}.h5'.format( n_snapshot )
# if hydro: expand_data_grid_to_cholla( proc_grid, data_ics['gas'], output_dir, output_base_name )