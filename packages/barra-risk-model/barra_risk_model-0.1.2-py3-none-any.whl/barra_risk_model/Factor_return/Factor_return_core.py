# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 11:03:21 2018

@author: yili.peng
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings
import time
from RNWS import read,write
from ..common.set_path import make_path,make_path_factor
from ..common.cprint import cprint


def replace_outlier(df,df_all,adj_ratio=3,err_ratio=5):
    '''
    process outliers
    
    df: dataframe (of style factors) with only numeric entries - chosen df
    df_all: dataframe (of style factors) with only numeric entries - total df
    adj_ratio: threshold to clip
    err_ration: threshold to delete
    '''
    mu=df.mean()
    sd=df.std()
    df_new=df.loc[~((df>mu+err_ratio*sd)|(df<mu-err_ratio*sd)).any(axis=1)]
    df_new2=df_new.clip(lower=mu-adj_ratio*sd,upper=mu+adj_ratio*sd,axis=1)
    df_all_new=df_all.loc[~((df_all>mu+err_ratio*sd)|(df_all<mu-err_ratio*sd)).any(axis=1)]
    df_all_new2=df_all_new.clip(lower=mu-adj_ratio*sd,upper=mu+adj_ratio*sd,axis=1)
    return df_new2,df_all_new2
def standardization(df,df_all):
    return (df-df.mean())/df.std(),(df_all-df.mean())/df.std()
def split_xy(sample,factor):
    train_inx=sample.dropna().index
    test_inx=sample.loc[sample[factor].isna()].index
    return train_inx,test_inx
def fill_missing(df,df_all):
    '''
    fill missing values of style factors by regression method
    
    df: standard dataframe - chosen 
    df_all: - total
    '''
    X_col=['SRCap','f_industry']
    y_col=df.drop(['SRCap','f_industry','ExcReturn'],axis=1).columns
    for factor in y_col:
        sample=df[X_col+[factor]]
        sample_all=df_all[X_col+[factor]]
        train_inx,test_inx=split_xy(sample,factor)
        _,test_all_inx=split_xy(sample_all,factor)        
        if len(train_inx)==0:
            raise Exception('no data of %s'%factor)
        if (len(test_inx)==0) and (len(test_all_inx)==0):
            continue
        
        X_all=pd.get_dummies(sample_all[X_col],drop_first=True)
        X=X_all.loc[sample.index]
        
        model=LinearRegression()
        model.fit(X=X.loc[train_inx],y=sample.loc[train_inx,factor])
        if (len(test_inx)>0):
            df.loc[test_inx,factor]=model.predict(X=X.loc[test_inx])
        if (len(test_all_inx)>0):
            df_all.loc[test_all_inx,factor]=model.predict(X=X_all.loc[test_all_inx])
    return df,df_all
def df_oneday(R,Factors_styl,Factor_ind,SRCap,dt,stock_filter=None):
    '''
    convert original dataframes of stock returns, style factors, industry factors and SRCap to a standard (daily) dataframe at time dt
    standard dataframe: dataframe with columns ['SRCap','f_industry','ExcReturn'] and style factors and indices of all stock tickers
    
    R: stock excess returns
    Factors_styl: style factors
    Factor_ind: industry factors
    SRCap: square root capitalization
    stock_filter: daily stock pool
    dt: date (must in indices of above dataframe)
    '''
    if stock_filter is not None:
        S_list=[SRCap.loc[dt].reindex(stock_filter.at[dt]).rename('SRCap'),R.loc[dt].reindex(stock_filter.at[dt]).rename('ExcReturn'),Factor_ind.loc[dt].reindex(stock_filter.at[dt]).rename('f_industry')]
        S_list.extend([Factors_styl[factor_name].loc[dt].reindex(stock_filter.at[dt]).rename(factor_name) for factor_name in Factors_styl.keys()])
    else:
        S_list=[SRCap.loc[dt].rename('SRCap'),R.loc[dt].rename('ExcReturn'),Factor_ind.loc[dt].rename('f_industry')]
        S_list.extend([Factors_styl[factor_name].loc[dt].rename(factor_name) for factor_name in Factors_styl.keys()])
    df=pd.concat(S_list,axis=1) 
    return df
def wls_constrain(y,X,h,w):
    '''
    problematic
    
    weighted least square regression with constrain, return beta and epsilon
    
    y=X*beta+epsilon 
    minimize (y-X*beta)'H(y-X*beta) subject to w'beta=0
    where H = diag(h)
    '''
    beta_names=X.columns
    y=y.values.reshape(-1,1)
    h=h.values.reshape(-1,1)
    w=w.values.reshape(-1,1)
    X=X.values
    A=np.linalg.pinv(X.T @ (h*X))
    B=X.T @ (h*y)
    beta_hat=A @ (B - (w.T @ A @ B)/(w.T @ A @ w) * w)
    return pd.Series(beta_hat.reshape(-1),index=beta_names,name='beta')
