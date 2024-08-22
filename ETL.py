
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError
import requests
import json
import csv
 
import pandas as pd
import tweepy 
import json
import logging
import os

from bs4 import BeautifulSoup

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

url = "https://www.cars.com/research/tesla-model_3-2018/consumer-reviews/?pg=1&nr=250"
url2 = "https://www.cars.com/research/nissan-leaf-2018/consumer-reviews/?pg=1&nr=50"

s3 = boto3.client('s3' ,region_name='us-west-2')

aws_secret_access_key

def download_ev_data(ev_data_tmp_path):
    response = requests.get('https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD')
    
    with open(ev_data_tmp_path, 'w') as f:
        writer = csv.writer(f)
        for line in response.iter_lines():
            writer.writerow(line.decode('utf-8').split(','))

def upload_file(file_path, bucket_name, object_name):
	s3.upload_file(file_path, bucket_name, object_name)


def connect_twitter_api():

    logger = logging.getLogger()

    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_KEY")
    access_token_secret = os.getenv("ACCESS_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)  
    
    tweets = api.user_timeline(screen_name="@GreenCarReports", 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
    
    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id
    while True:
        tweets = api.user_timeline(screen_name="@GreenCarReports", 
                               # 200 is the maximum allowed count
                               count=200,
                               include_rts = False,
                               max_id = oldest_id - 1,
                               # Necessary to keep full_text 
                               # otherwise only the first 140 words are extracted
                               tweet_mode = 'extended'
                               )
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)  
    
    return all_tweets

def tweets_to_df(all_tweets):
    #transform the tweepy tweets into a 2D array that will populate the csv	
    outtweets = [[tweet.id_str, 
                tweet.created_at, 
                tweet.favorite_count, 
                tweet.retweet_count, 
                tweet.full_text.encode("utf-8").decode("utf-8")] 
                for idx,tweet in enumerate(all_tweets)]
    df = pd.DataFrame(outtweets,columns=["id","created_at","favorite_count","retweet_count", "text"])
    df.to_csv('/tmp/tweets_by_green_cars.csv',index=False)



def web_scrapping_car_reviews(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    domains = soup.find_all("p", class_="review-card-text")

    list_reviews = []
    for domain in domains:
        list_reviews.append((domain.text.replace('\n','')).strip())
   
    filename= "/tmp/" + url.split('/')[4] +".csv"
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        for reviews in list_reviews:
            writer.writerow([reviews])


def setup():
    bucket_name = 'karen.bucket'
    
    ev_data_tmp_path = '/tmp/ev_data.csv'
    twitter_data_tmp_path = '/tmp/tweets_by_green_cars.csv'
    tesla_reviews_data_tmp_path = "/tmp/" + url.split('/')[4] +".csv"
    leaf_reviews_data_tmp_path = "/tmp/" + url2.split('/')[4] +".csv"
    
    download_ev_data(ev_data_tmp_path)
    print('download_ev_data')
    tweets_to_df(connect_twitter_api())
    print('tweets_to_df')
    web_scrapping_car_reviews(url)
    print('web_scrapping_car_reviews')
    web_scrapping_car_reviews(url2) 
    print('web_scrapping_car_reviews')
    
    upload_file(ev_data_tmp_path, bucket_name, 'json/ev_data.csv')
    print('upload_file_ev')
    upload_file(twitter_data_tmp_path, bucket_name, 'json/twitter_data.csv')
    upload_file(twitter_data_tmp_path, bucket_name, 'json/tesla_reviews_data.csv')
    upload_file(twitter_data_tmp_path, bucket_name, 'json/leaf_reviews_data.csv')

setup()
