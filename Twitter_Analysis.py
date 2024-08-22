from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 

from wordcloud import WordCloud
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

import pandas as pd
pd.set_option('display.max_colwidth', -1)
    
def detect_polarity(text):
    return TextBlob(text).sentiment.polarity
    
def get_df_with_car_reviews(url):
    
    filename= "/tmp/" + url.split('/')[4] +".csv"
    df = pd.read_csv(filename,names=['review'], header=None)
    df['polarity'] = df['review'].apply(detect_polarity)
    df['polarity_neutral'] = df['polarity'].apply(lambda x: True if ((x > 0)&(x<=0.1)) else False)
    df['polarity_negative'] = df['polarity'].apply(lambda x: True if x <= 0 else False)
    df['polarity_positive'] = df['polarity'].apply(lambda x: True if x > 0.1 else False)
    df['blob'] = df['review'].apply(lambda x: TextBlob(x).noun_phrases)

    cols = ['blob','polarity','polarity_negative','polarity_positive','polarity_neutral','review']
    df = df[cols] 
    return df


def df_to_list(df):
    nouns_tesla = []
    for index,row in df.iterrows():
        nouns_tesla.extend(row['blob'])    
    return nouns_tesla


def filter_words(text):
    if( 'tesla' in text or 'model' in text or "n't" in text or 'car' in text or 'bmw' in text
    or 'vehicle' in text or 'great' in text or 'leaf' in text or 'nissan' in text):
        return ''
    else:
        return text

def word_cloud(wd_list):
    wave_mask = np.array(Image.open("desktop/cloud.jpg"))
    stop_words = set(stopwords.words("english"))
    all_words = ' '.join([filter_words(text) for text in wd_list])
    wordcloud = WordCloud(
        mask=wave_mask,
        background_color='white',
        stopwords=stop_words,
        max_font_size=200).generate(all_words)
    plt.figure(figsize=(12, 10))
    plt.axis('off')
    plt.imshow(wordcloud, interpolation="bilinear")

def main():
    df = get_df_with_car_reviews(url)
    df2 = get_df_with_car_reviews(url2)

    wordcloud_list1 = df_to_list(df)
    wordcloud_list2 = df_to_list(df2)

    word_cloud(wordcloud_list1)
    word_cloud(wordcloud_list2)


if __name__ == '__main__':
    main()
    