def reg_oneday(df):
    '''
    perform regression for oneday
    
    df: standard dataframe
    '''
    weight=df['SRCap']
    cap=weight**2
    y=df['ExcReturn']
    X=df.drop(['SRCap','ExcReturn'],axis=1)
#    X['f_country']=1
    X1=X.copy()
    X1.loc[:,X1.columns!='f_industry']=0
    X1=pd.get_dummies(X1)
    X=pd.get_dummies(X)    
    constrain_weight=X1.multiply(cap,axis=0).sum()
    fct_return=wls_constrain(y,X,weight,constrain_weight)
    return fct_return
def reg_oneday_fill(df,beta):
    y=df['ExcReturn']
    X=df.drop(['SRCap','ExcReturn'],axis=1)
#   X['f_country']=1
    X=pd.get_dummies(X)
    epsilon=y-X.mul(beta).sum(axis=1)
    return y,X,epsilon
def pipeline(df):
    '''
    processing df to df_param & df_style
    '''
    df_style=df.drop(['SRCap','ExcReturn','f_industry'],axis=1)
    df_param=df[['SRCap','ExcReturn','f_industry']]
    df_param.dropna(inplace=True)
    return df_style,df_param
def factor_return_gen(R,SRCap,Factor_ind,Factors_styl,stock_pool,dt_range):
    '''
    generate factor returns and specific returns over a history period
    
    R: stock excess returns
    Factors_styl: style factors
    Factor_ind: industry factors
    SRCap: square root capitalization
    stock_pool: daily stock pool
    dt_range: a time period. Shall be the same as indices of above dataframe
    '''
    warnings.simplefilter("ignore")
    cprint('\t\tGenerate factor return',c='',f='l')
    Fct_return=pd.DataFrame()
    Spc_return=pd.DataFrame()
    R1=pd.DataFrame()
    X1=pd.DataFrame()
    ym_hist='000000'
    t0=time.time()
    t00=time.time()
    for dt1 in dt_range:
        ym_new=str(dt1)[:6]
        if ym_hist!=ym_new:
            t1=time.time()
            cprint('--- time spent %0.3f s'%(t1-t0))
            cprint('yearmonth:%s'%ym_new)
            ym_hist=ym_new
            t0=t1
        df=df_oneday(R,Factors_styl,Factor_ind,SRCap,dt1,stock_filter=stock_pool)
        df_style,df_param=pipeline(df)
        
        df_all=df_oneday(R,Factors_styl,Factor_ind,SRCap,dt1,stock_filter=None)
        df_all_style,df_all_param=pipeline(df_all)
        
        df_style,df_all_style=replace_outlier(df_style,df_all_style)
        df_style,df_all_style=standardization(df_style,df_all_style)
        
        df_clean=pd.merge(df_param,df_style,left_index=True,right_index=True,how='left')
        df_all_clean=pd.merge(df_all_param,df_all_style,left_index=True,right_index=True,how='left')
        
        df_filled,df_all_filled=fill_missing(df_clean,df_all_clean)
        
        beta=reg_oneday(df_filled)
        y,X,epsilon=reg_oneday_fill(df_all_filled,beta)
        
        Fct_return=Fct_return.append(beta.rename(dt1))
        Spc_return=Spc_return.append(epsilon.rename(dt1))
        R1=R1.append(y.rename(dt1))
        X['dt']=dt1
        X1=X1.append(X)
    t11=time.time()
    cprint('--- total time: %0.3f s\n'%(t11-t00))
    
    ind_col=('f_industry_'+(Factor_ind.stack(dropna=True).drop_duplicates())).tolist()
    Fct_return[ind_col]=Fct_return[ind_col].fillna(0)
    X1[ind_col]=X1[ind_col].fillna(0)
    X2={}
    for dt,group in X1.groupby('dt'):
        X2[dt]=group.drop('dt',axis=1)
    return R1,X2,Fct_return,Spc_return


def filter_stock(R,SRCap,Factor_ind,Factors_styl,stock_pool,main_stock=None,**kwargs):
    cprint('\t\tStart filtering',c='',f='l')
    t0=time.time()
    main_stock=([] if main_stock is None else main_stock)
    main_stock.extend(list(np.concatenate(stock_pool.tolist())))
    main_stock=list(set(main_stock))
    
    t1=time.time()
    cprint('keep columns %d / %d'%(len(main_stock),R.shape[1]))
    cprint('--- total time: %0.3f s\n'%(t1-t0))
    R_new=R.reindex(columns=main_stock)
    Factor_ind_new=Factor_ind.reindex(columns=main_stock)
    SRCap_new=SRCap.reindex(columns=main_stock)
    Factors_styl_new={key:df.reindex(columns=main_stock) for key,df in Factors_styl.items()}
    return R_new,SRCap_new,Factor_ind_new,Factors_styl_new

