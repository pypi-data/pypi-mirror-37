# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 09:21:29 2018

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
import os
class C:
    Style=OrderedDict()
#    Style['market']=['close','vwap','adjfactor','susp_days','maxupordown','mkt_cap_CSRC','turn','total_shares']
#    Style['prediction']=['west_eps_FTM','west_sales_CAGR']
#    Style['earning']=['netprofit_ttm','cashflow_ttm']
    Style['leverage']=['tot_liab_shrhldr_eqy','wgsd_pfd_stk','wgsd_debt_lt','wgsd_debttoassets']
    Style['update_time']=['stm_issuingdate']
#    Ind='industry2'
#    season_end=('0331','0630','0930','1231')
#    season_end_int=(331,630,930,1231)
    season_dt=[str(y*10000+md) for y in range(reading_data.trading_dt.min()//10000,date.today().year+1) for md in (331,630,930,1231)]
    season_end_dt=[str(reading_data.trading_dt[reading_data.trading_dt.le(y*10000+md)].iloc[-1]) for y in range(reading_data.trading_dt.min()//10000,date.today().year+1) for md in (331,630,930,1231)]
    
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

def loading_season(stk_lst,key,dt,log_path,des_path):
    result_dt=pd.DataFrame()
    for l in C.Style[key]:
        w_load=loading(log_path,stk_lst, l , dt, dt, "unit=1;currencyType=;rptType=1;Days=Alldays")
        result_dt=pd.concat([result_dt,pd.Series(w_load.Data[0],index=w_load.Codes,name=l)],axis=1)
    result_dt['dt']=dt
    result_dt.rename_axis('StkID').to_csv(''.join([des_path,'/',key,'_',dt,'.csv']))
    logger(key+'  \tfinished',log_path)

   
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
    
def check_list(dt,stk_path):
    dt=int(dt)
    file=stk_path+'/Stk_TotalA_'+str(dt)+'.csv'
    while not os.path.exists(file):
        dt-=1
        file=stk_path+'/Stk_TotalA_'+str(dt)+'.csv'
    stk_lst=read_file(file)
    return stk_lst,str(dt)

def load_descriptor_seasonal(dt_range,stk_path,des_path):
    log_path=des_path
#    load_season_queue=deque([False,False,load_season],3)
    for i in pd.date_range(str(dt_range[0]), str(dt_range[1]), freq="Q"):
        dt=i.strftime('%Y%m%d')
        logger('processing  \t'+dt,log_path)
        
#        trading_dt=w.tdays(str(int(dt)-20),dt,'')[-1].strftime('%Y%m%d')
#        file=stk_path+'/Stk_TotalA_'+trading_dt+'.csv'
#        stk_lst=read_file(file)
        
        stk_lst,_=check_list(dt,stk_path)
        
        for key in ('leverage','update_time'):#,'growth'
            loading_season(stk_lst,key,dt,log_path,des_path)