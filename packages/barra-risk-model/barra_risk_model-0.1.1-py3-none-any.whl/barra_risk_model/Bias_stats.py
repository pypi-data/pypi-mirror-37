# -*- coding: utf-8 -*-
"""
Created on Thu May 31 17:56:45 2018

@author: yili.peng
"""

import pandas as pd
import numpy as np
import warnings

def portfolio_std(w,F,S,X):
    '''
    compute portfolio standardized deviation as D = w'X*F*X'w + w'diag(S^2)*w
    
    w: weight, series
    F: predicted factor covariance matrix, dataframe
    S: predicted specific std, series
    X: realistic factor exposure, dataframe
    '''
    if F.isna().any().any():
        warnings.warn('Na exists in F, portfolio std computation failed')
        return np.nan
    
    X_tmp=X[F.columns]
    W_tmp=w.reindex(X_tmp.index).fillna(0)
    S_tmp=S.reindex(X_tmp.index).fillna(0)
    
    x_tmp=X_tmp.values
    f_tmp=F.values    
    s_tmp=S_tmp.values
    w_tmp=(W_tmp.values/W_tmp.sum()).reshape(-1,1)
    
    A=w_tmp.T @ x_tmp
    D=A @ f_tmp @ A.T + w_tmp.T @ np.diag(s_tmp)**2 @ w_tmp
    return D[0][0]**0.5

def portfolio_std_F(w,F,X):
    '''
    compute portfolio standardized deviation with only factor covariance matrix as D = w'X*F*X'w
    
    w: weight, series
    F: predicted factor covariance matrix, dataframe
    X: realistic factor exposure, dataframe
    '''        
    
    if F.isna().any().any():
        warnings.warn('Na exists in F, portfolio std computation failed')
        return np.nan
    X_tmp=X[F.columns]
    W_tmp=w.reindex(X_tmp.index).fillna(0)
    
    x_tmp=X_tmp.values
    w_tmp=(W_tmp.values/W_tmp.sum()).reshape(-1,1) 
    f_tmp=F.values
    
    A=w_tmp.T @ x_tmp
    D=A @ f_tmp @ A.T
    return D[0][0]**0.5
def portfolio_r(w,R):
    '''
    comput portfolio (daily) return as Pr = w'R
    
    w: stock weight, series
    R: stock return, series
    '''
    W_tmp=w.reindex(R.index).fillna(0)
    W_tmp=W_tmp/W_tmp.sum()
    return (R*W_tmp).sum()

def bs_std(R_d,S_m,times=21):
    '''
    R_d: daily portfolio return series
    S_m: monthly portfolio std series
    times: month/day
    '''
    b=R_d/S_m*np.sqrt(times)
    bs_tmp=b.std()
    return bs_tmp


def bs(R_all,F_all,X_all,S_all,W=None): 
    '''
    calculate bias stats w/ specific std
    R_all: Stock return df
    F_all: Factor matrix dict
    X_all: Factor exposure dict
    S_all: Specific std df
    W: weight. df/series/None(random). df=(date*stocks,weight) series=(stocks,weight).
    '''
    S=pd.Series()
    R=pd.Series()
    if (len(R_all)==0) or (len(F_all)==0) or (len(X_all)==0) or (len(S_all)==0):
        print('bias stats require effecient R_all, F_all, X_all, S_all')
        return pd.Series()
    if W is None:
        w=pd.Series(np.random.randint(low=0,high=1000,size=len(R_all.columns)),index=R_all.columns)
    elif type(W) is pd.Series:
        w=W
    elif type(W) is not pd.DataFrame:
        print('bias stats require effecient W')
        return pd.Series()
    cross_dt=list(set(R_all.index)&set(F_all.keys())&set(X_all.keys())&set(S_all.index))
    cross_dt.sort()
    for j in range(0,len(cross_dt),21):
        dt0=cross_dt[j]
        F_tmp=F_all[dt0]
        X_tmp=X_all[dt0]
        R_tmp=R_all.loc[dt0]
        S_tmp=S_all.loc[dt0]
        if F_tmp.isnull().any().any() or X_tmp.isnull().any().any():
            continue
        if type(W) is pd.DataFrame:
            if np.all(np.array(W.index)<dt0) or np.all(np.array(W.index)>dt0):
                continue
            else:
                dt0=np.max(np.array(W.index)[np.where(np.array(W.index)<=dt0)])
                w=W.loc[dt0]
        s_tmp=portfolio_std(w,F_tmp,S_tmp,X_tmp)
        R_tmp2=pd.Series()
        S_tmp2=pd.Series()
        for k in range(21):
            if (j+k)>=len(cross_dt):
                continue
            dt=cross_dt[j+k]
            S_tmp2.at[dt]=s_tmp
            R_tmp=R_all.loc[dt]
            r_tmp=portfolio_r(w,R_tmp)
            R_tmp2.at[dt]=r_tmp
        R=R.append(R_tmp2.sub(R_tmp2.mean()))
        S=S.append(S_tmp2)
    return bs_std(R,S)

