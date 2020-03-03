
# Electric Vehicles in WA: Exploratory Data Analysis and NLP through Sentiment Analysis.

## Table of contents
- [Inspiration](#general-info)
- [Technologies](#technologies)
- [Hypothesis Testing](#hypotesis-testing)
- [Prediction Model](#prediction-model)
- [Exploratory Data Analysis](#exploratory-data-analysis)
  + [Top 3 Electric Vehicles by year](#exploratory-data-analysis)
  + [Why people are choosing Tesla and Nissan Leaf?](#why)
   * [@GreenCarReports Tweets Analysis](#twitter-analysis)
   * [Cars.com Buyer's Reviews Analysis](#web-scrapping-analysis)
- [Data Sources](#data-sources)


## Inspiration
There is 53,818 electric vehicles registered in WA state. This exploratory data analysis tries to understand This exploratory data analysis tries to understand E.V costumers and identify potential E.V buyers. To accomplish this, I needed to understand the EV most populated zip codes with their respective demographic data. I focus on household income level and commutes times: Does tend to own an electric car is correlated to how much a household earn and how much a household commute to work?


## Technologies and Data Sources
* S3, Boto3 
* Tweepy
* NLTK, TextBlob
* Numpy, Pandas, Scipy, Sklearn
* MatplotLib, Seaborn, Plotly

<img src="/visualizations/tech.png"/>

# Exploratory Data Analysis

## Electric Vehicles Population Map
<img src="/visualizations/scatterplotmap.png"/>
Click here to see this interactive map: https://karenlo08.github.io/Electric_Vehicles-in-WA/ (In case map doesn't show up refresh web browser)

## Top 3 WA Electric Vehicles by Year

<img src="/visualizations/top3.png"/>

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

<img src="/visualizations/correlation_table.png"/>

# Why people are choosing Tesla and Nissan Leaf? 
During my analysis I wanted to know why E.V drivers were choosing certain models over others and how were they reacting about their products through tweets and reviews. In this section, I web scrapped cars.com to obtain reviews from Tesla and Leaf, whom were the most popular E.V in WA. Also, I create a connector to Twitter API to get tweets from a @GreenCarsReports, an account where electric cars news are posted. The goal was recognize the polarity of the reviews, set a threshold and classify them in bad, good or neutral.

## @GreenCarReports Tweets Analysis

```
def detect_polarity(text):
    return TextBlob(text).sentiment.polarity

df['polarity'] = df['review'].apply(detect_polarity)
df['polarity_neutral'] = df['polarity'].apply(lambda x: True if ((x > 0)&(x<=0.1)) else False)
df['polarity_negative'] = df['polarity'].apply(lambda x: True if x <= 0 else False)
df['polarity_positive'] = df['polarity'].apply(lambda x: True if x > 0.1 else False)
df['blob'] = df['review'].apply(lambda x: TextBlob(x).noun_phrases)

cols = ['blob','polarity','polarity_negative','polarity_positive','polarity_neutral','review']
df = df[cols]
```
<img src="/visualizations/polarity.png"/>


## Cars.com Buyer's Reviews Analysis
### 2018 Tesla Model 3 Reviews
<img src="/visualizations/car__tesla_reviews_bar.png"/>

### 2018 Nissan Leaf Reviews
<img src="/visualizations/car__tesla_reviews_bar.png"/>

You can check here for more visualizations and my thinking process on Sentiment Analysis here: https://github.com/karenlo08/EV/blob/master/Sentiment_Analysis.ipynb

# Thanks for reading!
