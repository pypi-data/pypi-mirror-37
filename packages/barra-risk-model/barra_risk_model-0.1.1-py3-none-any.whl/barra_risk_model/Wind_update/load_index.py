# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 10:13:21 2018

@author: yili.peng
"""
from ..common.cprint import cprint
from WindPy import w
import time
import pandas as pd

#def load_HS300(dt_range,weight_path):
#    start_date,end_date=dt_range[0],dt_range[1]
#    for i in w.tdays(str(start_date), str(end_date), "").Times:
#        dt=i.strftime('%Y%m%d')
#        cprint(dt)
#        w_load=w.wset("indexconstituent","date="+dt+";windcode=000300.SH")
#        err_step=0
#        while w_load.ErrorCode!=0:
#            cprint('\rTime: '+str(dt)+' Error:\t'+str(w_load.ErrorCode)+'  ----> sleep 3s and reload\r',c='r')
#            time.sleep(3)
#            w_load=w.wset("indexconstituent","date="+dt+";windcode=000300.SH")
#            err_step+=1
#            if err_step>5:
#                raise Exception('Failed for 5 times')
#        result_dt=pd.DataFrame(w_load.Data).T
#        result_dt[0]=dt
#        result_dt.to_csv(''.join([weight_path,'\Stk_HS300_',dt,'.csv']),encoding='gbk',index=False,header=False)
#
#def load_ZZ800(dt_range,weight_path):
#    start_date,end_date=dt_range[0],dt_range[1]
#    for i in w.tdays(str(start_date), str(end_date), "").Times:
#        dt=i.strftime('%Y%m%d')
#        cprint(dt)
#        w_load=w.wset("indexconstituent","date="+dt+";windcode=000906.SH")
#        err_step=0
#        while w_load.ErrorCode!=0:
#            cprint('\rTime: '+str(dt)+' Error:\t'+str(w_load.ErrorCode)+'  ----> sleep 3s and reload\r',c='r')
#            time.sleep(3)
#            w_load=w.wset("indexconstituent","date="+dt+";windcode=000906.SH")
#            err_step+=1
#            if err_step>5:
#                raise Exception('Failed for 5 times')
#        result_dt=pd.DataFrame(w_load.Data).T
#        result_dt[0]=dt
#        result_dt.to_csv(''.join([weight_path,'\Stk_ZZ800_',dt,'.csv']),encoding='gbk',index=False,header=False)
#
#def load_ZZ500(dt_range,weight_path):
#    start_date,end_date=dt_range[0],dt_range[1]
#    for i in w.tdays(str(start_date), str(end_date), "").Times:
#        dt=i.strftime('%Y%m%d')
#        cprint(dt)
#        w_load=w.wset("indexconstituent","date="+dt+";windcode=000905.SH")
#        err_step=0
#        while w_load.ErrorCode!=0:
#            cprint('\rTime: '+str(dt)+' Error:\t'+str(w_load.ErrorCode)+'  ----> sleep 3s and reload\r',c='r')
#            time.sleep(3)
#            w_load=w.wset("indexconstituent","date="+dt+";windcode=000905.SH")
#            err_step+=1
#            if err_step>5:
#                raise Exception('Failed for 5 times')
#        result_dt=pd.DataFrame(w_load.Data).T
#        result_dt[0]=dt
#        result_dt.to_csv(''.join([weight_path,'\Stk_ZZ500_',dt,'.csv']),encoding='gbk',index=False,header=False)
#
#def load_SZ50(dt_range,weight_path):
#    start_date,end_date=dt_range[0],dt_range[1]
#    for i in w.tdays(str(start_date), str(end_date), "").Times:
#        dt=i.strftime('%Y%m%d')
#        cprint(dt)
#        w_load=w.wset("indexconstituent","date="+dt+";windcode=000016.SH")
#        err_step=0
#        while w_load.ErrorCode!=0:
#            cprint('\rTime: '+str(dt)+' Error:\t'+str(w_load.ErrorCode)+'  ----> sleep 3s and reload\r',c='r')
#            time.sleep(3)
#            w_load=w.wset("indexconstituent","date="+dt+";windcode=000016.SH")
#            err_step+=1
#            if err_step>5:
#                raise Exception('Failed for 5 times')
#        result_dt=pd.DataFrame(w_load.Data).T
#        result_dt[0]=dt
#        result_dt.to_csv(''.join([weight_path,'\Stk_SZ50_',dt,'.csv']),encoding='gbk',index=False,header=False)

def load_index(dt_range,weight_path,w_ticker,file_pattern):
    start_date,end_date=dt_range[0],dt_range[1]
    for i in w.tdays(str(start_date), str(end_date), "").Times:
        dt=i.strftime('%Y%m%d')
        cprint(dt)
        w_load=w.wset("indexconstituent","date="+dt+";windcode=%s"%w_ticker)
        err_step=0
        while w_load.ErrorCode!=0:
            cprint('\rTime: '+str(dt)+' Error:\t'+str(w_load.ErrorCode)+'  ----> sleep 3s and reload\r',c='r')
            time.sleep(3)
            w_load=w.wset("indexconstituent","date="+dt+";windcode=%s"%w_ticker)
            err_step+=1
            if err_step>5:
                raise Exception('Failed for 5 times')
        result_dt=pd.DataFrame(w_load.Data).T
        result_dt[0]=dt
        result_dt.to_csv(''.join([weight_path,'\%s_'%file_pattern,dt,'.csv']),encoding='gbk',index=False,header=False)  

def load_SZ50(dt_range,weight_path):
    load_index(dt_range=dt_range,weight_path=weight_path,w_ticker='000016.SH',file_pattern='Stk_SZ50')
def load_HS300(dt_range,weight_path):
    load_index(dt_range=dt_range,weight_path=weight_path,w_ticker='000300.SH',file_pattern='Stk_HS300')
def load_ZZ500(dt_range,weight_path):
    load_index(dt_range=dt_range,weight_path=weight_path,w_ticker='000905.SH',file_pattern='Stk_ZZ500')
def load_ZZ800(dt_range,weight_path):
    load_index(dt_range=dt_range,weight_path=weight_path,w_ticker='000906.SH',file_pattern='Stk_ZZ800')