def bs_window(R_all,F_all,X_all,S_all,W=None):
    cross_dt=list(set(R_all.index)&set(F_all.keys())&set(X_all.keys())&set(S_all.index))
    cross_dt.sort()
    inx=(pd.Series(cross_dt)//100).rolling(2).agg(lambda x: x.iloc[1]-x.iloc[0]).fillna(1)
    inx_lst=list(inx.index[inx==1])
    if len(inx_lst)< 12:
        print('short history')
        return None
    else:
        bs_window=pd.Series()
        for i in range(12,len(inx_lst)):
            R_all_tmp=R_all.iloc[inx_lst[i-12]:inx_lst[i]]
            F_all_tmp={dt:F_all[dt] for dt in cross_dt[inx_lst[i-12]:inx_lst[i]]}
            X_all_tmp={dt:X_all[dt] for dt in cross_dt[inx_lst[i-12]:inx_lst[i]]}
            S_all_tmp=S_all.iloc[inx_lst[i-12]:inx_lst[i]]
            bs_window.at[cross_dt[inx_lst[i]]]=bs(R_all_tmp,F_all_tmp,X_all_tmp,S_all_tmp,W=W)
        return bs_window


def bs_F(R_all,F_all,X_all,W=None): 
    '''
    R_all: Stock return df
    F_all: Factor matrix dict
    X_all: Factor exposure dict
    W: weight. df/series/None(random). df=(date*stocks,weight) series=(stocks,weight).
    '''
    S=pd.Series()
    R=pd.Series()
    if (len(R_all)==0) or (len(F_all)==0) or (len(X_all)==0):
        print('bias stats require effecient R_all, F_all, X_all')
        return pd.Series()
    if W is None:
        w=pd.Series(np.random.randint(low=0,high=1000,size=len(R_all.columns)),index=R_all.columns)
    elif type(W) is pd.Series:
        w=W
    elif type(W) is not pd.DataFrame:
        print('bias stats require effecient W')
        return pd.Series()
    cross_dt=list(set(R_all.index)&set(F_all.keys())&set(X_all.keys()))
    cross_dt.sort()
    for j in range(0,len(cross_dt),21):
        dt0=cross_dt[j]
        F_tmp=F_all[dt0]
        X_tmp=X_all[dt0]
        R_tmp=R_all.loc[dt0]
        if F_tmp.isnull().any().any() or X_tmp.isnull().any().any():
            continue
        if type(W) is pd.DataFrame:
            if np.all(np.array(W.index)<dt0) or np.all(np.array(W.index)>dt0):
                continue
            else:
                dt0=np.max(np.array(W.index)[np.where(np.array(W.index)<=dt0)])
                w=W.loc[dt0]
        s_tmp=portfolio_std_F(w,F_tmp,X_tmp)
        R_tmp2=pd.Series()
        S_tmp2=pd.Series()
        for k in range(21):
            if (j+k)>=len(cross_dt):
                continue
            dt=cross_dt[j+k]
            S_tmp2.at[dt]=s_tmp
            R_tmp=R_all.loc[dt]
            r_tmp=portfolio_r(w,R_tmp)
            R_tmp2.at[dt]=r_tmp
        R=R.append(R_tmp2.sub(R_tmp2.mean()))
        S=S.append(S_tmp2)
    return bs_std(R,S)

def bs_f_window(R_all,F_all,X_all,W=None):
    cross_dt=list(set(R_all.index)&set(F_all.keys())&set(X_all.keys()))
    cross_dt.sort()
    inx=(pd.Series(cross_dt)//100).rolling(2).agg(lambda x: x.iloc[1]-x.iloc[0]).fillna(1)
    inx_lst=list(inx.index[inx==1])
    if len(inx_lst)< 12:
        print('short history')
        return None
    else:
        bs_window=pd.Series()
        for i in range(12,len(inx_lst)):
            R_all_tmp=R_all.iloc[inx_lst[i-12]:inx_lst[i]]
            F_all_tmp={dt:F_all[dt] for dt in cross_dt[inx_lst[i-12]:inx_lst[i]]}
            X_all_tmp={dt:X_all[dt] for dt in cross_dt[inx_lst[i-12]:inx_lst[i]]}
            bs_window.at[cross_dt[inx_lst[i]]]=bs_F(R_all_tmp,F_all_tmp,X_all_tmp,W=W)
        return bs_window

def factor_portfolio_r(w,R):
    '''
    w: weight df
    R: factor return
    '''
    W_tmp=w.reindex(R.index).fillna(0)
    W_tmp2=W_tmp.div(W_tmp.sum())
    return (W_tmp2.mul(R,axis=0)).sum()

def factor_portfolio_std(w,F_cov):
    '''
    w: weight
    F_cov: predicted factor covariance matrix
    '''        
    if F_cov.isnull().any().any():
        return pd.Series(index=w.columns)
    W_tmp=w.reindex(F_cov.index).fillna(0)
    W_tmp2=W_tmp.div(W_tmp.sum())
    V=np.diag(W_tmp2.T.values @ F_cov.values @ W_tmp2.values)
    return pd.Series(V**0.5,index=w.columns)

def real_std(R_all,W=None):
    '''
    real anually volatility
    
    W: weight. df/series/None(random). df=(date*stocks,weight) series=(stocks,weight).
    R_all: daily return of the next month anually
    '''
    if W is None:
        w=pd.Series(np.random.randint(low=0,high=1000,size=len(R_all.columns)),index=R_all.columns)
    elif type(W) is pd.Series:
        w=W
    elif type(W) is not pd.DataFrame:
        print('bias stats require effecient W')
        return pd.Series()
    cross_dt=R_all.index
    if len(cross_dt)<21:
        return pd.Series()
    real_std=pd.Series()
    for j in range(0,len(cross_dt)-21):
        dt0=cross_dt[j]
        if type(W) is pd.DataFrame:
            if np.all(np.array(W.index)<dt0) or np.all(np.array(W.index)>dt0):
                continue
            else:
                dt0=np.max(np.array(W.index)[np.where(np.array(W.index)<=dt0)])
                w=W.loc[dt0]
        R_tmp=R_all.iloc[j:j+21].fillna(0)    
        w_tmp=w.reindex(R_tmp.columns).fillna(0)/w.sum()
        pr=R_tmp.values @ w_tmp.values.reshape(-1,1) 
        real_std.at[dt0]=np.std(pr)
    return real_std.mul(np.sqrt(251))

def predicted_std(F_all,S_all,X_all,W=None):
    '''
    predicted anually volatility
    '''
    if W is None:
        w=pd.Series(np.random.randint(low=0,high=1000,size=len(S_all.columns)),index=S_all.columns)
    elif type(W) is pd.Series:
        w=W
    elif type(W) is not pd.DataFrame:
        print('bias stats require effecient W')
        return pd.Series()
    cross_dt=list(set(F_all.keys())&set(X_all.keys())&set(S_all.index))
    cross_dt.sort()
    predicted_std=pd.Series()
    for j in range(0,len(cross_dt)):
        dt0=cross_dt[j]
        if type(W) is pd.DataFrame:
            if np.all(np.array(W.index)<dt0) or np.all(np.array(W.index)>dt0):
                continue
            else:
                dt0=np.max(np.array(W.index)[np.where(np.array(W.index)<=dt0)])
                w=W.loc[dt0]
        predicted_std.at[dt0]=portfolio_std(w,F_all[dt0],S_all.loc[dt0],X_all[dt0])
    return predicted_std.mul(np.sqrt(12))

