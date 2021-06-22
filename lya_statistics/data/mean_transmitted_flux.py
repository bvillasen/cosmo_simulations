import numpy as np


# From SAZERAC Sara's Bosman talk
data = np.array([ #z     mean_F  mean_F_up  mean_F_low
[ 4.80,  0.19433, 0.20981, 0.179306 ],
[ 4.90,  0.17159, 0.18571, 0.157536 ],
[ 5.00,  0.15818, 0.16686, 0.149176 ],
[ 5.10,  0.14269, 0.14833, 0.137317 ],
[ 5.20,  0.12137, 0.12707, 0.115806 ],
[ 5.30,  0.10161, 0.10641, 0.096239 ],
[ 5.40,  0.08004, 0.08470, 0.074404 ],
[ 5.50,  0.05878, 0.06261, 0.054124 ],
[ 5.60,  0.04446, 0.04829, 0.040387 ],
[ 5.70,  0.02483, 0.02807, 0.021662 ],
[ 5.80,  0.01673, 0.01978, 0.013950 ],
[ 5.90,  0.01109, 0.01446, 0.008051 ],
[ 6.00,  0.00811, 0.01109, 0.004873 ],
[ 6.10,  0.00784, 0.01607, 0.001112 ],
[ 6.20,  0.00395, 0.00842, -0.00044 ] ]).T

z = data[0]
mean_F = data[1]
mean_F_p = data[2]
mean_F_l = data[3]
mean_F_sigma = 0.5*(  mean_F_p - mean_F_l  )
delta_F_upper = mean_F_p - mean_F
delta_F_lower = mean_F - mean_F_l
data_mean_flux_bosman_2021 = { 'name':'Bosman et al. (from Sazerac)', 'z':z, 'F_mean':mean_F, 'sigma_F_mean':mean_F_sigma, 'delta_F_upper': delta_F_upper,  'delta_F_lower': delta_F_lower }