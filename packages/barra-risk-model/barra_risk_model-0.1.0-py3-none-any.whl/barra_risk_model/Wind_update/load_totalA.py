# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 17:54:12 2018

@author: yili.peng
"""
from ..common.cprint import cprint
import pandas as pd
from WindPy import w
from datetime import datetime
import time

def get_totalA(start_date,end_date,out_path):
    for i in w.tdays(str(start_date), str(end_date), "").Times:
        dt=i.strftime('%Y%m%d')
        cprint(dt)
        w_load=w.wset("sectorconstituent","date="+dt+";sectorid=a001010100000000;field=wind_code,sec_name")
        err_step=0
        while w_load.ErrorCode!=0:
            cprint('\rTime: '+str(dt)+' Error:\t'+str(w_load.ErrorCode)+'  ----> sleep 3s and reload\r',c='r')
            time.sleep(3)
            w_load=w.wset("sectorconstituent","date="+dt+";sectorid=a001010100000000;field=wind_code,sec_name")
            err_step+=1
            if err_step>5:
                raise Exception('Failed for 5 times')
        df=pd.DataFrame(w_load.Data,index=['StkID','name']).T
        df['dt']=dt
        df.sort_values(by='StkID').to_csv(''.join([out_path,'\Stk_TotalA_',dt,'.csv']),index=False,columns=['dt','StkID','name'],header=False,encoding='gbk')

def load_totalA(dt_range,stk_path):
    out_path=stk_path
    get_totalA(start_date=dt_range[0],end_date=dt_range[1],out_path=out_path)
    with open(''.join([out_path,'\log.txt']),'a') as log:
        log.write('Operation time\t'+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'.\tData updated: from '+str(dt_range[0])+' to '+str(dt_range[0])+'\n')