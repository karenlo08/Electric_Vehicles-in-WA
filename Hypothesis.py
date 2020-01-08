from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pandas as pd
import numpy as np


zip_codes_2017_5yr_commute = pd.read_csv('documents/ev/zip_codes_2017_5yr_commute.csv')
zip_codes_2017_5yr_commute.rename(columns={"geo_id": "ZIP Code"}, inplace = True)

pop_ev = pd.read_csv('documents/ev/Electric_Vehicle_Population_Data.csv')
pop_ev_demographics = pd.merge(pop_ev,zip_codes_2017_5yr_commute, on='ZIP Code', how='left')


def calculate median_commute():
    median =(zip_codes_2017_5yr_commute['commute_10_14_mins'].apply(lambda x:x * [1] if x>0 else [0]) + 
    zip_codes_2017_5yr_commute['commute_15_19_mins'].apply(lambda x:x * [2] if x>0 else [0]) +
    zip_codes_2017_5yr_commute['commute_20_24_mins'].apply(lambda x:x * [3] if x>0 else [0]) +
    zip_codes_2017_5yr_commute['commute_25_29_mins'].apply(lambda x:x * [4] if x>0 else [0]) +
    zip_codes_2017_5yr_commute['commute_30_34_mins'].apply(lambda x:x * [5] if x>0 else [0]) +     
    zip_codes_2017_5yr_commute['commute_45_59_mins'].apply(lambda x:x * [6] if x>0 else [0]) ).apply(np.mean).astype(int)

    #Reference
    # commute_dict = {1:'commute_10_14_mins',2:'commute_15_19_mins',3:'commute_20_24_mins',
    #                 4:'commute_25_29_mins',5:'commute_30_34_mins',6:'commute_45_59_mins'}

    zip_codes_2017_5yr_commute['Median_commute'] = median


def decode_make():
    uniq_makes = pop_ev_demographics['Make'].unique()
    make_dict=dict()
    for i in range(len(uniq_makes)):
        make_dict[uniq_makes[i]] =i 

    pop_ev_demographics['Make_decode'] = pop_ev_demographics['Make'].map(make_dict)

def columns_to_correlate():
    df = pop_ev_demographics.groupby('ZIP Code').size().reset_index()
    ev = pd.merge(pop_ev_demographics[['ZIP Code','Make_decode','median_income','Median_commute']],df, on='ZIP Code', how='left')
    ev.rename(columns={0: "Total_EV"}, inplace = True)
    ev = ev[ev['median_income'].notnull()]

def nornmalize():
    ev2 = ev.copy()
    cols_to_norm = ['Median_commute','Total_EV']
    ev2[cols_to_norm] = StandardScaler().fit_transform(ev2[cols_to_norm])


def pearsonr_ci(x,y,alpha=0.05):
    ''' calculate Pearson correlation along with the confidence interval using scipy and numpy
    Parameters
    ----------
    x, y : iterable object such as a list or np.array
      Input for correlation calculation
    alpha : float
      Significance level. 0.05 by default
    Returns
    -------
    r : float
      Pearson's correlation coefficient
    pval : float
      The corresponding p value
    lo, hi : float
      The lower and upper bound of confidence intervals
    '''

    r, p = stats.pearsonr(x,y)
    r_z = np.arctanh(r)
    se = 1/np.sqrt(x.size-3)
    z = stats.norm.ppf(1-alpha/2)
    lo_z, hi_z = r_z-z*se, r_z+z*se
    lo, hi = np.tanh((lo_z, hi_z))
    return r, p, lo, hi

def plot():
    corr = ev.corr()

    %matplotlib inline

    plt.figure(figsize = (16,4))

    ax = sns.heatmap(corr, 
        xticklabels=corr.columns,
        yticklabels=corr.columns,
        annot=True)


pearsonr_ci(ev2['Median_commute'].values,ev2['Total_EV'].values)
pearsonr_ci(ev2['median_income'].values,ev2['Total_EV'].values)