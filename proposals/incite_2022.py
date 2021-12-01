

# Early Dark Energy Models
# Simulation: N=1024^3  L=25 Mpc/h    z_end=2  
node_hours_per_simulation = 60
n_simulations = 1000
time_EDE = n_simulations * node_hours_per_simulation
print( f'Time EDE: {time_EDE:.1f} node hrs')

# Neutrino Masses 
# Simulation: N=1024^3  L=25 Mpc/h    z_end=4  
node_hours_per_simulation = 30
n_simulations = 1000
time_neutrinos = n_simulations * node_hours_per_simulation
print( f'Time Neutrino masses: {time_neutrinos:.1f} node hrs')


# Thermal and Cosmolgy effects on BAOs
# Simulation: N=2048^3  L=200 Mpc/h    z_end=2  
node_hours_per_simulation = 250
n_simulations = 1000
time_BAOs = n_simulations * node_hours_per_simulation
print( f'Time BAOs: {time_BAOs:.1f} node hrs')

# Development and testing od RT simulations 
time_dev = 10000  
print( f'Time Development: {time_dev:.1f} node hrs')


time_total = time_EDE + time_neutrinos + time_BAOs + time_dev
print( f'Time TOTAL: {time_total:.1f} node hrs')
