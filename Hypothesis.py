from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats 
import pandas as pd
import numpy as np
%matplotlib inline


zip_codes_2017_5yr_commute = pd.read_csv('documents/ev2/zip_codes_2017_5yr_commute.csv')
zip_codes_2017_5yr_commute.rename(columns={"geo_id": "ZIP Code"}, inplace = True)

pop_ev = pd.read_csv('documents/ev2/Electric_Vehicle_Population_Data.csv')
pop_ev_demographics = pd.merge(pop_ev,zip_codes_2017_5yr_commute, on='ZIP Code', how='left')

def calculate_median_commute():
    median =(zip_codes_2017_5yr_commute['commute_10_14_mins'].apply(lambda x:x * [1] if x>0 else [0]) + 
    zip_codes_2017_5yr_commute['commute_15_19_mins'].apply(lambda x:x * [2] if x>0 else [0]) +
    zip_codes_2017_5yr_commute['commute_20_24_mins'].apply(lambda x:x * [3] if x>0 else [0]) +
    zip_codes_2017_5yr_commute['commute_25_29_mins'].apply(lambda x:x * [4] if x>0 else [0]) +
    zip_codes_2017_5yr_commute['commute_30_34_mins'].apply(lambda x:x * [5] if x>0 else [0]) +     
    zip_codes_2017_5yr_commute['commute_45_59_mins'].apply(lambda x:x * [6] if x>0 else [0]) ).apply(np.mean).astype(int)
    
    pop_ev_demographics['Median_commute'] = median
    #Reference
    #commute_dict = {1:'commute_10_14_mins',2:'commute_15_19_mins',3:'commute_20_24_mins',4:'commute_25_29_mins',5:'commute_30_34_mins',6:'commute_45_59_mins'}
    
    
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
    ev = ev[ev['Median_commute'].notnull()]
    return ev

def normalize(df,column):
    cols_to_norm = [column,'Total_EV']
    df[cols_to_norm] = StandardScaler().fit_transform(df[cols_to_norm])
    return df


def pearsonr_ci(x,y,alpha=0.05):
    r, p = stats.pearsonr(x,y)
    r_z = np.arctanh(r)
    se = 1/np.sqrt(x.size-3)
    z = stats.norm.ppf(1-alpha/2)
    lo_z, hi_z = r_z-z*se, r_z+z*se
    lo, hi = np.tanh((lo_z, hi_z))
    return r, p, lo, hi

def plot(df):
    corr = ev.corr()
    plt.figure(figsize = (16,4))
    ax = sns.heatmap(corr, 
        xticklabels=corr.columns,
        yticklabels=corr.columns,
        annot=True)

def main():
    calculate_median_commute()
    decode_make()
    ev = columns_to_correlate() 
    Median_commute_norm = normalize(ev,'Median_commute')
    median_income_norm = normalize(ev,'median_income')
    pearsonr_ci(Median_commute_norm['Median_commute'].values,Median_commute_norm['Total_EV'].values)
    pearsonr_ci(median_income_norm['median_income'].values,median_income_norm['Total_EV'].values)
    plot(ev)


if __name__ == '__main__':
    main()

