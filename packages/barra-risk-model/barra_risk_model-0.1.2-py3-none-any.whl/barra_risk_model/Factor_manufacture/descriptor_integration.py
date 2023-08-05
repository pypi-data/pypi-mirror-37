# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 15:56:38 2018

@author: yili.peng
"""
from ..common.set_path import make_path
from ..common.cprint import cprint
import os
import pandas as pd
from functools import reduce
from RNWS import read

def find_right_file_q(dt):
    '''
    '20150203' -> '20140930','20141231'
    '''
    dt=str(dt)
    year=int(dt[:4])
    md=int(dt[4:])
    if md<630:
        year_tmp1=year_tmp2=str(year-1)
        md_tmp1='0930'
        md_tmp2='1231'
    elif (630<=md<930):
        year_tmp1=str(year-1)
        year_tmp2=str(year)
        md_tmp1='1231'
        md_tmp2='0630'
    else:
        year_tmp1=year_tmp2=str(year)
        md_tmp1='0630'
        md_tmp2='0930'
    return year_tmp1+md_tmp1,year_tmp2+md_tmp2

def find_right_file_y(dt):
    '''
    '20150203' -> '20131231','20141231'
    '''
    dt=str(dt)
    year=int(dt[:4])
    return str(year-2)+'1231',str(year-1)+'1231'

def read_market(dt,des_path):
    file=''.join([des_path,'/market_',str(dt),'.csv'])
    if os.path.isfile(file):
        return pd.read_csv(file).drop('dt',axis=1)
    else:
        return pd.DataFrame(columns=['StkID','close','vwap','adjfactor','susp_days','maxupordown','mkt_cap_CSRC','turn','total_shares'])

def read_prediction(dt,des_path):
    file=''.join([des_path,'/prediction_',str(dt),'.csv'])
    if os.path.isfile(file):
        return pd.read_csv(file).drop('dt',axis=1)
    else:
        return pd.DataFrame(columns=['StkID','west_eps_FTM','west_sales_CAGR'])

def read_update_time(dt,des_path):
    file=''.join([des_path,'/update_time_',str(dt),'.csv'])
    if os.path.isfile(file):
        df=pd.read_csv(file).drop('dt',axis=1)
        df['stm_issuingdate']=df['stm_issuingdate'].str.slice(0,10).str.replace('/','-').str.split('-').str.join('').astype(float)
        return df
    else:
        return pd.DataFrame(columns=['StkID','stm_issuingdate']) 

def read_earning(dt,des_path):
    file=''.join([des_path,'/earning_',str(dt),'.csv'])
    if os.path.isfile(file):
        return pd.read_csv(file).drop('dt',axis=1)
    else:
        return pd.DataFrame(columns=['StkID','netprofit_ttm','cashflow_ttm'])   

def read_growth_r(dt,des_path):
    file=''.join([des_path,'/growth_r_',str(dt),'.csv'])
    if os.path.isfile(file):
        return pd.read_csv(file).drop('dt',axis=1)
    else:
        return pd.DataFrame(columns=['StkID','egro','sgro'])  
        
def read_leverage(dt,des_path):
    file=''.join([des_path,'/leverage_',str(dt),'.csv'])
    if os.path.isfile(file):
        return pd.read_csv(file).drop('dt',axis=1)
    else:
        return pd.DataFrame(columns=['StkID','tot_liab_shrhldr_eqy','wgsd_pfd_stk','wgsd_debt_lt','wgsd_debttoassets'])          

def read_daily(dt,des_path):
    ern=read_earning(dt,des_path)
    mkt=read_market(dt,des_path)
    prd=read_prediction(dt,des_path)
    return reduce(lambda x,y: pd.merge(x,y,on='StkID',how='outer'),[mkt,prd,ern])
    #pd.merge(mkt,prd,on='StkID',how='outer')

def read_quarterly(dt,des_path):
    lvg=read_leverage(dt,des_path)
    return lvg
    #reduce(lambda x,y: pd.merge(x,y,on='StkID',how='outer'),[ern,lvg]) #grt,

def read_yearly(dt,des_path):
    grt=read_growth_r(dt,des_path)
    return grt

def read_stk_srs(dt,stk_path):
    file=''.join([stk_path,'/Stk_TotalA_',str(dt),'.csv'])
    if os.path.isfile(file):
        try:
            stk_lst=pd.read_csv(file,header=None,encoding='gbk')[[1]].rename(columns={1:'StkID'})
        except UnicodeDecodeError:
            stk_lst=pd.read_csv(file,header=None,encoding='utf-8')[[1]].rename(columns={1:'StkID'})
        return stk_lst
    else:
        return pd.DataFrame(columns=['StkID'])

class warm_start:
    des_path='.'
    quarterly_df=read_quarterly('no history',des_path)
    yearly_df=read_yearly('no history',des_path)
 
def stk_pre_partition(dt,dt1,dt2,stk_path,des_path):
    # decompose stkid as three parts according to update time
    all_stkid=read_stk_srs(dt,stk_path)
    thresh_dt2=read_update_time(dt2,des_path)
    thresh2=pd.merge(all_stkid,thresh_dt2,on='StkID',how='left').fillna(1e8)['stm_issuingdate']
    thresh_dt1=read_update_time(dt1,des_path)
    thresh1=pd.merge(all_stkid,thresh_dt1,on='StkID',how='left').fillna({'stm_issuingdate':thresh2})['stm_issuingdate']    
    
    stkid2=all_stkid[thresh2<dt]['StkID'] # new 
    stkid1=all_stkid[(thresh1<dt)&(dt<=thresh2)]['StkID'] # semi-new
    stkid0=all_stkid[dt<=thresh1]['StkID'] # left  
    return stkid2,stkid1,stkid0

def descriptor_compile_quarterly(dt,stk_path,des_path):
    dt1,dt2=find_right_file_q(dt)
    stkid2,stkid1,stkid0=stk_pre_partition(dt,dt1,dt2,stk_path,des_path)
    
    df2=read_quarterly(dt2,des_path)
    stkid2_left=stkid2.loc[~stkid2.isin(df2['StkID'])]
    df_quarterly2=df2.loc[df2['StkID'].isin(stkid2)]
    stkid1=stkid1.append(stkid2_left)
    
    df1=read_quarterly(dt1,des_path)
    stkid1_left=stkid1.loc[~stkid1.isin(df1['StkID'])]
    df_quarterly1=df1.loc[df1['StkID'].isin(stkid1)]
    stkid0=stkid0.append(stkid1_left)
    
    df0=warm_start.quarterly_df
    df_quarterly0=pd.merge(pd.DataFrame(stkid0),df0,on='StkID',how='left')

    df_quarterly=pd.concat([df_quarterly0,df_quarterly1,df_quarterly2],ignore_index=True)
    warm_start.quarterly_df=df_quarterly # update history
    return df_quarterly

def descriptor_compile_yearly(dt,stk_path,des_path):
    dt1,dt2=find_right_file_y(dt)
    stkid2,stkid1,stkid0=stk_pre_partition(dt,dt1,dt2,stk_path,des_path)
    
    df2=read_yearly(dt2,des_path)
    stkid2_left=stkid2.loc[~stkid2.isin(df2['StkID'])]
    df_yearly2=df2.loc[df2['StkID'].isin(stkid2)]
    stkid1=stkid1.append(stkid2_left)

    df1=read_yearly(dt1,des_path)
    stkid1_left=stkid1.loc[~stkid1.isin(df1['StkID'])]
    df_yearly1=df1.loc[df1['StkID'].isin(stkid1)]
    stkid0=stkid0.append(stkid1_left)
    
    df0=warm_start.yearly_df
    df_yearly0=pd.merge(pd.DataFrame(stkid0),df0,on='StkID',how='left')
    
    df_yearly=pd.concat([df_yearly0,df_yearly1,df_yearly2],ignore_index=True)
    warm_start.yearly_df=df_yearly
    return df_yearly

def descriptor_compile(dt,stk_path,des_path):
    dt=int(dt)
    df_daily=read_daily(dt,des_path)
    df_quarterly=descriptor_compile_quarterly(dt,stk_path,des_path)
    df_yearly=descriptor_compile_yearly(dt,stk_path,des_path)
    df=reduce(lambda x,y: pd.merge(x,y,on='StkID',how='outer'),[df_daily,df_quarterly,df_yearly])
    return df.set_index('StkID').sort_index()


def descriptor_integration(path,dt_range,warm_start_quarterly,warm_start_yearly):
    '''
    path: root path to store data
    dt_range: (start,end). Example (20180301,20180508)
    warm_start_quarterly: earlist quarterly renewal date. Should match dt_range. Example 20170930
    warm_start_yearly: earlist yearly renewal date. Should match dt_range. Example 20161231
    
    ATTENTION: First quarter is not used. After quaterly updating file, dt_range should be longer.
    '''
    path_dic=make_path(path)
    des_path=path_dic['des_path']
    stk_path=path_dic['stk_path']
    itg_path=path_dic['itg_path']
    warm_start.quarterly_df=read_quarterly(warm_start_quarterly,des_path)
    warm_start.yearly_df=read_yearly(warm_start_yearly,des_path)
    ym='000000'
    cprint('\t\tdescriptor_integration',c='',f='l')
    trading_dt=read.reading_data.trading_dt
    for dt in trading_dt[(dt_range[0]<=trading_dt)&(trading_dt<=dt_range[1])].tolist():
        dt_format=str(dt)
        df_tmp=descriptor_compile(dt_format,stk_path,des_path)
        df_tmp.to_csv(''.join([itg_path,'/descriptors_',dt_format,'.csv']))
        if dt_format[:6]!=ym:
            cprint(dt_format[:6])
            ym=dt_format[:6]
