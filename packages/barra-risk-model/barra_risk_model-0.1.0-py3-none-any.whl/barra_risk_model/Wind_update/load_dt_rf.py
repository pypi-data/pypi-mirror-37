# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 17:33:59 2018

@author: yili.peng
"""

from WindPy import w
import pandas as pd 

def load_dt(dt_range,dt_path):
    '''
    #overwrite
    #dt_range=(20100101,20181231)
    '''
    pd.Series([dt.strftime('%Y%m%d') for dt in w.tdays(str(dt_range[0]), str(dt_range[1]), "").Times]).to_csv(dt_path+'/trading_date.csv',index=False)

def load_rf(dt_range,rf_path):
    '''
    overwrite
    dt_range=(20100101,20180630)
    '''
    if dt_range[0]<20150101:
        w_load_1=w.wsd("CGB1Y.WI", "close",str(dt_range[0]), str(20150101), "")
        w_load=w.wsd("TB1Y.WI", "close",str(20150101), str(dt_range[1]), "")
        if (w_load.ErrorCode!=0) or (w_load_1.ErrorCode!=0):
            raise Exception('Wind error')
        rate_1=pd.Series(w_load_1.Data[0],index=w_load_1.Times)/100
        rate=pd.Series(w_load.Data[0],index=w_load.Times)/100
        rate_1.append(rate).ffill().to_csv(rf_path+'/risk_free_rate.csv')
    else:
        w_load=w.wsd("TB1Y.WI", "close",str(dt_range[0]), str(dt_range[1]), "")
        if (w_load.ErrorCode!=0):
            raise Exception('Wind error')
        rate=pd.Series(w_load.Data[0],index=w_load.Times)/100
        rate.ffill().to_csv(rf_path+'/risk_free_rate.csv')