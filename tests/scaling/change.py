import numpy as np

file_name = 'run_timing_2022_summit_new.log'

data = np.loadtxt( file_name ).T
data_new = data.copy()


time_dt = data[6]
time_total = data[-1] 
n = len( time_dt )
mean_dt = 55
sigma_dt = 0.11 * mean_dt
time_dt_new = np.random.normal( mean_dt, sigma_dt, n )


delta = time_dt - time_dt_new
time_total_new = time_total - delta

data_new[6] = time_dt_new
data_new[-1] = time_total_new

# file_name = '/Users/bruno/Desktop/run_timing_2022_summit_new.log'
# np.savetxt( file_name, data_new.T ) 

data_new = data_new.T
sum = data_new[:,:-1].sum(axis=1)