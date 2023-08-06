#! C:\Python27
import numpy as np 
import pandas as pd 
from get_curvature2 import *
from get_shape import *
from scipy.io import loadmat
import os
import time

def get_bdprops_v3b(Bd = None):
    np.set_printoptions(precision=5,suppress=True)
    pnum = len(Bd)

    out_rph = np.zeros((pnum,38))
    out_cva = np.zeros((pnum,38))
    Bd = Bd[0] #for pickle input, not for cbdt
    for k in range(pnum):
        if (k % 20 == 0 or k == pnum-1): print str(k+1) + ' / ' + str(pnum)
        B=Bd[k]
        pn = len(B.T[0])
        if pn > 50:
            dist = np.power((B.T[0]-np.mean(B.T[0])),2) + np.power((B.T[1]-np.mean(B.T[1])),2)
            dist = np.sqrt(dist)
            cva = get_curvature2(B)
            rph = get_shape(dist)
            cvap= get_shape(cva.T[0])
            out_rph[k]=rph
            out_cva[k]=cvap
        else:
            out_rph[k]=np.zeros(38)
            out_cva[k]=np.zeros(38)
    return out_rph, out_cva

def get_bdprops(direc,bd,operators):
    start = time.time()

    # mat=loadmat('cbdt')
    # mdata=mat['cbdt']
    # cbdt = pd.DataFrame(mdata)[0]

    out_rph, out_cva = get_bdprops_v3b(bd)

    df1 = pd.DataFrame(out_rph,columns=operators)
    df2 = pd.DataFrame(out_cva,columns=operators)

    # if not os.path.exists(direc + 'rph.pickle'):
    #     df1.to_pickle(direc + 'rph.pickle')
    if not os.path.exists(direc + 'rph.csv'):
        df1.to_csv(direc + 'rph.csv', index = False)
    # if not os.path.exists(direc + 'cva.pickle'):
    #     df2.to_pickle(direc + 'cva.pickle')
    if not os.path.exists(direc + 'cva.csv'):
        df2.to_csv(direc + 'cva.csv', index = False)


    end = time.time()
    print 'elapsed time is ' + str(end-start) + 'seconds for get_bdprops'
    return df1,df2