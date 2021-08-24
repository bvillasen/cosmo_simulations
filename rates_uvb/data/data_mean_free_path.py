import os, sys
import numpy as np

root_dir = os.path.dirname(os.getcwd()) + '/'

data = np.loadtxt( root_dir + 'rates_uvb/data/mean_free_path_P19.txt').T 
data_lambda_P19 = { 'z':data[0], 'lambda':data[1], 'name':'Puchwein et al. 2019' }


data = np.array( [ [ 5.1, 9.09, 1.28, 1.60 ],
                   [ 6.0, 0.75, 0.65, 0.45] ]).T
data_lambda_Becker_2021 = { 'z':data[0], 'lambda':data[1],  'delta_h':data[2],  'delta_l':data[3], 'name':'Becker et al. 2021'  }
                   
      
