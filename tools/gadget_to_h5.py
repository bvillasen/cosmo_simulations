import os, sys
import h5py as h5
import numpy as np
import yt
from tools import *



input_dir = '/data/groups/comp-astro/nicole/wfirst1024/Gadget/'


n_snap = 500

infile_name =  input_dir + f'snapshot_{n_snap:03}'
print('\nLoading Gadget file:', infile_name)

ds = yt.load( infile_name )
data = ds.all_data()

