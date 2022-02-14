import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
sys.path.append( cosmo_dir + 'lya_statistics/data' )
from tools import *
from figure_functions import *


grid_dir = data_dir + 'cosmo_sims/sim_grid/1024_wdmgrid_nsim600/'
fit_name = 'fit_results_P(k)+_Boera_covmatrix'
input_dir = grid_dir + f'fit_mcmc/{fit_name}/temperature_evolution'

files = [ f for f in os.listdir(input_dir) if f[0] == 's' ]
files.sort()