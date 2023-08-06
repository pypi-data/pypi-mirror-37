# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 09:59:42 2018

@author: yili.peng
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.linalg import inv

def permutation(n):
    main_list=[np.concatenate([[k%2]*int((2**n)/(2**i)) for k in range(2**i)]) for i in range(1,n+1)]
    return np.array(main_list).T*2-1

def Sig(n):
    '''
    Sigma Matrix
    '''
    a=permutation(n)
    sub = a @ a.T
    add = n
    F=(add+sub)/2
    D=(add-sub)/2
    return ((2/15)**F)*((1/30)**D)

fh = lambda x,j: (x-1)*(3*x-1) if j==1 else x*(2-3*x)

def Tpn(rank_df):
    '''
    t stats
    '''
    n,p=rank_df.shape
    T_per=permutation(p)
    pos1=fh(rank_df.div(n+1),1)
    neg1=fh(rank_df.div(n+1),-1)
    TNP2=[pd.DataFrame(np.where(np.array(i)==1,pos1,neg1),columns=rank_df.columns,index=rank_df.index).prod(axis=1).mean() for i in T_per]
    return np.array(TNP2)

def Independence_test(df):
    '''
    copula test of independence of serveral time series
    H0: those timeseries are independent
    return stats and p-value
    
    df: dataframe of (n*p) time series dataframe
    '''
    rank_df=df.rank()
    n,p=rank_df.shape
    T=Tpn(rank_df).reshape([-1,1])
    S_inv=inv(Sig(p))
    T_stats=(T.T@S_inv@T)[0][0]*n
    p_value=1-stats.chi2.cdf(T_stats, p**2)
    return T_stats,p_value