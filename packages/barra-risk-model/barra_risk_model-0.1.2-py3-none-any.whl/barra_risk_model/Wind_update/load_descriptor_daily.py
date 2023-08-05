# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 09:19:27 2018

@author: yili.peng
"""

from ..common.cprint import cprint
from WindPy import w
from collections import OrderedDict
import pandas as pd
import time
from datetime import date
#from collections import deque
from RNWS.read import reading_data
#import numpy as np
class C:
    Style=OrderedDict()
    Style['market']=['close','vwap','adjfactor','susp_days','maxupordown','mkt_cap_CSRC','turn','total_shares']
    Style['prediction']=['west_eps_FTM','west_sales_CAGR']
    Style['earning']=['netprofit_ttm','cashflow_ttm']
#    Style['leverage']=['tot_liab_shrhldr_eqy','wgsd_pfd_stk','wgsd_debt_lt','wgsd_debttoassets']
#    Style['update_time']=['stm_issuingdate']
    Ind='industry2'
#    season_end=('0331','0630','0930','1231')
#    season_end_int=(331,630,930,1231)
#    season_dt=[str(y*10000+md) for y in range(reading_data.trading_dt.min()//10000,date.today().year+1) for md in (331,630,930,1231)]
#    season_end_dt=[str(reading_data.trading_dt[reading_data.trading_dt.le(y*10000+md)].iloc[-1]) for y in range(reading_data.trading_dt.min()//10000,date.today().year+1) for md in (331,630,930,1231)]
    
def logger(string,log_path,**kwargs):
    cprint(string,**kwargs)
    with open(log_path+'/log.txt','a') as logger:
        logger.write(''.join([string,'\n']))
    
def loading(*args):
    w_load=w.wsd(*args[1:])
    err_step=0
    while ((w_load.ErrorCode!=0) and (w_load.ErrorCode!=-40520007)):
        logger('\rTime: '+str(args[3])+' Error:\t'+str(w_load.ErrorCode)+'  ----> sleep 3s and reload\r',args[0],c='r')
        time.sleep(3)
        w_load=w.wsd(*args[1:])
        err_step+=1
        if err_step>5:
            logger('Failed for 5 times',args[0],c='r')
            raise Exception('Failed for 5 times')
    return w_load

def loading_daily(stk_lst,key,dt,log_path,des_path):
    result_dt=pd.DataFrame()
    for l in C.Style[key]:
        w_load=loading(log_path,stk_lst, l , dt, dt, "unit=1;currencyType=;rptType=1")
#        if w_load.ErrorCode==-40520007:
#            logger(l+'  \tNoData',log_path,c='r')
#            w_load=loading(log_path,stk_lst, l , dt, dt, "unit=1;currencyType=;rptType=1;Days=Alldays")
#            logger(l+' \treload with paramters Days=Alldays',log_path,c='r')
        result_dt=pd.concat([result_dt,pd.Series(w_load.Data[0],index=w_load.Codes,name=l)],axis=1)
    result_dt['dt']=dt
    result_dt.rename_axis('StkID').to_csv(''.join([des_path,'/',key,'_',dt,'.csv']))
    logger(key+'  \tfinished',log_path)

def loading_ind_daily(stk_lst,dt,log_path,des_path):
    w_load=loading(log_path,stk_lst, C.Ind , dt, dt, "industryType=3;industryStandard=5")
    r=pd.Series(w_load.Data[0],index=w_load.Codes,name=C.Ind)
    df=pd.concat([r,r.str.split('-',expand=True)],axis=1).rename(columns={'industry2':'industry',0:'level1',1:'level2',2:'level3'})
    df.rename_axis('StkID').to_csv(''.join([des_path,'/ind_',dt,'.csv']),encoding='gbk')
    logger('ind  \t\tfinished',log_path)

#def check_load_season(load_season_queue):
#    if all(load_season_queue):
#        return False
#    else:
#        return load_season_queue[-1]
   
def read_file(file):
    stk_lst=[]
    try:
        fd=open(file, 'r',encoding='gbk')
        for line in fd.readlines():
            stk_lst.append(line.strip('\n').split(',')[1])
    except UnicodeDecodeError:
        fd=open(file, 'r',encoding='utf-8')
        for line in fd.readlines():
            stk_lst.append(line.strip('\n').split(',')[1])
    finally:
        fd.close()
        stk_lst.sort()
    return stk_lst
    
def load_descriptor_daily(dt_range,stk_path,des_path):
    log_path=des_path
#    load_season_queue=deque([False,False,load_season],3)    
    for i in w.tdays(str(dt_range[0]), str(dt_range[1]), "").Times:
        dt=i.strftime('%Y%m%d')
        logger('processing  \t'+dt,log_path)
        file=stk_path+'/Stk_TotalA_'+str(dt)+'.csv'
        stk_lst=read_file(file)
#        if not update_season_only:
        for key in ('market','prediction','earning'):
            loading_daily(stk_lst,key,dt,log_path,des_path)
        loading_ind_daily(stk_lst,dt,log_path,des_path)
        
        #load season
#        if dt in C.season_end_dt:
#            season_dt= C.season_dt[np.where(np.array(C.season_end_dt)==dt)[0][0]]
#            for key in ('leverage','update_time'):#,'growth'
#                loading_daily(stk_lst,key,season_dt,log_path,des_path)
