### Importing:
from dotenv import load_dotenv
from datetime import datetime,date,timedelta

import os                 ###Basic 
import tweepy             ###Found as a simple twitter API
import pandas as pd       ###Dataframes
import numpy as np        ###Numbers
import requests           ###.env file 
import csv                ###Maybe put in CSV?

load_dotenv()

########SCRIPT-WIDE VARIABLES

##SECRET KEYS (.env)
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")

##DATE VARIABLES
todaydate = datetime.now().strftime('%Y-%m-%d')
yesterday = date.today() - timedelta(days=1)
yesterdaydate = yesterday.strftime('%Y-%m-%d')

####### API setup:
def twitter_setup():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

extractor = twitter_setup()

while True:
    try: 
        twitter_name = input('Enter a valid Twitter username: ')
    except: 
        print('error')
        continue


tweets = extractor.user_timeline(screen_name=twireatter_name, count=200)
print("Number of tweets extracted: {}.\n".format(len(tweets)))

print("5 recent tweets:\n")
for tweet in tweets[:5]:
    print(tweet.text)
    print()