# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 11:16:42 2018

@author: yili.peng
"""
from .Bias_stats import factor_portfolio_r
from .Bias_stats import factor_portfolio_std
import pandas as pd
import numpy as np
import warnings
import time
from scipy import linalg
from RNWS import read

def sigma_range(Fct_return,dt_range=None,var_halflife=84,var_ewm_length=50,var_lags=5,mon=21,**kwargs):
    '''
    forecast factor volatility for n days 
    
    Fct_return: Factor return
    dt_range: date range (must in Fct_return index)
    var_halflife: exponential decay half life
    var_ewm_length: exponential moving window
    var_lag: Newey-West series correlation lag
    mon: n days, typically one month n=21 
    '''
    dt_range=(Fct_return.index if dt_range is None else dt_range)
    
    if len(dt_range)<(var_lags+var_ewm_length):
        warnings.warn('history too short')
        return pd.DataFrame(index=dt_range,columns=Fct_return.columns)
    ewm=[Fct_return.loc[dt_range].shift(i).ewm(var_halflife,min_periods=var_ewm_length) for i in range(var_lags+1)]
    var_sum=(ewm[0].var() + sum([(1-i/(var_lags+1))*2*ewm[i].cov(ewm[0]) for i in range(1,var_lags+1)]))*mon
    return np.sqrt(var_sum)  
 
def rho_range(Fct_return,dt_range=None,cor_halflife=504,cor_ewm_length=50,cor_lags=2,**kwargs): 
    '''
    forecast factor correlation for n days 
    
    Fct_return: Factor return
    dt_range: date range (must in Fct_return index)
    cor_halflife: exponential decay half life
    cor_ewm_length: exponential moving window
    cor_lag: Newey-West series correlation lag
    '''        
    dt_range=(Fct_return.index if dt_range is None else dt_range)
    if len(dt_range)<(cor_lags+cor_ewm_length):
        warnings.warn('history too short')
        return pd.DataFrame(index=pd.MultiIndex.from_product([dt_range,Fct_return.columns]),columns=Fct_return.columns)
    ewm=[Fct_return.loc[dt_range].shift(i).ewm(cor_halflife,min_periods=cor_ewm_length) for i in range(cor_lags+1) ]
    cov_sum=ewm[0].cov(pairwise=True)+sum([(1-i/(cor_lags+1))*(ewm[i].cov(ewm[0],pairwise=True)+ewm[0].cov(ewm[i],pairwise=True)) for i in range(1,cor_lags+1)])
    
    cs=cov_sum.unstack()
    inx=cs.columns
    
    inx2=pd.MultiIndex(levels=inx.levels,labels=[range(Fct_return.shape[1]),range(Fct_return.shape[1])])
    s=np.sqrt(pd.DataFrame(cs[inx2].values,index=cs.index,columns=inx.levels[0]))
    result=cs.div(s,level=1).div(s,level=0).stack(dropna=False)
    return result
def sigma_gen_range(Fct_return,dt_range=None,sigma_gen_halflife=84,sigma_gen_ewm_length=50,**kwargs):
    '''
    generate historical factor volatility at time dt
    
    Fct_return: Factor return
    dt_range: date range (must in Fct_return index)
    sigma_gen_halflife: exponential decay half life
    sigma_gen_ewm_length: exponential moving window
    '''
    if dt_range is None:
        dt_range=Fct_return.index
    if len(dt_range)<(sigma_gen_ewm_length):
        warnings.warn('history too short')
        return pd.DataFrame(index=dt_range,columns=Fct_return.columns)
    sigma_range=Fct_return.loc[dt_range].ewm(halflife=sigma_gen_halflife,min_periods=sigma_gen_ewm_length).std().shift()
    return sigma_range
def vr_adj_range(F,Fct_return,dt_range=None,vra_halflife=42,vra_ewm_length=50,**kwargs):
    '''
    volatility regime risk adjustment for the predicted factor covariance matrix
    
    F: original factor covariance matrix, range
    Fct_return: Factor return
    dt_range: date range (must in Fct_return index)  
    vra_halflife: exponential decay half life
    vra_ewm_length: exponential moving window
    '''
    if dt_range is None:
        dt_range=Fct_return.index
    if len(dt_range)<(vra_ewm_length):
        warnings.warn('history too short, volatility regime risk adjustment failed')
        return F
    Fct_volatility=sigma_gen_range(Fct_return=Fct_return,dt_range=dt_range,sigma_gen_ewm_length=vra_ewm_length,**kwargs)
    lambda_sq=Fct_return.div(Fct_volatility.replace(0,np.nan).ffill())\
                        .pow(2)\
                        .ewm(halflife=vra_halflife,min_periods=vra_ewm_length)\
                        .mean().mean(axis=1)\
                        .fillna(1)
    return F.unstack().mul(lambda_sq,axis=0).stack(dropna=False)

def eigen_one(F_oneday):
    if F_oneday.isnull().any().any():
        return pd.Series(),pd.DataFrame(index=F_oneday.index)
    if np.linalg.matrix_rank(F_oneday)<F_oneday.shape[0]:
        raise Exception('rank error')
    D,U=linalg.eigh(F_oneday)
    return pd.Series(D),pd.DataFrame(U,index=F_oneday.index)

def eigen_one_reverse(D,U):
    return pd.DataFrame(U.values @ np.diag(D.values) @ U.T.values,columns=U.index,index=U.index)

def get_fct_weight(F):
    '''
    return unalianed weights. ie l2_norm(w)=1
    '''
    D=pd.DataFrame()
    W=[]
    for dt in F.index.get_level_values(0).unique():
        F_oneday=F.xs(dt,level=0)
        d,w=eigen_one(F_oneday)
        D=D.append(d.rename(dt))
        W.append(w)
    W_new=pd.concat(W,keys=F.index.get_level_values(0).unique())
    return D,W_new
    
def get_fct_bs(F,Fct_return,mon=21,periods=12):
    '''
    get factor-eigen bias stats to adjust
    21*12=252 trading dates are needed
    '''
    D,W=get_fct_weight(F)
    mon_inx=np.array(range(Fct_return.shape[0]))%mon  
    
    S=pd.concat([factor_portfolio_std(W.xs(dt,level=0),F.xs(dt,level=0)).rename(dt) for dt in Fct_return.index],axis=1).T
    S_lst=[S.loc[mon_inx==i].reindex(S.index,method='ffill') for i in range(mon)]
 
    R_lst=[]
    for i in range(mon):
        W_tmp=W.loc[(list(S.index[mon_inx==i]),slice(None))]
        W_tmp2=W_tmp.reindex(W.index).unstack().ffill().stack(dropna=False)
        R_tmp=pd.DataFrame()
        for dt in Fct_return.index:
            R_tmp=R_tmp.append(factor_portfolio_r(W_tmp2.xs(dt,level=0),Fct_return.loc[dt]).rename(dt))
        R_mean=R_tmp.rolling(mon).mean()
        R_mean_tmp=R_mean.loc[mon_inx==(i-1)%mon]
        R_lst.append(R_tmp-R_mean_tmp.reindex(R_tmp.index,method='bfill'))
 
    bs_last=pd.DataFrame()
    for i in range(Fct_return.shape[0]):
        if i < periods*mon:
            continue
        else:
            flag=mon_inx[i]
            R=R_lst[flag]
            S=S_lst[flag]
            b=R.iloc[(i-periods*mon):i].mul(np.sqrt(mon)).div(S.iloc[(i-periods*mon):i])
            dt=R.index[i]
            bs_last=bs_last.append(b.std().rename(dt))
    return bs_last,D,W

def eigen_adj_range(F,Fct_return,**kwargs):
    '''
    F: factor cov matrix
    Fct_return: fatcor return
    '''
    bs,D,W=get_fct_bs(F,Fct_return,**kwargs)
    D_tmp=bs.pow(2).mul(D)
    F_lst=[]
    keys=[]
    for dt in D_tmp.index:
        D_one=D_tmp.loc[dt]
        U_one=W.xs(dt,level=0)
        if D_one.isnull().any() or U_one.isnull().any().any():
            continue
        else:
            F_lst.append(eigen_one_reverse(D_one,U_one))
            keys.append(dt)
    return pd.concat(F_lst,keys=keys)

def cov_matrix_gen_range(Fct_return,dt_range=None,vr_adjust=True,eigen_adjust=True,**kwargs):
    '''
    predicted covariance matrix generator
    returns an adjusted covariance matrix of the n days after dt
    
    Fct_return: Factor return
    dt_range: date range (must in Fct_return index)
    eigen_adjust: whether to apply eigenfactor risk adjustment
    vr_adjust: whether to apply volatility regime risk adjustment
    -----------------------------------------------------------------
    **kwargs include:
        ---[ forecast factor volatility ]---
        var_halflife: exponential decay half life
        var_ewm_length: exponential moving window
        var_lag: Newey-West series correlation lag
        mon: n days, typically one month n=21
        
        ---[ forecast factor correlation ]---
        cor_halflife: exponential decay half life
        cor_ewm_length: exponential moving window
        cor_lag: Newey-West series correlation lag
        
        ---[ volatility regime risk adjustment ]---
        sigma_gen_halflife: exponential decay half life
        sigma_gen_ewm_length: exponential moving window             
        vra_halflife: exponential decay half life
        vra_ewm_length: exponential moving window
        
        ---[ eigen adjustment ]---
         mon: n days, typically one month n=21
         periods: months to calculate bias stats
    '''
    std=sigma_range(Fct_return=Fct_return,dt_range=dt_range,**kwargs)
    cor=rho_range(Fct_return=Fct_return,dt_range=dt_range,**kwargs)
    F=cor.unstack().mul(std,level=0).mul(std,level=1).stack(dropna=False)
    
    if eigen_adjust:
        tt0=time.time()
        F=eigen_adj_range(F,Fct_return.loc[F.unstack().index],**kwargs)
        tt1=time.time()
        print('Eigen Adj time  %0.2f s'%(tt1-tt0))
    if vr_adjust:
        tt0=time.time()
        F=vr_adj_range(F=F,Fct_return=Fct_return,dt_range=dt_range,**kwargs)
        tt1=time.time()
        print('VRA time  %0.2f s'%(tt1-tt0))          
    result={dt:F.xs(dt,level=0) for dt in F.index.get_level_values(0)}
    return result

def cov_matrix_oneday(Fct_return,dt,minimal_span=270,vr_adjust=True,eigen_adjust=True,**kwargs):
    '''
    minimal_dt: 270 if eigen_adjust, otherwise can be shorter
    '''
    dt_range=read.reading_data.trading_dt[read.reading_data.trading_dt<=dt][-minimal_span:].tolist()
    if not pd.Series(dt_range).isin(Fct_return.index).all():
        raise Exception('Fct_return should include a minimal dt_range')
    result=cov_matrix_gen_range(Fct_return,dt_range=dt_range,**kwargs)
    return result[dt]