def filter_dt(R,SRCap,Factor_ind,Factors_styl,pct_to_keep_core=0.7,pct_to_keep=0.4,**kwargs):
    cprint('\t\tStart aligning',c='',f='l')
    t0=time.time()
    inx_to_drop=[]
    flag=False # continued date
    for inx in R.index:
        if flag:
            break
        if (R.loc[inx].isna().mean()>(1-pct_to_keep_core)) or (Factor_ind.loc[inx].isna().mean()>(1-pct_to_keep_core)) or (SRCap.loc[inx].isna().mean()>(1-pct_to_keep_core)):
            inx_to_drop.append(inx)
        elif any([(Factors_styl[name].loc[inx].isna().mean()>(1-pct_to_keep)) for name in Factors_styl.keys()]):
            inx_to_drop.append(inx)
        else:
            print('start from %d'%inx)
            flag=True
    R_new=R.drop(inx_to_drop,axis=0)
    Factor_ind_new=Factor_ind.drop(inx_to_drop,axis=0)
    SRCap_new=SRCap.drop(inx_to_drop,axis=0)
    Factors_styl_new={name:Factors_styl[name].drop(inx_to_drop,axis=0) for name in Factors_styl.keys()}
    t1=time.time()
    cprint('drop rows %d / %d'%(len(inx_to_drop),R.shape[0]))
    cprint('--- total time: %0.3f s\n'%(t1-t0))
    return R_new,SRCap_new,Factor_ind_new,Factors_styl_new

def factor_return_manufacture(path,dt_range,pool='ZZ800',filter_stock_flag=True,filter_dt_flag=True,**kwargs):
    '''
    path: root path
    dt_range: (start,end)
    pool: ZZ800 ZZ500 HS300 or SZ50 as total stock pool for regression
    kwargs:
        filter_stock
            main_stock=None
        filter_dt 
            pct_to_keep_core=0.7,pct_to_keep=0.4      
    '''
    path_dict=make_path(path)
    path_dict.update(make_path_factor(path))
    start,end=dt_range[0],dt_range[1]
    style_path,ind_path,srcap_path,exr_path,factor_return_path=path_dict['style_path'],path_dict['ind_path'],path_dict['srcap_path'],path_dict['exr_path'],path_dict['freturn_path'] 
    cprint('\t\tStart reading',c='',f='l')
    if pool in ('ZZ800','ZZ500','HS300','SZ50'):
        stock_pool_path=path_dict['index_%s'%pool[2:]]
        stock_pool=read.read_srs(path=stock_pool_path,file_pattern='Stk_%s'%pool,start=start,end=end)
    else:
        raise Exception("pool must in ('ZZ800','ZZ500','HS300','SZ50') ")
    Factors_styl={name:read.read_df(path=style_path,file_pattern=name,start=start,end=end) for name in ['beta','book_to_price','growth','leverage','liquidity','momentum','nl_size','size','rvola']}
    Factor_ind=read.read_df(path=ind_path,file_pattern='ind_factor',start=start,end=end)
    SRCap= read.read_df(path=srcap_path,file_pattern='srcap',start=start,end=end)
    R= read.read_df(path=exr_path,file_pattern='exr',start=start,end=end)
    print('')
    if filter_stock_flag:
        R,SRCap,Factor_ind,Factors_styl = filter_stock(R,SRCap,Factor_ind,Factors_styl,stock_pool,**kwargs)
    if filter_dt_flag:
        R,SRCap,Factor_ind,Factors_styl = filter_dt(R,SRCap,Factor_ind,Factors_styl,**kwargs)
    dt_range=R.index
    Factor_ind=Factor_ind.applymap(lambda x: x if pd.isna(x) else str(x))
    R1,X1,Fct_return,Spc_return=factor_return_gen(R,SRCap,Factor_ind,Factors_styl,stock_pool,dt_range)
    cprint('\t\tStart writing',c='',f='l')
    write.write_df(R1,factor_return_path,'R',encoding='gbk')
    write.write_df(Fct_return,factor_return_path,'Fct_return',encoding='gbk')
    write.write_df(Spc_return,factor_return_path,'Spc_return',encoding='gbk')
    write.write_dict(X1,factor_return_path,'X1',encoding='gbk')