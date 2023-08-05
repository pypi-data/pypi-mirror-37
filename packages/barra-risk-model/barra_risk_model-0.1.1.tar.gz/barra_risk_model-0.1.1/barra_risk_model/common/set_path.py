# -*- coding: utf-8 -*-
"""
preated on Mon Jul  2 17:36:54 2018

@author: yili.peng
"""

import os

def create_chd_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def make_path(path):
    '''
    path: root path to store data
    '''
    path_dic=dict(
    stk_path=path+'/TotalA'
    ,des_path=path+'/descriptors'
    ,dt_path=path+'/trading_date'
    ,rf_path=path+'/rf_rate'
    ,growth_path=path+'/descriptors/growth'
    ,index_800=path+'/index/ZZ800'
    ,index_300=path+'/index/HS300'
    ,index_500=path+'/index/ZZ500'
    ,index_50=path+'/index/SZ50'
    ,itg_path=path+'/style_descriptor_integration'
    )
    for key,path_list in path_dic.items():
        create_chd_path(path_list)
    return path_dic

def make_path_factor(path):
    '''
    path: root path to store data
    '''
    path_dic=dict(
    srcap_path=path+'/srcap'
    ,style_path=path+'/style_factor'
    ,exr_path=path+'/exr'
    ,ind_path=path+'/ind_factor'
    ,freturn_path=path+'/factor_return_data'
    )
    for key,path_list in path_dic.items():
        create_chd_path(path_list)
    return path_dic