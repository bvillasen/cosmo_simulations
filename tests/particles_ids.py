import os, sys
from os import listdir
from os.path import isfile, join
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from load_data import load_snapshot_data_distributed
from tools import *


input_dir = data_dir + 'sphere/output_files/'

precision = np.float64
Lbox = 1.0    #kpc/h
n_cells = 256
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid

fields = [ 'density', 'particle_IDs' ]

n_snap = 0

data = load_snapshot_data_distributed( 'particles', fields, n_snap, input_dir, box_size, grid_size,  precision, show_progess=True, print_fields=True )
dens = data['density']      
p_ids = data['particle_IDs']    
n_total = len( p_ids )
print(f'n_total: {n_total}')

# p_ids.sort()
print(p_ids)

ids = np.linspace( 0, n_total-1, n_total ).astype(int)

