import numpy as np

data_jiani = np.array( [
[ 2.474864849900311192e+00, 2.518936420565516254e-01, 7.174543337252240697e-04 ],
[ 2.591309419655456914e+00, 2.883474836361683558e-01, 5.524159758959547610e-04 ],
[ 2.711362508206065058e+00, 3.371223848142201329e-01, 5.604326075037853721e-04 ],
[ 2.834202177298688508e+00, 3.680284086589403203e-01, 6.124303114267820028e-04 ],
[ 2.956922902396603714e+00, 3.946060912314548474e-01, 8.004899452313523223e-04 ],
[ 3.080214888163038900e+00, 4.348217257737682639e-01, 1.039951230299254389e-03 ],
[ 3.202791801878516864e+00, 4.801227260484299264e-01, 1.201013101308389319e-03 ],
[ 3.326037450776202942e+00, 5.339355486592979316e-01, 1.366201007512134842e-03 ],
[ 3.446160266024604457e+00, 5.860349546660713616e-01, 2.005032837878737654e-03 ],
[ 3.564701224363938437e+00, 6.344854736932603601e-01, 2.588174690982758368e-03 ],
[ 3.694878689641509784e+00, 7.092438898448540918e-01, 3.899311569575062385e-03 ],
[ 3.813348904928468563e+00, 7.570636013180213064e-01, 6.031563363114604559e-03 ],
[ 3.937099723544246199e+00, 8.470747242288079182e-01, 8.065366589366681355e-03 ],
[ 4.068927562750745963e+00, 9.755379017825053234e-01, 1.287850798172054771e-02 ],
[ 4.174598552232474447e+00, 1.036898350401118662e+00, 1.696608871083947132e-02 ],
[ 4.308174605488526154e+00, 1.152170573701994938e+00, 2.582691789902076887e-02 ] ]).T
z = data_jiani[0]
tau = data_jiani[1]
tau_error = data_jiani[2]
data_optical_depth_Jiani = {
'name':'Jiani ',
'z': z,
'tau': tau,
'tau_sigma': tau_error,
'tau_sigma_p': tau_error,
'tau_sigma_m': tau_error
}




data_keating = np.array( [
[ 4.2, 0.386215, 0.401744, 0.373139 ],
[ 4.4, 0.302689, 0.317515, 0.287006 ],
[ 4.6, 0.235014, 0.25179,  0.218802 ],
[ 4.8, 0.1695,   0.186972, 0.154833 ],
[ 5.0, 0.129563, 0.140772, 0.120686 ],
[ 5.2, 0.109078, 0.115458, 0.102487 ],
[ 5.4, 0.079947, 0.084354, 0.074827 ],
[ 5.6, 0.046133, 0.052229, 0.042031 ],
[ 5.8, 0.020964, 0.023283, 0.017795 ],
[ 6.0, 0.010206, 0.013067, 0.006533 ] ]).T
z = data_keating[0]
F = data_keating[1]
tau = -np.log(data_keating[1])
tau_p = -np.log(data_keating[2])
tau_m = -np.log(data_keating[3])
tau_error = ( tau_m - tau_p )/2 
data_optical_depth_Keating_2020 = {
'name':'Keating et al. (2020)',
'z': z,
'tau': tau,
'tau_sigma': tau_error,
'tau_sigma_p': tau_p - tau,
'tau_sigma_m': tau - tau_m
}




tau_sigma_p = np.array([ 0.04, 0.08, 0.1 ])
tau_sigma_m = np.array([ 0.04, 0.09, 0.11 ])
data_optical_depth_Boera_2019 = {
'name': 'Boera et al. (2019)',
'z': np.array([ 4.2, 4.6, 5.0 ]) ,
'tau': np.array([ 1.02, 1.41, 1.69 ]) ,
'tau_sigma_p': tau_sigma_p ,
'tau_sigma_m': tau_sigma_m ,
'tau_sigma': ( tau_sigma_p + tau_sigma_m ) / 2.0
}


