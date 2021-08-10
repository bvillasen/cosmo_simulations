import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab

base_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(base_dir)]
sys.path.extend(subDirectories)
from tools import *
from plot_uvb_rates import Plot_HI_Photoionization

data_boss_irsic_boera = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera'
data_name = data_boss_irsic_boera

root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
input_dir = root_dir + f'fit_mcmc/{data_name}/observable_samples/' 
output_dir = data_dir + 'cosmo_sims/figures/nature/'
create_directory( output_dir ) 

# Obtain distribution of the UVBRates
file_name = input_dir + 'samples_uvb_rates_new.pkl' 
samples_uvb_rates = Load_Pickle_Directory( file_name )

ion_HI_data = samples_uvb_rates['photoionization_HI']
z = ion_HI_data['z']
ion_HI = ion_HI_data['Highest_Likelihood']
higher = ion_HI_data['higher']
lower  = ion_HI_data['lower'] 

rates_data = {}
rates_data[0] = { 'z':z, 'photoionization':ion_HI, 'higher':higher, 'lower':lower, 'label':'This Work' }


Plot_HI_Photoionization( output_dir, rates_data=rates_data, figure_name='fig_phothoionization_HI', show_low_z=True )