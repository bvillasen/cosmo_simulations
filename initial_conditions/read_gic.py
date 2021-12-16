import numpy as np


def ReadFileHeader(f,loud=1):  
    h = np.fromfile(f,dtype=np.int32,count=1); assert(h[0] == 260)
    b = np.fromfile(f,dtype=np.byte,count=256)
    b = np.fromfile(f,dtype=np.int32,count=1)
    if(loud): print("File version: %d"%b[0])
    h = np.fromfile(f,dtype=np.int32,count=1); assert(h[0] == 260)
    h = np.fromfile(f,dtype=np.int32,count=1); assert(h[0] == 4*122)
    b = np.fromfile(f,dtype=np.float32,count=12)
    fh = {
        "OmegaB":b[0],
        "OmegaD":b[1],
        "OmegaL":b[2],
        "OmegaN":b[3],
        "h100":b[4],
        "ns":b[5],
        "sigma8":b[6],
        "kpivot":b[7],
        "abeg":b[8],
        "dx":b[9],
        "delDC":b[10],
        "rmsDC":b[11]
        }
    b = np.fromfile(f,dtype=np.int32,count=6)
    fh["nx"] = b[0]
    fh["ny"] = b[1]
    fh["nz"] = b[2]
    fh["seed"] = b[3]
    fh["seed2"] = b[4]
    fh["nrec"] = b[5]
    b = np.fromfile(f,dtype=np.int64,count=1)
    fh["ntot"] = b[0]
    b = np.fromfile(f,dtype=np.int32,count=2)
    fh["lmax"] = b[0]
    fh["iflag"] = b[1]
    b = np.fromfile(f,dtype=np.float32,count=100)
    h = np.fromfile(f,dtype=np.int32,count=1); assert(h[0] == 4*122)
    if(loud): print(fh)
    return fh
##


def ReadLevelHeader(f,loud=1):  
    h = np.fromfile(f,dtype=np.int32,count=1); assert(h[0] == 24)
    b = np.fromfile(f,dtype=np.int32,count=2)
    lh = {
        "l":b[0],
        "lmax":b[1]
        }
    b = np.fromfile(f,dtype=np.int64,count=1)
    lh["nlev"] = b[0]
    b = np.fromfile(f,dtype=np.float32,count=1)
    lh["Mlev"] = b[0]
    b = np.fromfile(f,dtype=np.int32,count=1)
    lh["ind"] = b[0]
    h = np.fromfile(f,dtype=np.int32,count=1); assert(h[0] == 24)
    if(loud): print(lh)
    return lh
##


def ReadRecord(f,dtype,nrec):
    h = np.fromfile(f,dtype=np.int32,count=1); assert(h[0] == 4*nrec)
    b = np.fromfile(f,dtype=dtype,count=nrec)
    h = np.fromfile(f,dtype=np.int32,count=1); assert(h[0] == 4*nrec)
    return b
##


#
#  Array is saved hierarchically, repack it to a flat array
#
def RepackArray(arr,fh):
    nref = 2**fh["lmax"]
    arr = arr.reshape((fh["nz"],fh["ny"],fh["nx"]*nref**3))
    arr1 = np.empty((fh["nz"]*nref,fh["ny"]*nref,fh["nx"]*nref),dtype=np.float32)
    for k in range(nref):
        for j in range(nref):
            for i in range(nref):
                arr1[k::nref,j::nref,i::nref] = arr[:,:,i+nref*(j+nref*k)::nref**3]
            ##
        ##
    ##
    return arr1

    
def ReadArray(f,fh,ntot,ind,loud=0):
    nread = 0
    arr = np.empty((ntot,),dtype=np.float32)
    while(nread < ntot):
        b = ReadRecord(f,np.float32,fh['nrec'])
        if(ind):
            ReadRecord(f,np.int32,fh['nrec'])
            ReadRecord(f,np.int32,fh['nrec'])
            ReadRecord(f,np.int32,fh['nrec'])
        ##
        nmax = fh['nrec']
        if(nread+nmax > ntot): nmax = ntot - nread
        arr[nread:nread+nmax] = b[0:nmax]
        if(loud):
            p0 = (100*nread)//ntot
        ##
        nread += fh['nrec']
        if(loud):
            p1 = (100*nread)//ntot
            if(p1 > p0): print("reading... %d%% done"%p0,end="\r")
        ##
    ##
    if(loud): print("                               ",end="\r")    
    return arr
##

            
def ReadDen(fname,loud=1):
    with open(fname,'rb') as f:
        fh = ReadFileHeader(f,loud=loud)
        nlow = fh["nx"]*fh["ny"]*fh["nz"]
        if(fh["lmax"] > 0):
            h = np.fromfile(f,dtype=np.int32,count=1); assert(h[0] == 12)
            b = np.fromfile(f,dtype=np.int32,count=3)
            h = np.fromfile(f,dtype=np.int32,count=1); assert(h[0] == 12)
            ReadArray(f,fh,nlow,0)

            for l in range(fh["lmax"]+1):
                lh = ReadLevelHeader(f,loud=loud); assert(lh["l"]==l and lh["lmax"]==fh["lmax"])
            ##
            d = ReadArray(f,fh,fh["ntot"],1,loud=loud)
            return RepackArray(d,fh)
        else:
            return None
        ##
    ##
##


def ReadXV(fname,loud=1):
    with open(fname,'rb') as f:
        fh = ReadFileHeader(f,loud=loud)
        nlow = fh["nx"]*fh["ny"]*fh["nz"]
        if(fh["lmax"] > 0):
            h = np.fromfile(f,dtype=np.int32,count=1); assert(h[0] == 12)
            b = np.fromfile(f,dtype=np.int32,count=3)
            h = np.fromfile(f,dtype=np.int32,count=1); assert(h[0] == 12)
            ReadArray(f,fh,nlow,0)

            for l in range(fh["lmax"]+1):
                lh = ReadLevelHeader(f,loud=loud); assert(lh["l"]==l and lh["lmax"]==fh["lmax"])
            ##
            x = ReadArray(f,fh,fh["ntot"],0,loud=loud)
            y = ReadArray(f,fh,fh["ntot"],0,loud=loud)
            z = ReadArray(f,fh,fh["ntot"],0,loud=loud)
            return fh, (RepackArray(x,fh),RepackArray(y,fh),RepackArray(z,fh))
        else:
            return None
        ##
    ##
##
# 
# path = "/data/gnedin/REI/D/IC/P2"
# 
# d = ReadDen(path+"/rei20A_mr1_B.den")
# (x,y,z) = ReadXV(path+"/rei20A_mr1_D.pos")
# 
# import matplotlib.pyplot as plt
# 
# fig = plt.figure(figsize=(8,4))
# 
# ax1 = fig.add_subplot(1,2,1)
# ax2 = fig.add_subplot(1,2,2)
# 
# ax1.imshow(d[0,:,:],origin="lower")
# ax2.scatter(x[0],y[0],s=1)
# 
# 
# plt.show()

    
