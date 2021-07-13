import os, sys
import h5py as h5
import numpy as np
import yt
from tools import *
import read_gadget as gdt



input_dir = '/data/groups/comp-astro/nicole/wfirst2048/Gadget/'
output_dir =  data_dir + 'cosmo_sims/wfirst_2048/snapshots/h5_files/'
create_directory( output_dir )


snapshots = np.arange( 50, 501, 50 )

n_boxes = 8

for n_snap in snapshots:
  for n_box in range(n_boxes):
    infile_name =  input_dir + f'snapshot_{n_snap:03}.{n_box}'
    print('\nLoading Gadget file:', infile_name)
    header, data = gdt.loadgadget_pos_box( infile_name )
    redshift = header.redshift
    box_size = float(header.boxsize) #kpc/h, comoving
    m = float(header.m) #Msol/h
    n_particles = int(header.N)
    pos_x, pos_y, pos_z = data.T #kpc/h

    current_z = redshift
    current_a = 1 / ( current_z + 1)

    outfile_name = output_dir + f'snapshot_{n_snap:03}.{n_box}.h5'
    outfile = h5.File( outfile_name, 'w' )

    outfile.attrs['current_a'] = current_a
    outfile.attrs['current_z'] = current_z
    outfile.attrs['particle_mass'] = m

    data = outfile.create_dataset( 'pos_x', data=pos_x )
    data = outfile.create_dataset( 'pos_y', data=pos_y )
    data = outfile.create_dataset( 'pos_z', data=pos_z )

    outfile.close()
    print( f'Saved File: {outfile_name}' )