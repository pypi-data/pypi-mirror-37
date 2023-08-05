# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 15:45:06 2018

@author: yili.peng
"""

from WindPy import w
from ..common.set_path import make_path
from ..common.cprint import cprint
from .load_dt_rf import load_dt,load_rf
from .load_totalA import load_totalA
from .load_growth import load_growth
from .load_index import load_ZZ800,load_ZZ500,load_HS300,load_SZ50
#from .load_descriptor import load_descriptor
from .load_descriptor_daily import load_descriptor_daily
from .load_descriptor_seasonal import load_descriptor_seasonal
import warnings
from RNWS import detect_last_date
from datetime import date
'''
path='//goodnight/Public/个人工作记录/彭一立/barra/data_source'
dt_range_dict={
         'dt':(20100101,20181231)
        ,'rf':(None,20180701)
        ,'totalA':(None,None) # let it find
        ,'growth':None # do not update
        ,'index':(20180601,20180701)
        ,'descriptor':(20180601,20180701)
        }
update_wind(path,dt_range_dict)
'''
def change_dt(dt_range):
    if type(dt_range) is int:
        return (dt_range,dt_range)
    return dt_range
def fill_dt(dt_range,df_path):   
    dt_range2=dt_range    
    if dt_range[0] is None:
        dt_range2=(detect_last_date(df_path),dt_range2[1])
    if dt_range[1] is None:
        dt_range2=(dt_range2[0],int(date.today().strftime('%Y%m%d')))
    return dt_range2
def fill_dt2(dt_range):
    dt_range2=dt_range
    if dt_range[0] is None:
        dt_range2=(20100101,dt_range2[1])
    if dt_range[1] is None:
        dt_range2=(dt_range2[0],int(date.today().strftime('%Y%m%d')))
    return dt_range2

def update_wind(path,dt_range_dict):
    '''
    path: root path to store data
    dt_range_dict: {'key': (start,end) or None if no need for update }
                key: 'dt','rf','totalA','growth','index','descriptor'
    
    **kwargs:
        update_season_only: default False. Note at least 3 days a head to avoid weekend
        load_season: default False
    
    Important: remenber to reload growth,update_seaon every time after companies posting thier reports!!!
    '''
    warnings.simplefilter('ignore')
    path_dict=make_path(path)
    keys=['dt','rf','totalA','descriptor_annually','index','descriptor_daily','descriptor_seasonal']
    w.start()
    for k in keys:
        if k not in dt_range_dict.keys():
            continue
        elif dt_range_dict[k] is None:
            continue
        else:
            if k=='dt':
                cprint('\t\tload dt',c='',f='l')
                dt_range2=fill_dt2(dt_range_dict[k])
                load_dt(dt_range=dt_range2,dt_path=path_dict['dt_path'])
            elif k=='rf':
                cprint('\t\tload rf',c='',f='l')
                dt_range2=fill_dt2(dt_range_dict[k])
                load_rf(dt_range=dt_range2,rf_path=path_dict['rf_path'])
            elif k=='totalA':
                cprint('\t\tload totalA',c='',f='l')
                dt_range2=fill_dt(dt_range_dict[k],path_dict['stk_path'])
                load_totalA(dt_range=dt_range2,stk_path=path_dict['stk_path'])
            elif k=='descriptor_annually':
                cprint('\t\tload descriptor annually',c='',f='l')
                dt_range=change_dt(dt_range_dict[k])
                dt_range2=fill_dt(dt_range,path_dict['growth_path'])
                load_growth(dt_range=dt_range2,stk_path=path_dict['stk_path'],growth_path=path_dict['growth_path'])
            elif k=='index':
                cprint('\t\tload HS300',c='',f='l')
                dt_range2=fill_dt(dt_range_dict[k],path_dict['index_300'])
                load_HS300(dt_range=dt_range2,weight_path=path_dict['index_300'])
                cprint('\t\tload SZ50',c='',f='l')
                dt_range2=fill_dt(dt_range_dict[k],path_dict['index_50'])
                load_SZ50(dt_range=dt_range2,weight_path=path_dict['index_50'])
                cprint('\t\tload ZZ500',c='',f='l')
                dt_range2=fill_dt(dt_range_dict[k],path_dict['index_500'])
                load_ZZ500(dt_range=dt_range2,weight_path=path_dict['index_500'])
                cprint('\t\tload ZZ800',c='',f='l')
                dt_range2=fill_dt(dt_range_dict[k],path_dict['index_800'])
                load_ZZ800(dt_range=dt_range2,weight_path=path_dict['index_800'])
            elif k=='descriptor_daily':
                cprint('\t\tload descriptor daily',c='',f='l')
                dt_range2=fill_dt(dt_range_dict[k],path_dict['des_path'])
                load_descriptor_daily(dt_range=dt_range2,stk_path=path_dict['stk_path'],des_path=path_dict['des_path'])
            elif k=='descriptor_seasonal':
                cprint('\t\tload descriptor seasonal',c='',f='l')
                dt_range=change_dt(dt_range_dict[k])
                dt_range2=fill_dt(dt_range,path_dict['des_path'])
                load_descriptor_seasonal(dt_range2,stk_path=path_dict['stk_path'],des_path=path_dict['des_path'])
            else:
                continue
    w.close()