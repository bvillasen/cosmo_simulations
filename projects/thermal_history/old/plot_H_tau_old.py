import sys, os
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import matplotlib
import palettable
import pylab
root_dir = os.path.dirname(os.path.dirname(os.getcwd())) + '/'
subDirectories = [x[0] for x in os.walk(root_dir)]
sys.path.extend(subDirectories)
from tools import *
from plot_optical_depth import Plot_tau_HI
from colors import *

black_background = True

input_dir = data_dir + 'cosmo_sims/sim_grid/1024_P19m_np4_nsim400/fit_mcmc/fit_results_P(k)+tau_HeII_Boss_Irsic_Boera_systematic/'
modified_dir = data_dir + 'cosmo_sims/rescaled_P19/1024_50Mpc_modified_gamma_sigmoid/analysis_files/'
output_dir = data_dir + f'cosmo_sims/figures/paper_thermal_history/'
if black_background: output_dir += 'black_background/'
create_directory( output_dir )


file_name = input_dir + f'observable_samples/samples_fields.pkl'
fields_sim_data = Load_Pickle_Directory( file_name )

line_color = 'k'
if black_background: line_color = purples[1]

data_tau = fields_sim_data['tau']
data_to_plot = {}
data_to_plot[0] = { 'z':data_tau['z'], 'tau':data_tau['Highest_Likelihood'], 'high':data_tau['higher']*1.03, 'low':data_tau['lower']*0.97}
data_to_plot[0]['label'] = 'This Work (Best-Fit)'
data_to_plot[0]['line_color'] = line_color
data_to_plot[0]['lw'] = 3.0

n_files = 56
z_vals, tau_vals = [], []
for n_file in range(n_files):
  file_name = modified_dir + f'{n_file}_analysis.h5'
  file = h5.File( file_name, 'r' )
  z = file.attrs['current_z'][0]
  F = file['lya_statistics'].attrs['Flux_mean_HI'][0]
  tau = -np.log(F)
  z_vals.append( z )
  tau_vals.append( tau )
z_vals = np.array( z_vals )
tau_vals = np.array( tau_vals )

indices  = z_vals < 4.5
tau_0 = data_tau['Highest_Likelihood']
tau_vals[indices] = data_tau['Highest_Likelihood'][indices]

indices  = z_vals >= 6.1
tau_vals[indices] = data_tau['Highest_Likelihood'][indices]

line_color = 'k'
if black_background: line_color = 'C0'


data_to_plot[1] = { 'z':z_vals, 'tau':tau_vals }
data_to_plot[1]['line_color'] = line_color
data_to_plot[1]['label'] = r'Modified to Match HI $\tau_{\mathrm{eff}}$'
data_to_plot[1]['ls'] = '--'
data_to_plot[1]['lw'] = 2.5

Plot_tau_HI( output_dir,  samples_tau_HI=data_to_plot, labels='', black_background=black_background, figure_name='tau_HI.png'  )




