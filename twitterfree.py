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

#Annoying hour timerange classifier - had to make super long because couldn't figure out >=/<= issue in pandas dtype
#https://stackoverflow.com/questions/30953299/pandas-if-row-in-column-a-contains-x-write-y-to-row-in-column-b
def applyFunc(hourposted):
    if hourposted == 0:
        return 'Late Night'
    elif hourposted == 1:
        return 'Late Night'
    elif hourposted == 2:
        return 'Late Night'
    elif hourposted == 3:
        return 'Late Night'
    elif hourposted == 4:
        return 'Late Night'
    
    elif hourposted == 5:
        return 'Early Morning'
    elif hourposted == 6:
        return 'Early Morning'
    elif hourposted == 7:
        return 'Early Morning'
    elif hourposted == 8:
        return 'Early Morning'
    
    elif hourposted == 9:
        return 'Late Morning'
    elif hourposted == 10:
        return 'Late Morning'
    elif hourposted == 11:
        return 'Late Morning'
    
    elif hourposted == 12:
        return 'Early Afternoon'
    elif hourposted == 13:
        return 'Early Afternoon'
    elif hourposted == 14:
        return 'Early Afternoon'
    
    elif hourposted == 15:
        return 'Late Afternoon'
    elif hourposted == 16:
        return 'Late Afternoon'
    elif hourposted == 17:
        return 'Late Afternoon'
    
    elif hourposted == 18:
        return 'Early Evening'
    elif hourposted == 19:
        return 'Early Evening'
    elif hourposted == 20:
        return 'Early Evening'

    elif hourposted == 21:
        return 'Late Evening'
    elif hourposted == 22:
        return 'Late Evening'
    elif hourposted == 23:
        return 'Late Evening'

    else:
        return 'No Timestamp'



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
lastweek = date.today() - timedelta(days=7)
lastweekdate = lastweek.strftime('%Y-%m-%d')



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
tdf['tweet_timerange'] = tdf['tweet_hour']
tdf['tweet_timerange'] = tdf['tweet_timerange'].apply(applyFunc)


#calculations
avg_tweet_length = np.average(tdf['tweet_length'])
most_tweets_on = np.max(tdf['tweet_date'])
number_max_tweets = len(tdf.loc[(tdf['tweet_date']==np.max(tdf['tweet_date'])),:])
percent_capslock = "{:.1f}".format(sum(map(str.isupper,str([i for i in tdf['tweet']]).split()))/len(str([i for i in tdf['tweet']]).split())*100)
fully_capslock_tweet = sum([i.isupper() for i in tdf['tweet']])

#Date Diff
first_tweet = min(tdf['tweet_date'])
last_tweet = max(tdf['tweet_date'])
delta = (last_tweet - first_tweet).days

#Count Tables/Data
retweet_most_tweet = tdf.sort_values('retweet_count', ascending=False)[:1]['tweet'].values[0]
retweet_most_date = tdf.sort_values('retweet_count', ascending=False)[:1]['tweet_date'].values[0]
retweet_most_retweets = add_commas(tdf.sort_values('retweet_count', ascending=False)[:1]['retweet_count'].values[0])
likes_most_tweet = tdf.sort_values('likes', ascending=False)[:1]['tweet'].values[0]
likes_most_date = tdf.sort_values('likes', ascending=False)[:1]['tweet_date'].values[0]
likes_most_retweets = add_commas(tdf.sort_values('likes', ascending=False)[:1]['likes'].values[0])


table_most_frequent_day = tdf.groupby(['tweet_day'], as_index=False).agg({
    "id":np.count_nonzero,
    "likes":np.sum,
    "retweet_count":np.sum
    }).sort_values('id',ascending=False).rename({'id':'count'},axis='columns')
    
most_frequent_day = table_most_frequent_day[:1]['tweet_day'].values[0]

#append a hashtag if source = hashtag
if source == 'hashtag':
    selected_name = '#'+selected_name

### {# of tweets extracted -> from X to Y [Z Days]}
print(f'Data from {first_tweet} to {last_tweet} ({delta} days).')
print()
print('-----------------------------------')
print('-----------------------------------')

####RESULTS
print(f'Average Tweet length: {"{:.1f}".format(avg_tweet_length)} characters.')
print(f'Most Tweets on: {most_tweets_on} for a total of {number_max_tweets} tweets.')
print(f'Most retweeted: "{retweet_most_tweet}" with {retweet_most_retweets} retweets (posted on {retweet_most_date}).')
print(f'Most liked: "{likes_most_tweet}" with {likes_most_retweets} likes (posted on {likes_most_date}).')

print('-----------------------------------')
print(f"{fully_capslock_tweet} of {selected_name} {len(tdf)} Tweets were written entirely in ALL CAPS!")
print(f"{percent_capslock}% of {selected_name}'s individual words were ALL CAPS!")

print('-----------------------------------')
print("Primary source of tweets:")
print(tdf.groupby(['source'],as_index=False)[['id']].count().sort_values('id',ascending=False).rename({'id':'count'},axis='columns').to_string(index=False)) ## Remove to_string for DF

print('-----------------------------------')
print(f"{most_frequent_day} is {selected_name}'s most frequent day for Tweets.")
print(table_most_frequent_day.to_string(index=False)) ## Remove to_string for DF
