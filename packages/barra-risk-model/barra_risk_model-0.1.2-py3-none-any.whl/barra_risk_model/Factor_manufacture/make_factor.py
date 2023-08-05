# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:23:40 2018

@author: yili.peng
"""
import time
import warnings
from multiprocessing import Pool
import pandas as pd
import numpy as np
from glob import glob
from RNWS import read
from ..common.cprint import cprint
from ..common.set_path import make_path,make_path_factor


def make_exr(dt_range,itg_path,rf_path,exr_path):
    '''
    fist date of dt_range would be empty.
    dt_range must cover 1 more trading day.
    '''
    adjPrice=pd.DataFrame()
    start_dt,end_dt=dt_range[0],dt_range[1]
    trading_dt=read.reading_data.trading_dt
    for dt in trading_dt[(trading_dt>=start_dt)&(trading_dt<=end_dt)].tolist():
        df=pd.read_csv(itg_path+'/descriptors_%d.csv'%dt)
        cprint('read '+str(dt))
        adjPrice=adjPrice.append(pd.Series((df['close']*df['adjfactor']).tolist(),index=df['StkID'],name=dt))
    rs=adjPrice.pct_change().iloc[1:]
    dt_range=rs.index
    rf=pd.read_csv(rf_path+'/risk_free_rate.csv',header=None).rename(columns={0:'dt',1:'rate_free'})
    rf['dt']=rf['dt'].str.replace('-','').astype(int)
    rf=rf.set_index('dt')
    rf=rf.reindex(dt_range)
    rf=np.log(rf+1)/365
    exr=rs.subtract(rf['rate_free'],axis=0)
    for inx in exr.index:
        cprint('write '+str(inx))
        exr.loc[inx].to_csv(exr_path+'/exr_'+str(inx)+'.csv')

def make_srcap(dt_range,des_path,srcap_path):
    trading_dt=read.reading_data.trading_dt
    for d in trading_dt[(dt_range[0]<=trading_dt)&(trading_dt<=dt_range[1])].tolist():
        dt=str(d)
        file=des_path+'/market_'+dt+'.csv'
        cprint('read '+dt)
        try:
            df=pd.read_csv(file,encoding='gbk')
        except UnicodeDecodeError:
            df=pd.read_csv(file,encoding='utf-8')
        s=pd.Series((df['mkt_cap_CSRC']**0.5).tolist(),index=df['StkID'].tolist(),name=dt)
        cprint('write '+dt)
        s.to_csv(srcap_path+'/srcap_'+dt+'.csv')

def make_ind(dt_range,des_path,ind_path,level='level1',mapping=False,ind_mapping_exists=False):
    '''
    ind_mapping
    '''
    trading_dt=read.reading_data.trading_dt
    ind_mapping=(pd.Series() if not ind_mapping_exists else pd.read_csv(ind_path+'/mapping.csv',encoding='gbk',index_col=0,header=None)[1])
    for d in trading_dt[(dt_range[0]<=trading_dt)&(trading_dt<=dt_range[1])].tolist():
        dt=str(d)
        file=des_path+'/ind_'+dt+'.csv'
        cprint('read '+dt)
        try:
            df=pd.read_csv(file,encoding='gbk')
        except UnicodeDecodeError:
            df=pd.read_csv(file,encoding='utf-8')
        s=pd.Series(df[level].tolist(),index=df['StkID'].tolist(),name=dt)
        if not mapping:
            cprint('write '+dt)
            s.to_csv(ind_path+'/ind_factor_'+dt+'.csv',encoding='gbk')
        else:
            for i in s.unique():
                if i not in ind_mapping.index and (not pd.isna(i)):
                    ind_mapping.at[i]=len(ind_mapping)
            ind_mapping.to_csv(ind_path+'/mapping.csv',encoding='gbk')
            cprint('write '+dt)
            pd.Series(ind_mapping.reindex(s.values).values,index=s.index).to_csv(ind_path+'/ind_factor_'+dt+'.csv',encoding='gbk')

class read_in:
    def read_all(itg_path,rf_path,start_dt=None,end_dt=None,**kwargs):  # 完整制作需要回溯 525 天数据
        cprint('start to read',f='l',c='g')
        one_set={}
        adjPrice=pd.DataFrame()
        cap=pd.DataFrame()
        epibs=pd.DataFrame()
        etop=pd.DataFrame()
        cetop=pd.DataFrame()
        sgro=pd.DataFrame()
        egro=pd.DataFrame()
        egib_s=pd.DataFrame()
        btop=pd.DataFrame()
        mlev=pd.DataFrame()
        dtoa=pd.DataFrame()
        blev=pd.DataFrame()
        turn=pd.DataFrame()
        yr_hist='0000'
        t_hist=time.time()
        for p in glob(itg_path+'/descriptors_[0-9]*.csv'):
            dt=p.split('_')[-1].split('.')[0]
            if (start_dt is not None) and (int(dt)<int(start_dt)):
                continue
            elif (end_dt is not None) and (int(dt)>int(end_dt)):
                continue
            df=pd.read_csv(p)
            yr_new=dt[:4]
            if yr_new != yr_hist:
                yr_hist=yr_new
                t_new=time.time()
                cprint('--- time spent: %0.3f s'%(t_new-t_hist))
                cprint('year '+ yr_new)
                t_hist=t_new
            #overall: beta, momentum, size, volatility, nl size
            adjPrice=adjPrice.append(pd.Series((df['close']*df['adjfactor']).tolist(),index=df['StkID'],name=dt))
            cap=cap.append(pd.Series((df['mkt_cap_CSRC']).tolist(),index=df['StkID'],name=dt))
            #earining
            epibs=epibs.append(pd.Series((df['west_eps_FTM']*df['total_shares']/df['close']).tolist(),index=df['StkID'],name=dt))
            etop=etop.append(pd.Series((df['netprofit_ttm']/df['mkt_cap_CSRC']).tolist(),index=df['StkID'],name=dt))
            cetop=cetop.append(pd.Series((df['cashflow_ttm']/df['close']).tolist(),index=df['StkID'],name=dt))
            #growth
            sgro=sgro.append(pd.Series((df['sgro']).tolist(),index=df['StkID'],name=dt))
            egro=egro.append(pd.Series((df['egro']).tolist(),index=df['StkID'],name=dt))
            egib_s=egib_s.append(pd.Series((df['west_sales_CAGR']).tolist(),index=df['StkID'],name=dt))
            #book_to_price
            btop=btop.append(pd.Series((df['tot_liab_shrhldr_eqy']/df['mkt_cap_CSRC']).tolist(),index=df['StkID'],name=dt))
            #leverage
            mlev=mlev.append(pd.Series(((df['mkt_cap_CSRC']+df['wgsd_pfd_stk'].fillna(0)+df['wgsd_debt_lt'].fillna(0))/df['mkt_cap_CSRC']).tolist(),index=df['StkID'],name=dt))
            dtoa=dtoa.append(pd.Series((df['wgsd_debttoassets']).tolist(),index=df['StkID'],name=dt))
            blev=blev.append(pd.Series(((df['tot_liab_shrhldr_eqy']+df['wgsd_pfd_stk'].fillna(0)+df['wgsd_debt_lt'].fillna(0))/df['tot_liab_shrhldr_eqy']).tolist(),index=df['StkID'],name=dt))
            #liquidity
            turn=turn.append(pd.Series((df['turn']).tolist(),index=df['StkID'],name=dt))
        t_new=time.time()
        cprint('--- time spent: %0.3f s'%(t_new-t_hist))
        rf=pd.read_csv(rf_path+'/risk_free_rate.csv',header=None).rename(columns={0:'dt',1:'rate_free'})
        rf['dt']=rf['dt'].str.replace('-','')
        rf=rf.set_index('dt')
        dt_range=adjPrice.index
        rf=rf.reindex(dt_range)
        one_set['rs']=adjPrice.pct_change()
        one_set['cap']=cap
        one_set['epibs']=epibs
        one_set['etop']=etop
        one_set['cetop']=cetop
        one_set['sgro']=sgro
        one_set['egro']=egro
        one_set['egib_s']=egib_s
        one_set['btop']=btop
        one_set['mlev']=mlev
        one_set['dtoa']=dtoa
        one_set['blev']=blev
        one_set['turn']=turn
        one_set['rf']=np.log(rf+1)/365
        cprint('read finished\n',f='l',c='g')
        return one_set

class Math:
    def orthogonalize(y,X,**kwargs):
        '''
        y=b.X+e
        y=(y_1,y_2,...,y_T) (1*T array)
        X=(X_1,X_2,...,X_T) (1*T array)
        '''
        X_tmp=X[~(np.isnan(X)|np.isnan(y))]
        y_tmp=y[~(np.isnan(X)|np.isnan(y))]
        if sum(X_tmp**2)==0:
            return np.array([np.nan for i in range(len(y))])
        beta=sum(y_tmp*X_tmp)/sum(X_tmp**2)
        e=y-beta*X
        return e
    def variance_with_halflife(s,h,**kwargs):
        '''
        s=[s_1,s_2,...,s_T] (list or array)
        '''
        s=np.array(s)
        T=len(s)
        w=0.5**(1/h)
        W=[w**(T-1-i) for i in range(T)]
        avg_w=np.average(a=s,weights=W)
        var_w=np.average((s-avg_w)**2,weights=W)
        return var_w

    def wls_with_halflife_handmade(X,y,h,**kwargs): # 6 times faster!
        '''
        y=(y_1,y_2,...,y_T) (1*T array)
        X=(X_1,X_2,...,X_T) (1*T array)
        '''        
        T=len(y)
        w=0.5**(1/h)
        W=np.array([w**(T-1-i) for i in range(T)])
        W_sum=sum(W)
        W_sum_X=sum(W*X)
        W_sum_X2=sum(W*(X**2))
        W_sum_Y=sum(W*y)
        W_sum_XY=sum(W*X*y)
        base=(W_sum*W_sum_X2-W_sum_X**2)
        if base<1e-7 :
            cprint('singular')
            alpha=beta=sigma=np.nan
        else:
            alpha=(W_sum_X2*W_sum_Y-W_sum_XY*W_sum_X)/base
            beta=(W_sum*W_sum_XY-W_sum_X*W_sum_Y)/base
            e=y-alpha-beta*X
            sigma=np.std(e)
        return alpha,beta,sigma
    def winsorize(srs,drop_pct=0.01,trct_pct=0.05,**kwargs):
        '''
        srs: pd.series
        '''
        thresh=srs.quantile([drop_pct,1-drop_pct,trct_pct,1-trct_pct])
        drop_lower=thresh.iloc[0]
        drop_higher=thresh.iloc[1]
        clip_lower=thresh.iloc[2]
        clip_higher=thresh.iloc[3]
        srs=srs.loc[(srs>drop_lower) & (srs<drop_higher)].clip(lower=clip_lower,upper=clip_higher)
        return srs
    def standardise_with_weight(srs,w):
        '''
        srs: pd.series
        w: cap, pd.series
        '''
        w=w.reindex(srs.index)
        s=srs.fillna(0)
        w.fillna(0,inplace=True)
        return (pd.Series(np.nan,index=srs.index,name=srs.name) if (w==0).all() else (srs-np.average(s,weights=w))/srs.std())

    def sum_with_weight_srs(data,weight):
        data_df=pd.concat(data,axis=1)
        values=np.ma.average(np.ma.masked_array(data_df,np.isnan(data_df)),axis=1,weights=weight).filled(np.nan)
        return pd.Series(values,index=data_df.index)

class Make_factor:
    def __init__(self,one_set,multi=False):
        '''
        multi method is not stable for now
        '''
        self.one_set=one_set
        self.style_factors={}
        self.size=self.one_set['cap']
        self.result_beta=None
        self.result_sigma=None
        self.exr=None
        common_inx=list(set(self.one_set['rf'].index)&set(self.one_set['rs'].index))
        common_inx.sort()
        self.one_set['rf']=self.one_set['rf'].loc[common_inx]
        self.one_set['rs']=self.one_set['rs'].loc[common_inx]
        warnings.filterwarnings("ignore")
        self.multi=multi
    def __call__(self):
        self.make_size()
        self.make_nl_size()
        self.make_book_to_price()
        self.make_leverage()
        self.make_growth()
        self.make_momentum()
        self.make_liquidity()
        self.make_ern()
        if self.multi:
            self.make_beta_mul()
        else:
            self.make_beta()
        self.make_volatility()
        return self.style_factors
    def make_ern(self,frac=(0.68,0.11,0.21)):
        t0=time.time()
        cprint('make_earings')
        result=pd.DataFrame()
        for inx in self.size.index:
            epibs=Math.standardise_with_weight(self.one_set['epibs'].loc[inx],self.size.loc[inx])
            etop=Math.standardise_with_weight(self.one_set['etop'].loc[inx],self.size.loc[inx])
            cetop=Math.standardise_with_weight(self.one_set['cetop'].loc[inx],self.size.loc[inx])
            result_raw=Math.sum_with_weight_srs(data=(epibs,etop,cetop),weight=frac).rename(inx)
            result=result.append(Math.standardise_with_weight(result_raw,self.size.loc[inx]))
        self.style_factors['earings']=result
        t1=time.time()
        cprint('--- time spent: %0.3f s'%(t1-t0))
    def make_size(self):
        t0=time.time()
        cprint('make_size')
        size_raw=np.log(self.one_set['cap'])
        result=pd.DataFrame()
        for inx in self.size.index:
            result=result.append(Math.standardise_with_weight(size_raw.loc[inx],self.size.loc[inx]))
        self.style_factors['size']=result
        t1=time.time()
        cprint('--- time spent: %0.3f s'%(t1-t0))
    def make_nl_size(self,**kwargs):
        t0=time.time()
        cprint('make_nl_size')
        result=pd.DataFrame()
        X=np.log(self.one_set['cap'])
        for inx in X.index: 
            x_srs=X.loc[inx].dropna()
            x=x_srs.values
            y=x**3  
            res=Math.orthogonalize(y,x)
            res_srs=pd.Series(res,index=x_srs.index,name=inx)
            res_srs=Math.winsorize(res_srs,**kwargs)
            res_srs=Math.standardise_with_weight(res_srs,self.size.loc[inx])
            result=result.append(res_srs)
        self.style_factors['nl_size']=result
        t1=time.time()
        cprint('--- time spent: %0.3f s'%(t1-t0))
    def make_book_to_price(self):
        t0=time.time()
        cprint('make_book_to_price')
        btop_raw=self.one_set['btop']
        result=pd.DataFrame()
        for inx in self.size.index:
            result=result.append(Math.standardise_with_weight(btop_raw.loc[inx],self.size.loc[inx]))
        self.style_factors['book_to_price']=result
        t1=time.time()
        cprint('--- time spent: %0.3f s'%(t1-t0))
    def make_leverage(self,frac=(0.38,0.27,0.35)):
        t0=time.time()
        cprint('make_leverage')
        result=pd.DataFrame()
        for inx in self.size.index:
            mlev=Math.standardise_with_weight(self.one_set['mlev'].loc[inx],self.size.loc[inx])
            blev=Math.standardise_with_weight(self.one_set['blev'].loc[inx],self.size.loc[inx])
            dtoa=Math.standardise_with_weight(self.one_set['dtoa'].loc[inx],self.size.loc[inx])
            result_raw=Math.sum_with_weight_srs(data=(mlev,blev,dtoa),weight=frac).rename(inx)
            result=result.append(Math.standardise_with_weight(result_raw,self.size.loc[inx]))
        self.style_factors['leverage']=result
        t1=time.time()
        cprint('--- time spent: %0.3f s'%(t1-t0))
    def make_growth(self,frac=(0.47,0.24,0.11)):
        t0=time.time()
        cprint('make_growth')
        frac=[i/sum(frac) for i in frac]
        result=pd.DataFrame()
        for inx in self.size.index:
            sgro=Math.standardise_with_weight(self.one_set['sgro'].loc[inx],self.size.loc[inx])
            egro=Math.standardise_with_weight(self.one_set['egro'].loc[inx],self.size.loc[inx])
            egib=Math.standardise_with_weight(self.one_set['egib_s'].loc[inx],self.size.loc[inx])
            result_raw=Math.sum_with_weight_srs(data=(sgro,egro,egib),weight=frac).rename(inx)
            result=result.append(Math.standardise_with_weight(result_raw,self.size.loc[inx]))
        self.style_factors['growth']=result
        t1=time.time()
        cprint('--- time spent: %0.3f s'%(t1-t0))
    def make_momentum(self,T=420,L=21,h=126):
        t0=time.time()
        cprint('make_momentum')
        log_exr=np.log(self.one_set['rs']+1).subtract(np.log(self.one_set['rf']['rate_free']+1),axis=0)
        result_raw=log_exr.ewm(halflife=h,min_periods=T).mean().shift(L)
        result=pd.DataFrame()
        for inx in self.size.index:
            result=result.append(Math.standardise_with_weight(result_raw.loc[inx],self.size.loc[inx]))
        self.style_factors['momentum']=result
        t1=time.time()
        cprint('--- time spent: %0.3f s'%(t1-t0))
    def make_liquidity(self,frac=(0.35,0.35,0.3)):
        t0=time.time()
        cprint('make_liquidity')
        Turn=self.one_set['turn']
        stom=Turn.rolling(21).sum()
        stom[stom<1e-8]=np.nan
        stom=np.log(stom)
        stoq=Turn.rolling(21*3).sum()
        stoq[stoq<1e-8]=np.nan
        stoq=np.log(stoq)/3
        stoa=Turn.rolling(21*12).sum()
        stoa[stoa<1e-8]=np.nan
        stoa=np.log(stoa)/12

        result=pd.DataFrame()
        for inx in self.size.index:
            stom0=Math.standardise_with_weight(stom.loc[inx],self.size.loc[inx])
            stoq0=Math.standardise_with_weight(stoq.loc[inx],self.size.loc[inx])
            stoa0=Math.standardise_with_weight(stoa.loc[inx],self.size.loc[inx])
            result_raw=Math.sum_with_weight_srs(data=(stom0,stoq0,stoa0),weight=frac).rename(inx)
            result=result.append(Math.standardise_with_weight(result_raw,self.size.loc[inx])) 
        self.style_factors['liquidity']=result
        t1=time.time()
        cprint('--- time spent: %0.3f s'%(t1-t0))
    @staticmethod
    def make_beta_core(x):
        s,R,T,h,col=x[0],x[1],x[2],x[3],x[4]
        result_beta_tmp=[]
        result_sigma_tmp=[]
        for i in range(R.shape[0]):
            if i<T:
                result_beta_tmp.append(np.nan)
                result_sigma_tmp.append(np.nan)
            else:
                y=s.iloc[(i-T):i].values
                X=R.iloc[(i-T):i].values
                na_flag=(np.isnan(X)| np.isnan(y))
                if np.mean(na_flag)>0.2:
                    result_beta_tmp.append(np.nan)
                    result_sigma_tmp.append(np.nan)
                    continue
                _,beta,sigma=Math.wls_with_halflife_handmade(X[~na_flag],y[~na_flag],h)
                result_beta_tmp.append(beta)
                result_sigma_tmp.append(sigma)
        return result_beta_tmp,result_sigma_tmp,col
    def make_beta_mul(self,T=252,h=63,processors=None):
        t0=time.time()
        cprint('make_beta')
        exr=self.one_set['rs'].subtract(self.one_set['rf']['rate_free'],axis=0)
        
        R=(exr*self.one_set['cap']).sum(axis=1,min_count=1)/self.one_set['cap'].sum(axis=1,min_count=1)
        
        result_beta=pd.DataFrame(index=R.index)
        result_sigma=pd.DataFrame(index=R.index)
        X=[[exr[col],R,T,h,col] for col in exr.columns]
        cprint('*** beta pool start',c='g')
        tt0=time.time()
        pool = Pool(processes=processors)
        multi_res=pool.map(self.make_beta_core,X)
        pool.close()
        pool.join()
        tt1=time.time()
        cprint('*** beta pool end\n--- pool time: %0.3f s'%(tt1-tt0),c='g')
        for res in multi_res:
            result_beta_tmp=res[0]
            result_sigma_tmp=res[1]
            col=res[2]
            result_beta[col]=result_beta_tmp
            result_sigma[col]=result_sigma_tmp
        result=pd.DataFrame()
        for inx in self.size.index:
            result=result.append(Math.standardise_with_weight(result_beta.loc[inx],self.size.loc[inx])) 
        self.style_factors['beta']=result
        self.result_beta=result
        self.result_sigma=result_sigma
        self.exr=exr
        t1=time.time()
        cprint('--- time spent: %0.3f s'%(t1-t0))
    def make_beta(self,T=252,h=63):
        t0=time.time()
        cprint('make_beta')
        exr=self.one_set['rs'].subtract(self.one_set['rf']['rate_free'],axis=0)
        R=(exr*self.one_set['cap']).sum(axis=1,min_count=1)/self.one_set['cap'].sum(axis=1,min_count=1)
        result_beta=pd.DataFrame(index=R.index)
        result_sigma=pd.DataFrame(index=R.index)
        columns=exr.columns
        n=len(columns)
        for i in range(n):
            col=columns[i]
            cprint('making beta ['+'>'*(((i+1)*30)//n)+' '*(30-((i+1)*30)//n)+']',head='\r',end='\r',c='g')
            s=exr[col]
            result_beta_tmp=[]
            result_sigma_tmp=[]
            for i in range(R.shape[0]):
                if i<T:
                    result_beta_tmp.append(np.nan)
                    result_sigma_tmp.append(np.nan)
                else:
                    y=s.iloc[(i-T):i].values
                    X=R.iloc[(i-T):i].values
                    na_flag=(np.isnan(X)| np.isnan(y))
                    if np.mean(na_flag)>0.2:
                        result_beta_tmp.append(np.nan)
                        result_sigma_tmp.append(np.nan)
                        continue
                    _,beta,sigma=Math.wls_with_halflife_handmade(X[~na_flag],y[~na_flag],h)
                    result_beta_tmp.append(beta)
                    result_sigma_tmp.append(sigma)
            result_beta[col]=result_beta_tmp
            result_sigma[col]=result_sigma_tmp
        print('')
        result=pd.DataFrame()
        for inx in self.size.index:
            result=result.append(Math.standardise_with_weight(result_beta.loc[inx],self.size.loc[inx]))
        self.style_factors['beta']=result
        self.result_beta=result
        self.result_sigma=result_sigma
        self.exr=exr
        t1=time.time()
        cprint('--- time spent: %0.3f s'%(t1-t0))
    def make_volatility(self,T=252,h=42,frac=(0.74,0.16,0.1),processors=None): # after make_beta,make_momentum
        t0=time.time()
        cprint('make_volatility')
        if (self.result_beta is None) or (self.result_sigma is None) or (self.exr is None):
            raise Exception('Make beta first')        
        dastd=self.exr.ewm(halflife=h,min_periods=T).std()
        
        rs=self.one_set['rs']
        rf=self.one_set['rf']
        Z_max=Z_min=np.log(1+rs).subtract(np.log(1+rf['rate_free']),axis=0).rolling(21*12).sum()
        for T in range(1,12):
            tmp=np.log(1+rs).subtract(np.log(1+rf['rate_free']),axis=0).rolling(21*T).sum()
            Z_max=np.maximum(Z_max,tmp)
            Z_min=np.minimum(Z_min,tmp)
        cmra=Z_max-Z_min
            
        hsigma=self.result_sigma   
        rvola_raw=pd.DataFrame()
        for inx in self.size.index:
            dastd0=Math.standardise_with_weight(dastd.loc[inx],self.size.loc[inx])
            cmra0=Math.standardise_with_weight(cmra.loc[inx],self.size.loc[inx])
            hsigma0=Math.standardise_with_weight(hsigma.loc[inx],self.size.loc[inx])
            rv=Math.sum_with_weight_srs(data=(dastd0,cmra0,hsigma0),weight=frac).rename(inx)
            rvola_raw=rvola_raw.append(rv)
        rvola=pd.DataFrame()
        for inx in rvola_raw.index:
            y=rvola_raw.loc[inx].values
            X=self.result_beta.loc[inx].values
            y1=(Math.orthogonalize(y,X) if not ((np.isnan(X)).all() or (np.isnan(y)).all()) else np.array([np.nan for i in range(len(y))]))
            rvola_tmp=pd.Series(y1,index=rvola_raw.columns,name=inx)
            rvola=rvola.append(Math.standardise_with_weight(rvola_tmp,self.size.loc[inx]))
        self.style_factors['rvola']=rvola    
        t1=time.time()
        cprint('--- time spent: %0.3f s'%(t1-t0))


def make_style_factor(dt_range,history_start_date,itg_path,rf_path,style_path):
    '''
    __name__=='__main__' needed 
    dt_range: (start,end) 
    history_start_date: start date to calculating history
    -NOTE: 525 days are needed for full production
    '''
    one_set=read_in.read_all(itg_path,rf_path,start_dt=history_start_date,end_dt=dt_range[1])
    M=Make_factor(one_set)
    style_fac=M()
    for key in style_fac.keys():
        cprint('write '+key)
        df=style_fac[key]
        for inx in df.index:
            if int(inx)>dt_range[0]:
                df.loc[inx].to_csv(style_path+'/'+key+'_'+str(inx)+'.csv')

def manufacture(path,dt_range_dict,history_start_date=None,**ind_kwargs):
    '''
    path: root path to store data
    dt_range_dict: {'key': (start,end) or None if no need for update }
                    key: 'exr', 'srcap', 'ind','styl'
    -NOTE: start should be one more trading day before.
    
    history_start_date: start date to calculating history for style factor
    -NOTE: 525 days are needed for full production
    '''
    path_dict=make_path(path)
    path_dict.update(make_path_factor(path))
    keys=['exr', 'srcap', 'ind','styl']
    for k in keys:
        if k not in dt_range_dict.keys():
            continue
        elif dt_range_dict[k] is None:
            continue
        else:
            if k=='exr':
                cprint('\t\tmake exr',c='',f='l')
                make_exr(dt_range=dt_range_dict[k],itg_path=path_dict['itg_path'],rf_path=path_dict['rf_path'],exr_path=path_dict['exr_path'])
            elif k=='srcap':
                cprint('\t\tmake srcap',c='',f='l')
                make_srcap(dt_range=dt_range_dict[k],des_path=path_dict['des_path'],srcap_path=path_dict['srcap_path'])
            elif k=='ind':
                cprint('\t\tmake ind',c='',f='l')
                make_ind(dt_range=dt_range_dict[k],des_path=path_dict['des_path'],ind_path=path_dict['ind_path'],**ind_kwargs)
            elif (k=='styl') and (history_start_date is not None):
                cprint('\t\tmake styl',c='',f='l')
                make_style_factor(dt_range=dt_range_dict[k],history_start_date=history_start_date,itg_path=path_dict['itg_path'],rf_path=path_dict['rf_path'],style_path=path_dict['style_path'])