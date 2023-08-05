# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 09:19:15 2018

@author: yili.peng
"""
from ..common.set_path import make_path
import pandas as pd
from sklearn.linear_model import LinearRegression
from functools import reduce
import numpy as np

def read_file(year,growth_path):
    year=str(year)    
    file=''.join([growth_path,'\\growth_',year,'1231.csv'])
    return pd.read_csv(file) # if not exists would raise error
    
def make_df(year,growth_path):
    year=str(year)
    df=read_file(year,growth_path)
    df['eps_'+year]=df['eps_ttm']
    df['sps_'+year]=df['gr_ttm2']/df['total_shares']
    return df[['StkID','eps_'+year]],df[['StkID','sps_'+year]]
    
def produce_regression(s):
    y=s.drop('StkID').astype(float).values
    if sum(np.isnan(y))>0:
        return np.nan
    x=np.array(range(0,60,12))
    mdl=LinearRegression()
    mdl.fit(X=x.reshape(-1,1),y=y)
    a=mdl.coef_[0]*12
    tilde=np.mean(abs(y))
    return a/tilde
    
def make_egro_and_sgro(year,growth_path):
    year=int(year)
    df_eps_0,df_sps_0=make_df(year-4,growth_path)
    df_eps_1,df_sps_1=make_df(year-3,growth_path)
    df_eps_2,df_sps_2=make_df(year-2,growth_path)
    df_eps_3,df_sps_3=make_df(year-1,growth_path)
    df_eps_4,df_sps_4=make_df(year,growth_path)
    df_eps=reduce(lambda x,y: pd.merge(left=x,right=y,on='StkID',how='outer'),[df_eps_0,df_eps_1,df_eps_2,df_eps_3,df_eps_4])
    df_sps=reduce(lambda x,y: pd.merge(left=x,right=y,on='StkID',how='outer'),[df_sps_0,df_sps_1,df_sps_2,df_sps_3,df_sps_4])
    egro=df_eps.apply(produce_regression,axis=1)
    sgro=df_sps.apply(produce_regression,axis=1)
    return pd.DataFrame({'egro':egro.tolist(),'sgro':sgro.tolist()},index=df_eps['StkID'].tolist()).rename_axis('StkID')
    
def make_growth(year_range,path):
    path_dict=make_path(path)
    des_path,growth_path=path_dict['des_path'],path_dict['growth_path']
    year=range(int(year_range[0]),int(year_range[1]))
    for y in year:
        dt=str(y)+'1231'
        print('make '+str(y))
        df=make_egro_and_sgro(y,growth_path)
        df['dt']=dt
        df.to_csv(des_path+'\\growth_r_'+dt+'.csv',index=True)
