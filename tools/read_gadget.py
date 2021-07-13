''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
'''
...................Functions for Reading Gadget Files..................
'''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


import numpy as np
import matplotlib.pyplot as plt
import struct
import os
import pandas as pd

########################################################################
########################################################################
########################################################################
#Read Header
########################################################################
########################################################################
########################################################################

def loadgadget_header(filename):

    #Open file
    if os.path.exists(filename):
        f = open(filename,'rb')
    else:
        f = open(filename+'.0','rb')

    #Read header
    myheader = f.read(256+4)
    N_arr = np.array(struct.unpack('i'*6,myheader[4:28]))
    m_arr =  np.array(struct.unpack('d'*6,myheader[28:76]))
    time = struct.unpack('d',myheader[76:84])[0]
    redshift = struct.unpack('d',myheader[84:92])[0]
    N_all = np.array(struct.unpack('i'*6,myheader[100:124]))
    Numfiles = struct.unpack('i',myheader[128:132])[0]
    Boxsize = struct.unpack('d',myheader[132:140])[0]
    Omega0 = struct.unpack('d',myheader[140:148])[0]
    OmegaLam = struct.unpack('d',myheader[148:156])[0]
    H0 = struct.unpack('d',myheader[156:164])[0]
    f.close()

    #Create header output
    labels = ['N','m','time','redshift','boxsize']
    header = pd.DataFrame(np.zeros([1,np.size(labels)]), columns=labels)
    header['N'] = N_arr[1]
    header['m'] = m_arr[1]
    header['time'] = time
    header['redshift'] = redshift
    header['boxsize'] = Boxsize

    return header, Numfiles



def loadgadget(filename,longIDs=False):
    '''
    Load gadget file
    ---------
    filename: base of filename (if split into multiple files, leave off '.x')
    longIDs: if IDs are stored as 64 bit integers, have to turn this on
    ---------
    header: pandas object with snapshot info
    data: Nx7 array with ID, x, y, z, vx, vy, vz
    '''

    header, Numfiles = loadgadget_header(filename)
    data = np.array([])

    print('Reading ' + str(Numfiles)+ ' files:')
    for i in range(Numfiles):

        #Open file
        if Numfiles>1:
            myfilename=filename+'.'+str(i)
        else:
            myfilename=filename
        f = open(myfilename,'rb')

        #Read header
        myheader = f.read(256+4)
        N_arr = np.array(struct.unpack('i'*6,myheader[4:28]))
        f.read(8)
        if i!=0:
            header['N'] = header['N']+ N_arr[1]

        #Set up mydata
        mydata = np.zeros([N_arr[1],7])

        #Read positions
        temp = f.read(4*3*N_arr[1])
        temp = np.ndarray((1, 3*N_arr[1]), 'f', temp)[0]
        mydata[:,1:4] = np.reshape(temp,(N_arr[1],3))
        f.read(8)

        #Read velocities
        temp = f.read(4*3*N_arr[1])
        temp = np.ndarray((1, 3*N_arr[1]), 'f', temp)[0]
        mydata[:,4:7] = np.reshape(temp,(N_arr[1],3))
        f.read(8)

        #Read IDs
        if longIDs:
            temp = f.read(8*N_arr[1])
            temp = np.ndarray((1, N_arr[1]), 'l', temp)[0]
        else:
            temp = f.read(4*N_arr[1])
            temp = np.ndarray((1, N_arr[1]), 'i', temp)[0]
        mydata[:,0] = temp

        f.close()

        if data.shape[0]==0:
            data = mydata.copy()
        else:
            data = np.vstack([data,mydata])


    return header, data


def loadgadget_pos(filename):
    '''
    Load gadget file
    ---------
    filename: base of filename (if split into multiple files, leave off '.x')
    ---------
    header: pandas object with snapshot info
    data: Nx3 array x, y, z
    '''

    header, Numfiles = loadgadget_header(filename)
    data = np.array([])

    print('Reading ' + str(Numfiles)+ ' files:')
    for i in range(Numfiles):

        #Open file
        if Numfiles>1:
            myfilename=filename+'.'+str(i)
        else:
            myfilename=filename
        f = open(myfilename,'rb')
        print(myfilename)

        #Read header
        myheader = f.read(256+4)
        N_arr = np.array(struct.unpack('i'*6,myheader[4:28]))
        f.read(8)
        if i!=0:
            header['N'] = header['N']+ N_arr[1]

        #Read positions
        temp = f.read(8*3*N_arr[1])
        temp = np.ndarray((1, 3*N_arr[1]), 'f', temp)[0]
        mydata = np.reshape(temp,(N_arr[1],3))
        f.close()

        if data.shape[0]==0:
            data = mydata.copy()
        else:
            data = np.vstack([data,mydata])

    return header, data