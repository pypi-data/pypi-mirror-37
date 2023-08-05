# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 15:26:18 2018

@author: yili.peng
"""
import pandas as pd
import numpy as np
from sklearn import linear_model
import warnings
import time
from RNWS import read
from .Factor_matrix_core import sigma_range

def structuralModelAdj_range(sigma_TS,Spc_return,X1,stock_pool,gamma_n=None,dt_range=None,E0=1.1,**kwargs):
    dt_range=(sigma_TS.index if dt_range is None else dt_range)
    gamma_n=(pd.DataFrame(1,index=Spc_return.index,columns=Spc_return.columns) if gamma_n is None else gamma_n)
    Sigma_n_hat=pd.DataFrame()
    for dt1 in dt_range:
        stock_pool_dt=stock_pool.loc[dt1]
        sigma_TS_dt=sigma_TS.loc[dt1]
        X1_dt=X1[dt1]
        data_temp=pd.merge(sigma_TS_dt.to_frame(),X1_dt,how='left',left_index=True, right_index=True)
        data=data_temp.reindex(stock_pool_dt).dropna()
        if data.shape[0]==0:
#            warnings.warn('training data is empty. Failed to do structural adjustment at %s'%str(dt1))
            Sigma_n_hat=Sigma_n_hat.append(sigma_TS.loc[dt1])
            continue
        na_stock_index=data_temp[data_temp.isnull().any(axis=1)].index
        na_stock_res=pd.Series(np.nan,index=na_stock_index,name=dt1)
        data_pred=data_temp.dropna()
        gamma_n_dt=gamma_n.loc[dt1].reindex(data_pred.index)
        data_Y=np.log(data[dt1].values)
        data_X=data.drop(dt1,axis=1).values             
        data_pred_x=data_pred.drop(dt1,axis=1).values
        regr = linear_model.LinearRegression(fit_intercept=False)
        regr.fit(data_X, data_Y)
        y_hat=regr.predict(data_pred_x)
        sigma_STR=E0*np.exp(y_hat)   
        sigma_res=pd.Series((gamma_n_dt.values*data_pred[dt1]+(1-gamma_n_dt)*sigma_STR),index=data_pred.index)
        Sigma_n_hat=Sigma_n_hat.append(sigma_res.append(na_stock_res))
    return Sigma_n_hat
def BayesianSKG_range(Sigma_n_hat,Spc_return,Cap,dt_range=None,q=0.1,**kwargs):
    dt_range=(Sigma_n_hat.index if dt_range is None else dt_range)      
    sigma_SH_final=pd.DataFrame()
    for dt1 in dt_range:
        Sigma_n_hat_dt=Sigma_n_hat.loc[dt1].to_frame()            
        na_sigma_temp=Sigma_n_hat_dt[Sigma_n_hat_dt[dt1].isnull()][dt1]            
        sigma_rank=Sigma_n_hat_dt.dropna()
        if sigma_rank.shape[0]==0:
#            warnings.warn('sigma is empty. Failed to do baysian adjustment at %s'%str(dt1))
            sigma_SH_final=sigma_SH_final.append(Sigma_n_hat.loc[dt1])
            continue
        sigma_rank['group']=pd.qcut(sigma_rank[dt1],10,labels=False)
        sigma_vs_cap=sigma_rank.copy()
        sigma_vs_cap['cap']=Cap.loc[dt1].reindex(sigma_rank.index)
        sigma_vs_cap['sigma_sn_cw_avg']=sigma_vs_cap.cap / sigma_vs_cap.groupby('group').cap.transform("sum") * sigma_vs_cap[dt1]
        sigma_vs_cap['delt_sigma_sn_tmp']=np.square(sigma_vs_cap[dt1]-sigma_vs_cap['sigma_sn_cw_avg']) / sigma_vs_cap.groupby('group').group.transform(np.size)
        delt_sigma_sn=np.sqrt(sigma_vs_cap.groupby('group').agg({'delt_sigma_sn_tmp':sum})).reindex(sigma_vs_cap['group'])
        sigma_vs_cap['delt_sigma_sn']=delt_sigma_sn.values
        sigma_vs_cap['Vn']=(q*abs(sigma_vs_cap[dt1]-sigma_vs_cap['sigma_sn_cw_avg']))/(sigma_vs_cap['delt_sigma_sn']+q*abs(sigma_vs_cap[dt1]-sigma_vs_cap['sigma_sn_cw_avg']))  
        sigma_SH=sigma_vs_cap['Vn']*sigma_vs_cap['sigma_sn_cw_avg']+(1-sigma_vs_cap['Vn'])*sigma_vs_cap[dt1]
        sigma_SH=sigma_SH.append(na_sigma_temp)
        sigma_SH_final=sigma_SH_final.append(sigma_SH.rename(dt1))
    return sigma_SH_final
def vr_adj(sigma_SH_final,Spc_return,Cap,dt_range=None,vra_halflife=42,vra_ewm_length=50,forecast_time_span=21,**kwargs):
    dt_range=(sigma_SH_final.index if dt_range is None else dt_range)
    if len(dt_range)<(vra_ewm_length):
#        warnings.warn('history too short, volatility regime risk adjustment failed')
        return sigma_SH_final
    bs_final_sq=pd.Series()
    for dt1 in dt_range:
        Spc_return_dt=Spc_return.loc[dt1].rename('Spc_return').to_frame()
        sigma_SH_final_dt=sigma_SH_final.loc[dt1].dropna()
        if sigma_SH_final_dt.shape[0]==0:
            bs_final_sq.at[dt1]=np.nan
            continue
        Spc_return_dt=Spc_return.loc[dt1].reindex(sigma_SH_final_dt.index)
        cap_dt=Cap.loc[dt1].reindex(sigma_SH_final_dt.index)
        bs_dt_sq=np.average(np.square(Spc_return_dt/sigma_SH_final_dt)*forecast_time_span,weights=cap_dt)
        bs_final_sq.at[dt1]=bs_dt_sq
    lam=np.sqrt(bs_final_sq.ewm(halflife=vra_halflife,min_periods=vra_ewm_length).mean())
    return sigma_SH_final.multiply(lam,axis=0)
        
def spc_matrix_gen_range(Spc_return,dt_range=None,X_all=None,stock_pool=None,cap=None,gamma_n=None,structural_adj=True,bayesian_shrinkage=True,vr_adj_spc=True,forecast_time_span=21,**kwargs):
    '''
    predicted specific std generator
    returns specific std of the n days after dt
    
    Spc_return: Spc_return
    dt_range: date range (must in Spc_return index)
    X1,stock_pool,cap,gamma_n: must be given when using adjustments
    structural_adj: whether to apply structural adjustment
    bayesian_shrinkage: whether to apply bayesian_shrinkage
    vr_adjust_spc: whether to apply volatility regime risk adjustment
    forecast_time_span: n days, typically one month n=21
    -----------------------------------------------------------------
    **kwargs include:
        ---[ forecast factor volatility ]---
        var_halflife: exponential decay half life
        var_ewm_length: exponential moving window
        var_lag: Newey-West series correlation lag
        
        ---[ structuralModelAdj ]---
        E0: an empirical number greater than 1
        
        ---[ BayesianSKG_range ]---
        q: empirically 0.1
        
        ---[ VRA ]---
        vra_halflife:exponential decay half life, default 42
        vra_ewm_length:exponential moving window, default 50
    '''
    sigma=sigma_range(Spc_return,forecast_time_span=forecast_time_span,**kwargs)
    if structural_adj:
        if (stock_pool is not None) and (X_all is not None):
            tt0=time.time()
            sigma=structuralModelAdj_range(sigma,Spc_return,X_all,stock_pool,gamma_n=gamma_n,**kwargs)
            tt1=time.time()
            print('Structural Adj time  %0.2f s'%(tt1-tt0))
        else:
            warnings.warn('input stockpool and X1 for structural adjustment')
    if bayesian_shrinkage:
        if cap is not None:
            tt0=time.time()
            sigma=BayesianSKG_range(sigma,Spc_return,Cap=cap,dt_range=dt_range,**kwargs)
            tt1=time.time()
            print('Bayesian SKG time  %0.2f s'%(tt1-tt0))
        else:
            warnings.warn('input cap for bayesian shrinkage')
    if vr_adj_spc:
        if cap is not None:
            tt0=time.time()
            sigma=vr_adj(sigma,Spc_return,Cap=cap,dt_range=dt_range,forecast_time_span=forecast_time_span,**kwargs)
            tt1=time.time()
            print('VRA time  %0.2f s'%(tt1-tt0))
        else:
            warnings.warn('input cap for vra')                
    return sigma

def spc_matrix_oneday(Spc_return,dt,minimal_span=60,X_all=None,stock_pool=None,cap=None,gamma_n=None,structural_adj=True,bayesian_shrinkage=True,vr_adj_spc=True,forecast_time_span=21,**kwargs):
    dt_range=read.reading_data.trading_dt[read.reading_data.trading_dt<=dt][-minimal_span:].tolist()
    if not pd.Series(dt_range).isin(Spc_return.index).all():
        raise Exception('Spc_return should include a minimal dt_range')
    result=spc_matrix_gen_range(Spc_return,dt_range,X_all=X_all,stock_pool=stock_pool,cap=cap,gamma_n=gamma_n,structural_adj=structural_adj,bayesian_shrinkage=bayesian_shrinkage,vr_adj_spc=vr_adj_spc,forecast_time_span=forecast_time_span,**kwargs)
    return result.loc[dt]