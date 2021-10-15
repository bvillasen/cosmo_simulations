import numpy as np

data_becker_bolton = np.array( [[ 2.40, 1.03796, 1.40337, 0.74260 ], 
                            [ 2.80, 0.85557, 1.15677, 0.63766 ],
                            [ 3.20, 0.78716, 1.07247, 0.60034 ],
                            [ 3.60, 0.80015, 1.08738, 0.61337 ],
                            [ 4.00, 0.85382, 1.16328, 0.65118 ],
                            [ 4.40, 0.95888, 1.33683, 0.72756 ],
                            [ 4.75, 0.94755, 1.34488, 0.67103 ]])



data_photoionization_HI_becker_bolton_2013 = {
'z': data_becker_bolton[:,0],
'mean': data_becker_bolton[:,1],
'high': data_becker_bolton[:,2],
'low': data_becker_bolton[:,3],
'name':'Becker & Bolton (2013)'
}

# data_dalosio = np.array( [
# [ 4.8, 0.60279, 0.68148 ,0.40148 ],
# [ 5.0, 0.55432, 0.65451 ,0.35349 ],
# [ 5.2, 0.51367, 0.62539 ,0.32341 ],
# [ 5.4, 0.50352, 0.63539 ,0.31220 ],
# [ 5.6, 0.48236, 0.63571 ,0.36320 ],
# [ 5.8, 0.29094, 0.40664 ,0.17139 ] ])
# 
# data_photoionization_HI_dalosio_2018 = {
# 'z': data_dalosio[:,0],
# 'mean': data_dalosio[:,1],
# 'high': data_dalosio[:,2],
# 'low': data_dalosio[:,3],
# 'name':"D'Aloisio et al. 2018"
# }


data_dalosio = np.array( [
[ 4.8, 0.60, 0.08 ,0.20 ],
[ 5.0, 0.55, 0.10 ,0.20 ],
[ 5.2, 0.51, 0.11 ,0.19 ],
[ 5.4, 0.50, 0.13 ,0.19 ],
[ 5.6, 0.48, 0.15 ,0.19 ],
[ 5.8, 0.29, 0.11 ,0.12 ] ])

data_photoionization_HI_dalosio_2018 = {
'z': data_dalosio[:,0],
'mean': data_dalosio[:,1],
'high': data_dalosio[:,1] + data_dalosio[:,2],
'low': data_dalosio[:,1] - data_dalosio[:,3],
'name':"D'Aloisio et al. (2018)"
}

data_gallego = np.array([
[ 3.1, 0.82, 0.53 ],
[ 3.9, 1.12, 0.53 ],
[ 4.9, 0.85, 0.53 ] ]) 


data_photoionization_HI_gallego_2021 = {
'z': data_gallego[:,0],
'mean': data_gallego[:,1],
'high': data_gallego[:,1] + data_gallego[:,2],
'low':  data_gallego[:,1] - data_gallego[:,2],
'name':"Gallego et al. (2021)"
}

# data_calverley = np.array([ 
# [ 4.99651, 0.710290, 1.02897, 0.50044 ],
# [ 5.99969, 0.145607, 0.22143, 0.09645 ] ])
# data_photoionization_HI_calverley_2011 = {
# 'z': data_calverley[:,0]+0.02,
# 'mean': data_calverley[:,1],
# 'high': data_calverley[:,2],
# 'low': data_calverley[:,3],
# 'name':"Calverley et al. 2011"
# } 

data_calverley = np.array([ 
[ 5, -12.15, 0.16 ],
[ 6, -12.84, 0.18  ] ])
 
data_photoionization_HI_calverley_2011 = {
'z': data_calverley[:,0]+0.02,
'mean': 10**data_calverley[:,1] *1e12,
'high': 10**(data_calverley[:,1] + data_calverley[:,2]) *1e12 ,
'low': 10**(data_calverley[:,1] - data_calverley[:,2]) *1e12,
'name':"Calverley et al. (2011)"
} 


data_wyithe = np.array([
[ 4.99684, 0.47429, 0.78076, 0.27098 ],
[ 5.99702, 0.18094, 0.36451, 0.09051 ] ])


data_photoionization_HI_wyithe_2011 = {
'z': data_wyithe[:,0] + 0.04,
'mean': data_wyithe[:,1],
'high': data_wyithe[:,2],
'low': data_wyithe[:,3],
'name':"Wyithe et al. (2011)"
} 

# data_gaikwad = np.array([
# [ 0.0992, 0.06607, 0.06038, 0.0721 ],  
# [ 0.2014, 0.10401, 0.09616, 0.1128 ],  
# [ 0.2999, 0.13673, 0.12228, 0.1529 ],  
# [ 0.3985, 0.20001, 0.17503, 0.2255 ] ])
# 
# data_photoionization_HI_gaikwad_2017 = {
# 'z': data_gaikwad[:,0] ,
# 'mean': data_gaikwad[:,1],
# 'high': data_gaikwad[:,3],
# 'low': data_gaikwad[:,2],
# 'name':"Gaikwad et al. 2017"
# } 
data_gaikwad = np.array([
[ 0.1, 0.066, 0.015 ],  
[ 0.2, 0.100, 0.021 ],  
[ 0.3, 0.145, 0.037 ],  
[ 0.4, 0.210, 0.052 ] ])

data_photoionization_HI_gaikwad_2017 = {
'z': data_gaikwad[:,0] ,
'mean': data_gaikwad[:,1],
'high': data_gaikwad[:,1] + data_gaikwad[:,2],
'low': data_gaikwad[:,1] - data_gaikwad[:,2],
'name':"Gaikwad et al. (2017)"
}