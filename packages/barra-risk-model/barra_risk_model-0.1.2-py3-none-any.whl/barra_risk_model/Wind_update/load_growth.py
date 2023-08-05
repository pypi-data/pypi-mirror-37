# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 18:24:53 2018

@author: yili.peng
"""
from ..common.cprint import cprint
from WindPy import w
import pandas as pd
import time
import os

def loading(*args):
    w_load=w.wsd(*args)
    err_step=0
    while ((w_load.ErrorCode!=0) and (w_load.ErrorCode!=-40520007)):
        cprint('\rTime: '+str(args[2])+' Error:\t'+str(w_load.ErrorCode)+'  ----> sleep 3s and reload\r',c='r')
        time.sleep(3)
        w_load=w.wsd(*args)
        err_step+=1
        if err_step>5:
            cprint('Failed for 5 times',c='r')
            raise Exception('Failed for 5 times')
    return w_load

def loading_lst(stk_lst,dt,field_lst):
    result_dt=pd.DataFrame()
    for l in field_lst:
        w_load=loading(stk_lst, l , dt, dt, "Days=Alldays")
#        if w_load.ErrorCode==-40520007:
#            cprint(str(l)+' '+str(dt)+'  \tNoData',c='r')
#            result_dt=pd.concat([result_dt,pd.Series(None,index=stk_lst,name=l)],axis=1)
#            continue
        result_dt=pd.concat([result_dt,pd.Series(w_load.Data[0],index=w_load.Codes,name=l)],axis=1)
    cprint(str(dt)+'  \tfinished')
    return result_dt.rename_axis('StkID')

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

def load_growth(dt_range,stk_path,growth_path):
    time_list=[t.strftime('%Y%m%d') for t in pd.date_range(start=str(dt_range[0]),end=str(dt_range[1]),freq='y')]
    for t in time_list:
        stk_lst,dt=check_list(t,stk_path)
        df1=loading_lst(stk_lst,dt,['total_shares'])
        df2=loading_lst(stk_lst,t,['gr_ttm2','eps_ttm'])
        df=pd.concat([df1,df2],axis=1)
        df['dt']=t
        df.to_csv(''.join([growth_path,'/growth_',t,'.csv']))