data_becker = np.array( [[2.15,  0.8806 , 0.0103],
[2.25,  0.8590 , 0.0098],
[2.35,  0.8304 , 0.0093],
[2.45,  0.7968 , 0.0089],
[2.55,  0.7810 , 0.0090],
[2.65,  0.7545 , 0.0088],
[2.75,  0.7371 , 0.0088],
[2.85,  0.7167 , 0.0086],
[2.95,  0.6966 , 0.0084],
[3.05,  0.6670 , 0.0082],
[3.15,  0.6385 , 0.0080],
[3.25,  0.6031 , 0.0079],
[3.35,  0.5762 , 0.0074],
[3.45,  0.5548 , 0.0071],
[3.55,  0.5325 , 0.0071],
[3.65,  0.4992 , 0.0069],
[3.75,  0.4723 , 0.0068],
[3.85,  0.4470 , 0.0072],
[3.95,  0.4255 , 0.0071],
[4.05,  0.4030 , 0.0071],
[4.15,  0.3744 , 0.0074],
[4.25,  0.3593 , 0.0075],
[4.35,  0.3441 , 0.0102],
[4.45,  0.3216 , 0.0094],
[4.55,  0.3009 , 0.0104],
[4.65,  0.2881 , 0.0117],
[4.75,  0.2419 , 0.0201],
[4.85,  0.2225 , 0.0151]]).T
z = data_becker[0]
F = data_becker[1]
tau = -np.log(data_becker[1])
tau_error = 1/F * data_becker[2] 
data_optical_depth_Becker_2013 = {
'name': 'Becker et al. (2013)',
'z': z,
'tau': tau,
'tau_sigma': tau_error,
'tau_sigma_p': tau_error,
'tau_sigma_m': tau_error
}


def Compute_analytical_TauEff_Becker( z ):
  z_0   = 3.5 
  tau_0 = 0.751
  C     = -0.132
  beta  = 2.9
  tau = tau_0 * ( (1 + z) / (1+ z_0) )**beta + C  
  return tau


data_bosman = np.array([
[5.0, 0.135, 0.012 ],
[5.2, 0.114, 0.006 ],
[5.4, 0.084, 0.005 ],
[5.6, 0.050, 0.005 ],
[5.8, 0.023, 0.004 ],
[6.0, 0.0072, 0.0018 ]]).T 
z = data_bosman[0]
F = data_bosman[1]
tau = -np.log(data_bosman[1])
tau_error = 1/F * data_bosman[2] 
data_optical_depth_Bosman_2018 = {
'name':'Bosman et al. (2018)',
'z': z,
'tau': tau,
'tau_sigma': tau_error,
'tau_sigma_p': tau_error,
'tau_sigma_m': tau_error
}

from mean_transmitted_flux import data_mean_flux_bosman_2020
z = data_mean_flux_bosman_2020['z']
F_mean = data_mean_flux_bosman_2020['F_mean']
sigma_F_mean = data_mean_flux_bosman_2020['sigma_F_mean']
tau = -np.log( F_mean )
sigma_tau = 1/F_mean*sigma_F_mean
data_optical_depth_Bosman_2020 = {'name':'Bosman et al. (2020)', 'z':z, 'tau':tau, 'tau_sigma':sigma_tau  }


from mean_transmitted_flux import data_mean_flux_bosman_2021
z = data_mean_flux_bosman_2021['z']
F_mean = data_mean_flux_bosman_2021['F_mean']
sigma_F_mean = data_mean_flux_bosman_2021['sigma_F_mean']
tau = -np.log( F_mean )
sigma_tau = 1/F_mean*sigma_F_mean
data_optical_depth_Bosman_2021 = {'name':'Bosman et al. (from SAZERAC)', 'z':z, 'tau':tau, 'tau_sigma':sigma_tau  }


