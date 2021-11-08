import numpy as np

data_Fan = np.array([
[ 5.02966, 5.4095e-05  , 4.0575e-05 ,  7.105e-05   ],
[ 5.24756, 6.6661e-05  , 4.6229e-05 ,  9.1057e-05  ],
[ 5.44898, 6.6396e-05  , 4.2097e-05 ,  9.646e-05   ],
[ 5.64925, 8.6053e-05  , 4.9327e-05 ,  0.000130749 ],
[ 5.84893, 0.000119286 , 7.9097e-05 ,  0.000119286 ],
[ 6.09998, 0.00042856  , 0.000129703,  0.00042856  ]]).T
z = data_Fan[0]
xHI = data_Fan[1]
xHI_l = data_Fan[2]
xHI_h = data_Fan[3]
sigma_l = xHI - xHI_l
sigma_h = xHI_h - xHI
label = 'Fan et al. (2006)'
data_HI_fraction_Fan_2006 = { 'z':z, 'xHI':xHI, 'sigma_h':sigma_h, 'sigma_l':sigma_l, 'label':label } 


data_HI_fraction_Greig_2017 = { 'z':np.array([7.1]), 'xHI':np.array([.40]), 'sigma_h':np.array([.21]), 'sigma_l':np.array([.19]), 'label':'Greig et al. (2017)'  }
data_HI_fraction_Greig_2019 = { 'z':np.array([7.5]), 'xHI':np.array([.21]), 'sigma_h':np.array([.17]), 'sigma_l':np.array([.19]), 'label':'Greig et al. (2019)'  }

data_HI_fraction_Hoag_2019 = { 'z':np.array([7.6]), 'xHI':np.array([.88]), 'sigma_h':np.array([.05]), 'sigma_l':np.array([.1]), 'label':'Hoag et al. (2019)'  }

data_HI_fraction_Mason_2018 = { 'z':np.array([7.0]), 'xHI':np.array([.59]), 'sigma_h':np.array([.11]), 'sigma_l':np.array([.15]), 'label':'Mason et al. (2018)'  }

data_HI_fraction_Mason_2019 = { 'z':np.array([7.9]), 'xHI':np.array([.76]), 'sigma_h':np.array([.1]), 'sigma_l':np.array([.0]), 'label':'Mason et al. (2019)'  }

data_HI_fraction_McGreer_2011 = { 'z':np.array([5.5, 6.1]), 'xHI':np.array([.2, 0.5]), 'sigma_h':np.array([.0, 0.]), 'sigma_l':np.array([.1, .1]), 'label':'McGreer et al. (2011)'  }
data_HI_fraction_McGreer_2015 = { 'z':np.array([5.6, 5.9]), 'xHI':np.array([.04, 0.06]), 'sigma_h':np.array([.0, 0.]), 'sigma_l':np.array([.01, .02]), 'label':'McGreer et al. (2015)'  }

data_HI_fraction_Schroeder_2013 = { 'z':np.array([6.1]), 'xHI':np.array([.1]), 'sigma_h':np.array([.1]), 'sigma_l':np.array([.0]), 'label':'Schroeder et al. (2013)'  }

data_HI_fraction_Yang_2020 = { 'z':np.array([7.5]), 'xHI':np.array([0.39]), 'sigma_h':np.array([.22]), 'sigma_l':np.array([.13]), 'label':'Yang et al. (2020b)' } #Damping modeling of the quasar

data_HI_fraction_Wang_2020 = { 'z':np.array([7.0]), 'xHI':np.array([0.70]), 'sigma_h':np.array([.20]), 'sigma_l':np.array([.23]), 'label':'Wang et al. (2020)' } #Damping modeling of the quasar


