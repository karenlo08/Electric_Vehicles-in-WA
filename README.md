
# Electric Vehicles in WA

## Table of contents
- [Inspiration](#general-info)
- [Hypothesis Testing](#hypotesis-testing)
- [Prediction Model](#prediction-model)
- [Exploratory Data Analysis](#exploratory-data-analysis)
  + [Top 3 Electric Vehicles by year](#exploratory-data-analysis)
  + [Why people are choosing Tesla and Nissan Leaf?](#why)
   * [@GreenCarReports Tweets Analysis](#twitter-analysis)
   * [Cars.com Buyer's Reviews Analysis](#web-scrapping-analysis)
- [Data Sources](#data-sources)
- [Technologies](#technologies)
- [Setup](#setup)

## Inspiration
This project is simple Lorem ipsum dolor generator.

## Technologies
* S3
* Boto3
* Numpy, Pandas, Scipy, Sklearn
* MatplotLib, Seaborn, Plotly
* Tweepy

## Hypothesis Testing
#### Does a higher income or lower income relates to having more or less electric cars?  Higher commutes times can be a contribuitor to buy a electric car?


```
H0: There is no statiscally significant relationship between household income level/commute times and the number of electric vehicles by zip code.
HA: There is a statiscally significant relationship between household income level/commute times and the number of electric vehicles by zip code.
Significance level: 0.05
```

Normalize the median income data/median commute time and total E.V. population data to be comparable between each other.


```python
def normalize(df,column):
    cols_to_norm = [column,'Total_EV']
    df[cols_to_norm] = StandardScaler().fit_transform(df[cols_to_norm])
    return df
```


```python
median_income_norm = normalize(ev,'median_income')
median_commute_norm = normalize(ev,'Median_commute')
print(median_income_norm[:3])
print(median_commute_norm[:3])
```

       ZIP Code  Make_decode  median_income  Median_commute  Total_EV
    0     98107            0       0.032427        0.372514 -0.140544
    1     98370            1      -0.246282       -1.776191 -0.478660
    2     98360            2      -0.029047        0.372514 -1.056531
       ZIP Code  Make_decode  median_income  Median_commute  Total_EV
    0     98107            0       0.032427        0.372514 -0.140544
    1     98370            1      -0.246282       -1.776191 -0.478660
    2     98360            2      -0.029047        0.372514 -1.056531


Next, calculate a Pearson correlation coefficient and the p-value for testing non-correlation.


```python
def pearsonr(x,y,alpha=0.05):
    r, p = stats.pearsonr(x,y)
    return r,p
```


```python
print(pearsonr(median_income_norm['median_income'].values,median_income_norm['Total_EV'].values))
print(pearsonr(median_income_norm['Median_commute'].values,median_income_norm['Total_EV'].values))
```

    (0.59373613499395383, 3.7922998932025516e-58)
    (-0.0034307164978868562, 0.93333529849276775)


1. The coefficient 0.6 shows a strong correlation and the p-value is less than 0.05, so we reject the null hypothesis and aprove the alternative where there is s a statiscally significant relationship between household income level and the number of electric vehicles by zip code.

2. There is a weak negative correlation between commute times and getting an electric car. Also, the p-value is greater than our alpha, so we fail to reject the Null hypothesis.

<img src="/visualizations/correlation.jpg"/>

## Prediction Model

<img src="/visualizations/prediction.jpng"/>

# Exploratory Data Analysis
## Top 3 WA Electric Vehicles by Year

<img src="/visualizations/pie1.png"/>
<img src="/visualizations/pie2.png"/>
<img src="/visualizations/pie3.png"/>
<img src="/visualizations/pie.png"/>

## Why people are choosing Tesla and Nissan Leaf? 

### Cars.com Buyer's Reviews Analysis

2018 Tesla Model 3 Reviews


<img src="/visualizations/leaf_review.png"/>
<img src="/visualizations/pie1_tesla.png"/>

2018 Nissan Leaf Reviews

<img src="/visualizations/tesla_review.png"/>
<img src="/visualizations/pie1_leaf.png"/>

### @GreenCarReports Tweets Analysis

<img src="/visualizations/gree_cars_review.png"/>
