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

data_boss_irsic_boera = 'fit_results_P(k)+tau_HeII_Boss_Irsic_Boera_systematic'
data_name = data_boss_irsic_boera

root_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/'
input_dir = root_dir + f'fit_mcmc/{data_name}/observable_samples/' 

output_dir = data_dir + 'cosmo_sims/figures/paper_thermal_history/'
create_directory( output_dir ) 

# Obtain distribution of the UVBRates
file_name = input_dir + 'samples_uvb_rates_new.pkl' 
samples_uvb_rates = Load_Pickle_Directory( file_name )

ion_HI_data = samples_uvb_rates['photoionization_HI']
z = ion_HI_data['z'] - 0.06
ion_HI = ion_HI_data['Highest_Likelihood']
higher = ion_HI_data['higher']
lower  = ion_HI_data['lower'] 
indices = z > 6.1
higher[indices] *=10
indices = z > 5.9
lower[indices] *= 1
rates_data = {}
rates_data[0] = { 'z':z, 'photoionization':ion_HI, 'higher':higher, 'lower':lower, 'label':'This Work (Best-Fit)', }
z_original = z

modified_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_modified_gamma_sigmoid/'
file_name = modified_dir + 'UVB_rates_2.h5'
file = h5.File( file_name, 'r' )
z = file['UVBRates']['z'][...]
photoionization_HI = file['UVBRates']['Chemistry']['k24'][...]
indices = z < 4.8
z_0 = z[indices]
photoionization_HI[indices] = 10**np.interp( z_0, z_original, np.log10(ion_HI)) 
# indices = z > 6.2
# z_0 = z[indices]
# photoionization_HI[indices] = 10**np.interp( z_0, z_original, np.log10(ion_HI)) 
rates_data[1] = { 'z':z, 'photoionization':photoionization_HI, 'label': r'Modified to Match HI $\tau_{\mathrm{eff}}$' }

rates_data[0]['line_color'] = 'k'
rates_data[1]['line_color'] = 'C0'

rates_data[0]['ls'] = '-'
rates_data[1]['ls'] = '--'


rates_data[0]['lw'] = 3.5
rates_data[1]['lw'] = 2.5



Plot_HI_Photoionization( output_dir, rates_data=rates_data, figure_name='Gamma_HI', show_low_z=True )