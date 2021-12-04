import os, sys
from os import listdir
from os.path import isfile, join
import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
root_dir = os.path.dirname(os.getcwd()) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from load_data import load_snapshot_data_distributed, load_analysis_data
from tools import *


input_dir_0 = data_dir + 'cosmo_sims/256_hydro_50Mpc/analysis_files/'
input_dir_1 = data_dir + 'cosmo_sims/256_hydro_50Mpc/output_files/'
output_dir = data_dir + 'cosmo_sims/256_hydro_50Mpc/figures/'
create_directory( output_dir ) 

precision = np.float64
Lbox = 50000.0    #kpc/h
n_cells = 256
box_size = [ Lbox, Lbox, Lbox ]
grid_size = [ n_cells, n_cells, n_cells ] #Size of the simulation grid


n_snaps = 48

fields = [ 'density'  ]
z, diff_gas, diff_dm = [], [], []

n_snap = 0
data = load_analysis_data( n_snap, input_dir_0 )

