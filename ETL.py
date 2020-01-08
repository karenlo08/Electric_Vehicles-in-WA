
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError
import requests
import json
import csv

#from __future__ import unicode_literals
import pandas as pd
import tweepy 
import json
import logging
import os

access_key_id = 'AKIAIAS55T2BVOAPKADQ'
secret_access_key = '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'

s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-west-2')

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



def setup():
    bucket_name = 'karen.bucket'
    
    ev_data_tmp_path = '/tmp/ev_data.csv'
    twitter_data_tmp_path = '/tmp/tweets_by_green_cars.csv'
    
    download_ev_data(ev_data_tmp_path)
    tweets_to_df(connect_twitter_api())#check
    
    upload_file(ev_data_tmp_path, bucket_name, 'json/ev_data.csv')
    upload_file(twitter_data_tmp_path, bucket_name, 'json/twitter_data.csv')

setup()