# data_yang = np.array([
# [ 5.355, 2.885, 2.947, 2.801 ],
# [ 5.506, 3.682, 3.755, 3.611 ],
# [ 5.665, 4.217, 4.271, 4.157 ], 
# [ 5.823, 5.091, 5.166, 5.022 ],
# [ 5.994, 6.316, 6.484, 6.137 ] ]).T
data_yang = np.array([
[ 5.36, 2.84, 0.07 ],
[ 5.51, 3.64, 0.06 ],
[ 5.67, 4.17, 0.05 ], 
[ 5.83, 5.05, 0.06 ],
[ 6.00, 6.27, 0.16 ] ]).T
z = data_yang[0]
tau = data_yang[1]
sigma_tau = data_yang[2]
data_optical_depth_Yang_2020 = {'name':'Yang et al. (2020a)', 'z':z, 'tau':tau, 'tau_sigma':sigma_tau  }


data_optical_depth_Gaikward_2020 = np.array([
    [ 2.0,  0.8690, 0.0214],
    [ 2.2,  0.8261, 0.0206],
    [ 2.4,  0.7919, 0.0210],
    [ 2.6,  0.7665, 0.0216],
    [ 2.8,  0.7398, 0.0212],
    [ 3.0,  0.7105, 0.0213],
    [ 3.2,  0.6731, 0.0223],
    [ 3.4,  0.5927, 0.0247],
    [ 3.6,  0.5320, 0.0280],
    [ 3.8,  0.4695, 0.0278] ])
    
data_eiliers_2018 = np.array( [
[ 4.0	 ,  0.4046	, 0.0151	, 0.9049	, 0.0372	],
[ 4.25 ,	0.3595	, 0.0112	, 1.0230	, 0.0311	],
[ 4.5	 ,  0.2927	, 0.0190	, 1.2286	, 0.0651	],
[ 4.75 ,	0.1944	, 0.0150	, 1.6381	, 0.0770	],
[ 5.0	 ,  0.1247	, 0.0132	, 2.0818	, 0.1060	],
[ 5.25 ,	0.0795	, 0.0078	, 2.5321	, 0.0984	],
[ 5.5	 ,  0.0531	, 0.0058	, 2.9357	, 0.1090	],
[ 5.75 ,	0.0182	, 0.0045	, 4.0057	, 0.2469	],
[ 6.0	 ,  0.0052	, 0.0043	, 4.7595	, 0	],
[ 6.25 ,	-0.0025	, 0.0007	, 6.5843	, 0	] ]).T
z = data_eiliers_2018[0][:-2]
F_mean = data_eiliers_2018[1][:-2]
sigma_F_mean = data_eiliers_2018[2][:-2]    
tau =  data_eiliers_2018[3][:-2]
sigma_tau = data_eiliers_2018[4][:-2]
z_lower = data_eiliers_2018[0][-2:]
tau_lower = data_eiliers_2018[3][-2:]
data_optical_depth_Eilers_2018 = {'name':'Eilers et al. (2018)', 'z':z, 'tau':tau, 'tau_sigma':sigma_tau  }
data_optical_depth_Eilers_2018['lower_limits'] = { 'z':z_lower, 'tau':tau_lower }


data_Fan = np.array([
[ 4.90, 5.15, 2.1, 0.3, 0  ], 
[ 5.15, 5.35, 2.5, 0.5, 0  ], 
[ 5.35, 5.55, 2.6, 0.6, 0  ],
[ 5.55, 5.75, 3.2, 0.8, 0  ],
[ 5.75, 5.95, 4.0, 0.8, -1  ],
[ 5.95, 6.25, 7.1, 2.1, -1  ]]).T
z = 0.5 * ( data_Fan[0] + data_Fan[1] )
tau = data_Fan[2]
sigma_tau = data_Fan[3]
type = data_Fan[4]
indices_data = np.where( type == 0 )
indices_lower = np.where( type == -1 )
data_optical_depth_Fan_2006 = {'name': 'Fan et al. (2006)', 'z':z[indices_data], 'tau':tau[indices_data], 'tau_sigma':sigma_tau[indices_data] } 
data_optical_depth_Fan_2006['lower_limits'] = { 'z':z[indices_lower], 'tau':tau[indices_lower], 'tau_sigma':sigma_tau[indices_lower] }