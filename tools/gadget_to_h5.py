import os, sys
import h5py as h5
import numpy as np
import yt
from tools import *
import read_gadget as gdt



input_dir = '/data/groups/comp-astro/nicole/wfirst1024/Gadget/'
input_dir = '/raid/bruno/data/cosmo_sims/wfirst_1024/snapshots/'
output_dir = input_dir + 'h5_files/'
create_directory( output_dir )


snapshots = np.arange( 50, 451, 50 )

for n_snap in snapshots:
  infile_name =  input_dir + f'snapshot_{n_snap:03}'
  print('\nLoading Gadget file:', infile_name)
  header, data = gdt.loadgadget_pos( infile_name )
  redshift = header.redshift
  box_size = float(header.boxsize) #kpc/h, comoving
  m = float(header.m) #Msol/h
  n_particles = int(header.N)
  pos_x, pos_y, pos_z = data.T #kpc/h

  current_z = redshift
  current_a = 1 / ( current_z + 1)


  outfile_name = output_dir + f'snapshot_{n_snap:03}.h5'
  outfile = h5.File( outfile_name, 'w' )

  outfile.attrs['current_a'] = current_a
  outfile.attrs['current_z'] = current_z
  outfile.attrs['particle_mass'] = m


  data = outfile.create_dataset( 'pos_x', data=pos_x )
  data = outfile.create_dataset( 'pos_y', data=pos_y )
  data = outfile.create_dataset( 'pos_z', data=pos_z )


  outfile.close()
  print( f'Saved File: {outfile_name}' )