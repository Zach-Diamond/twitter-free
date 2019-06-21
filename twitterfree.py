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

###FUNCTIONS
def add_commas(my_number):
    return "{:,}".format(my_number)


########SCRIPT-WIDE VARIABLES

##SECRET KEYS (.env)
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")

###DATE VARIABLES
todaydate = datetime.now().strftime('%Y-%m-%d')
yesterday = date.today() - timedelta(days=1)
yesterdaydate = yesterday.strftime('%Y-%m-%d')

###RESULT LISTS
results=[]

##AUTHENTICATING API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

print('-----------------------------------')
print('INITIATING SUPER ADVANCED TWITTER BOT...')
print('...CALCULATING...')
print('...PERFORMING BASIC ADDITION...')
print('...7+3= UNKNOWN...')
print('...9--NO, WAIT, 10...')
print('...CONFIGURING...')
print('...LEARNING SPANISH...')
print('---- CONFIGURATION COMPLETE ----')
print('-----------------------------------')

###CHOOSE LOOKUP TYP
viable=['hashtag','user']
source = input('To begin, please type either HASHTAG or USER: ').lower()
while source not in viable or len(source)==0:
    source = input('INVALID ENTRY, please type either HASHTAG or USER: ').lower()
else: 
    pass


########## USERS ############
if source == 'user':
    #####USER INPUT FOR TWITTER NAME
    #selected_name = input('Please enter a valid Twitter username: ')
    selected_name = 'realDonaldTrump'

    for i in range(10): # https://stackoverflow.com/questions/2083987/how-to-retry-after-exception
        try:
            tweets = api.user_timeline(screen_name=selected_name, tweet_mode='extended', count=200)
        except:
            selected_name = input('User not found. Please Enter a valid Twitter username: ')
        else:
            break
    else:
        print("No valid user names entered. Exiting program.")

    user = api.get_user(selected_name)

    print('-----------------------------------')
    print('-----------------------------------')
    print(f'Username Entered: {user.screen_name}')
    print(f'Follower Count: {add_commas(user.followers_count)}')
    for tweet in tweets:
        results.append(tweet.full_text)


########## HASHTAGS ############
else:
    selected_name = input('Please enter a valid Hashtag to search: ')
    #selected_name == 'Trump'

    for i in range(10): #Allow 10 retries
        try:
           tweets = tweepy.Cursor(api.search, q=f'{selected_name} -filter:retweets', tweet_mode='extended', lang='en').items(200)
        except:
            selected_name = input('Hashtag not found. Please Enter a valid hashtag: ')
        else:
            break
    else:
        print("No valid user names entered. Exiting program.")

    print('-----------------------------------')
    print('-----------------------------------')
    print(f'Hashtag Entered: {selected_name}')  
    for tweet in tweets:
        results.append(([tweet.full_text,tweet.id,tweet.source,
        tweet.retweeted,tweet.retweet_count,tweet.in_reply_to_screen_name,
        tweet.favorited,tweet.favorite_count,tweet.created_at]))
        #print(tweet.full_text)


#CREATING DATAFRAME
tdf = pd.DataFrame(results)
print("Number of tweets extracted: {}.\n".format(len(tdf)))
print('-----------------------------------')

###ADDING COLUMNS FROM TWITTER DATA
if source == 'user':
    tdf = tdf.rename({0:'tweet'},axis='columns')
    tdf['id'] = np.array([tweet.id for tweet in tweets])
    tdf['source'] = np.array([tweet.source for tweet in tweets])
    tdf['retweeted'] = np.array([tweet.retweeted for tweet in tweets])
    tdf['retweet_count'] = np.array([tweet.retweet_count for tweet in tweets])
    tdf['reply_to_user'] = np.array([tweet.in_reply_to_screen_name for tweet in tweets])
    tdf['liked'] = np.array([tweet.favorited for tweet in tweets])
    tdf['likes'] = np.array([tweet.favorite_count for tweet in tweets])
    tdf['tweeted_at'] = np.array([tweet.created_at for tweet in tweets])
else:
    tdf = tdf.rename({
    0:"tweet",
    1:"id",
    2:"source",
    3:"retweeted",
    4:"retweet_count",
    5:"reply_to_user",
    6:"liked",
    7:"likes",
    8:"tweeted_at"}
    , axis='columns')

#Additional columns
tdf['tweet_date'] = tdf['tweeted_at'].dt.date
tdf['tweet_day'] = tdf['tweeted_at'].dt.weekday_name
tdf['tweet_hour'] = tdf['tweeted_at'].dt.hour
tdf['tweet_length'] = [len(tweets) for tweets in tdf['tweet']]

#calculations
avg_tweet_length = np.average(tdf['tweet_length'])
most_tweets_on = np.max(tdf['tweet_date'])
number_max_tweets = len(tdf.loc[(tdf['tweet_date']==np.max(tdf['tweet_date'])),:])
most_frequent_day = np.max(tdf['tweet_day'])

#append a hashtag if source = hashtag
if source == 'hashtag':
    selected_name = '#'+selected_name

####RESULTS
print(f'Average Tweet length: {avg_tweet_length}')
print(f'Most Tweets on: {most_tweets_on} for a total of {number_max_tweets}')
print(f"{most_frequent_day} is {selected_name}'s most frequent day for Tweets.")
print("Primary source of tweets:")
print(tdf.groupby(['source'],as_index=False)[['id']].count().sort_values('id',ascending=False))