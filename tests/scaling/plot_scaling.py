import os, sys
import numpy as np 
import matplotlib.pyplot as plt
cosmo_dir = os.path.dirname( os.path.dirname(os.getcwd()) ) + '/'
subDirectories = [x[0] for x in os.walk(cosmo_dir)]
sys.path.extend(subDirectories)
# from tools import *

output_dir = '/Users/bruno/Desktop/'
# create_directory( output_dir )

# Load timing 
file_name = 'run_timing_2022_summit.log'
data = np.loadtxt( file_name ).T
n_proc = data[0]
n_steps = data[5] 
time_dt = data[6] / n_steps 
time_hydro = data[7] / n_steps
time_bound = data[8] / n_steps 
time_potential = data[9] / n_steps
time_pot_bound = data[10] / n_steps
time_part_dens = data[11] / n_steps 
time_part_bound = data[12] / n_steps
time_part_dens_bound = data[13] / n_steps
time_adv_part_1 = data[14] / n_steps 
time_adv_part_2 = data[15] / n_steps 
time_chemistry = data[16] / n_steps
time_total = data[17] / n_steps

n_proc_summit = n_proc 
time_hydro_summit = time_hydro 
time_gravity_summit = time_potential
time_mpi_summit = time_bound + time_pot_bound + time_part_bound + time_part_dens_bound
time_particles_summit = time_dt + time_part_dens + time_adv_part_1 + time_adv_part_2
time_chemistry_summit = time_chemistry
time_total_summit = time_total


# Load timing 
file_name = 'run_timing_2022_crusher.log'
data = np.loadtxt( file_name ).T
n_proc = data[0]
n_steps = data[5] 
time_dt = data[6] / n_steps 
time_hydro = data[7] / n_steps
time_bound = data[8] / n_steps 
time_potential = data[9] / n_steps
time_pot_bound = data[10] / n_steps
time_part_dens = data[11] / n_steps 
time_part_bound = data[12] / n_steps
time_part_dens_bound = data[13] / n_steps
time_adv_part_1 = data[14] / n_steps 
time_adv_part_2 = data[15] / n_steps 
time_chemistry = data[16] / n_steps
time_total = data[17] / n_steps

n_proc_crusher = n_proc
time_hydro_crusher = time_hydro 
time_gravity_crusher = time_potential
time_mpi_crusher = time_bound + time_pot_bound + time_part_bound + time_part_dens_bound
time_particles_crusher = time_dt + time_part_dens + time_adv_part_1 + time_adv_part_2
time_chemistry_crusher = time_chemistry
time_total_crusher = time_total

import matplotlib
matplotlib.rcParams['font.sans-serif'] = "Helvetica"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['mathtext.rm'] = 'serif'

colors = [ 'C0', 'C1', 'C2', 'C3', 'C4', 'k']

nrows, ncols = 1, 1
fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6*ncols,6*nrows))

ax.plot( n_proc_summit, time_hydro_summit,     label='Hydro',c=colors[0]     , ls='-'  )
ax.plot( n_proc_summit, time_mpi_summit,       label='MPI',c=colors[1]       , ls='-'  )
ax.plot( n_proc_summit, time_gravity_summit,   label='Poisson',c=colors[2]   , ls='-'  )
ax.plot( n_proc_summit, time_particles_summit, label='Particles',c=colors[3] , ls='-'  )
ax.plot( n_proc_summit, time_chemistry_summit, label='Chemistry',c=colors[4] , ls='-'  )
ax.plot( n_proc_summit, time_total_summit,     label='Total',c=colors[5]     , ls='-'  )

ax.plot( n_proc_crusher, time_hydro_crusher,     c=colors[0]     , ls='--'  )
ax.plot( n_proc_crusher, time_mpi_crusher,       c=colors[1]       , ls='--'  )
ax.plot( n_proc_crusher, time_gravity_crusher,   c=colors[2]   , ls='--'  )
ax.plot( n_proc_crusher, time_particles_crusher, c=colors[3] , ls='--'  )
ax.plot( n_proc_crusher, time_chemistry_crusher, c=colors[4] , ls='--'  )
ax.plot( n_proc_crusher, time_total_crusher,     c=colors[5]     , ls='--'  )


ax.legend( loc=2, frameon=False, fontsize=11 )

ax.set_xscale('log')

ax.set_xlabel('Number of GPUs')
ax.set_ylabel('Milliseconds per time-step ')

figure_name = output_dir + f'cholla_scaling_summit_2022.png'
fig.savefig( figure_name, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor() )
print( f'Saved Figure: {figure_name}' )
