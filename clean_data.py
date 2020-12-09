# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 17:14:23 2019

@author: smorandv
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def rm_ext_and_nan(CTG_features, extra_feature):
    """

    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A dictionary of clean CTG called c_ctg
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    CTG_features =CTG_features.drop(extra_feature,axis =1)
    def isnumber(x):
        if type(x)==float or type(x)==int:
            return x
        else:
            return 'nan'
    
    
    CTG_features =CTG_features.applymap(isnumber)
    CTG_features =CTG_features.to_dict('list')
    c_ctg ={k:[elem for elem in v if elem is not 'nan'] for k,v in CTG_features.items()}
    # --------------------------------------------------------------------------
    return c_ctg


def nan2num_samp(CTG_features, extra_feature):
    """

    :param CTG_features: Pandas series of CTG features
    :param extra_feature: A feature to be removed
    :return: A pandas dataframe of the dictionary c_cdf containing the "clean" features
    """
    c_cdf = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    CTG_features =CTG_features.drop('DR',axis =1)
    def isnumber(x):
        if type(x)==float or type(x)==int:
            return x
        else:
            return 'nan'


    CTG_features =CTG_features.applymap(isnumber)
    CTG_features.head()
    for col in CTG_features.columns:
        data = CTG_features[col]
        clean = data[data!='nan']
        p = clean.value_counts(normalize=True)
        a = data[data== 'nan']
        #print(p.index)
        #print(a.shape)
        value =np.random.choice(p.index, size=a.shape, replace=True, p=p.values)
        #print(value)
        data[data=='nan'] = value
        #print(data[data=='nan'])
        CTG_features[col] =data
    
    c_cdf = CTG_features.to_dict()
    # -------------------------------------------------------------------------
    return pd.DataFrame(c_cdf)


def sum_stat(c_feat):
    """

    :param c_feat: Output of nan2num_cdf
    :return: Summary statistics as a dicionary of dictionaries (called d_summary) as explained in the notebook
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    c_stat = c_feat.describe()
    a_stat = c_stat.loc[['min','25%','50%','75%','max'],:]
    a_stat.index = ['min','Q1','median','Q3','max']
    d_summary = a_stat.to_dict()
    # -------------------------------------------------------------------------
    return d_summary


def rm_outlier(c_feat, d_summary):
    """

    :param c_feat: Output of nan2num_cdf
    :param d_summary: Output of sum_stat
    :return: Dataframe of the dictionary c_no_outlier containing the feature with the outliers removed
    """
    c_no_outlier = {}
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------

    
    UP ={}
    LOW ={}
    c_no_outlier ={}
    c_no_outlier =c_feat.to_dict()
    for k in c_no_outlier.keys():
      
        Q1 = d_summary[k]['Q1'] 
        Q3 = d_summary[k]['Q3']
        IQR = Q3-Q1
        UP=(Q3+1.5*IQR)
        LOW=(Q1-1.5*IQR)
        for i in (range(1,2127)):
            if (c_no_outlier[k][i]>UP) or (c_no_outlier[k][i]<LOW):
                c_no_outlier[k][i] = None
    

    
    # -------------------------------------------------------------------------
    return pd.DataFrame(c_no_outlier)


def phys_prior(c_cdf, feature, thresh):
    """

    :param c_cdf: Output of nan2num_cdf
    :param feature: A string of your selected feature
    :param thresh: A numeric value of threshold
    :return: An array of the "filtered" feature called filt_feature
    """
    # ------------------ IMPLEMENT YOUR CODE HERE:-----------------------------
    data = c_cdf[feature].to_numpy()
    data[data>thresh]=None
    filt_feature = data
    # -------------------------------------------------------------------------
    return filt_feature


def norm_standard(CTG_features, selected_feat=('LB', 'ASTV'), mode='none', flag=False):
    """

    :param CTG_features: Pandas series of CTG features
    :param selected_feat: A two elements tuple of strings of the features for comparison
    :param mode: A string determining the mode according to the notebook
    :param flag: A boolean determining whether or not plot a histogram
    :return: Dataframe of the normalized/standardazied features called nsd_res
    """
    x, y = selected_feat
    # ------------------ IMPLEMENT YOUR CODE HERE:------------------------------
    nsd_res=CTG_features
    
    if mode == 'none':
        nsd_res=CTG_features
        
    elif mode == 'standard':
        mean_x=CTG_features.mean()
        std_x = CTG_features.std()
        nsd_res=((CTG_features-mean_x)/(std_x))
       
    elif mode == 'MinMax':
        min_x = CTG_features.min()
        max_x = CTG_features.max()
        nsd_res=((CTG_features-min_x)/(max_x-min_x))
        
    elif mode == 'mean':
        min_x = CTG_features.min()
        max_x = CTG_features.max()
        mean_x=CTG_features.mean()
        nsd_res =  (CTG_features-mean_x)/(max_x-min_x)
        
    if flag:
        import matplotlib.pyplot as plt
        gtc_x=[]
        gtc_y=[]
        gtc_x=nsd_res[x]
        gtc_y=nsd_res[y]
        
        Q = pd.DataFrame( gtc_x)
        Q.hist(bins = 100)
        plt.figure()
        
        plt.show()
        P = pd.DataFrame(gtc_y)
        P.hist(bins = 100)
        plt.figure()
        plt.show()
           
    # -------------------------------------------------------------------------
    return pd.DataFrame(nsd_res)
