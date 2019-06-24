### Importing:
from dotenv import load_dotenv
from datetime import datetime,date,timedelta

import os                 ###Basic 
import tweepy             ###Found as a simple twitter API
import pandas as pd       ###Dataframes
import numpy as np        ###Numbers
import requests           ###.env file 
import csv                ###Maybe put in CSV?

import matplotlib.pyplot as plt  #plotting
import nltk                      #NLP
import string
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer 
from nltk.stem.wordnet import WordNetLemmatizer 
from nltk.tag import pos_tag
from nltk import FreqDist
from nltk.corpus import stopwords
from wordcloud import WordCloud
from textblob import TextBlob
import re


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

def clean_data(tokens, stop_words = ()):  #https://www.sitepoint.com/natural-language-processing-python/

    cleaned_tokens = []

    for token, tag in pos_tag(tokens):
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if token not in string.punctuation and token.lower() not in stop_words and "//" not in token.lower():
            cleaned_tokens.append(token)
    return cleaned_tokens



########SCRIPT-WIDE VARIABLES

##SECRET KEYS (.env)
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")

###DATE VARIABLES
todaydate = datetime.today().strftime('%Y-%m-%d')
yesterday = date.today() - timedelta(days=1)
yesterdaydate = yesterday.strftime('%Y-%m-%d')
lastweek = date.today() - timedelta(days=7)
lastweekdate = lastweek.strftime('%Y-%m-%d')


###NLP TEXT CLEANUP
lem = WordNetLemmatizer()
stemmer = PorterStemmer()
stop_words = stopwords.words('english')
# Additional stop_words are appended below (after user-input) following observations


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
    selected_name = input('Please enter a valid Twitter username: ')
    #selected_name = 'realDonaldTrump'

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
try: 
    tdf = pd.DataFrame(results)
except: 
    print('API Error: Only 1 result returned. Please re-run the program.')
    quit()

if len(tdf)<3:
    print('API Error: Only 1 result returned. Please re-run the program.')
    quit()


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
#Convert tweeted_at to Eastern
tdf['tweeted_at'] = tdf['tweeted_at'].dt.tz_localize('UTC')
tdf['tweeted_at'] = tdf['tweeted_at'].dt.tz_convert('US/Eastern')
# Add additional fields
tdf['tweet_date'] = tdf['tweeted_at'].dt.date
tdf['tweet_day'] = tdf['tweeted_at'].dt.weekday_name
tdf['tweet_hour'] = tdf['tweeted_at'].dt.hour
tdf['tweet_length'] = [len(tweets) for tweets in tdf['tweet']]
tdf['tweet_timerange'] = tdf['tweet_hour']
tdf['tweet_timerange'] = tdf['tweet_timerange'].apply(applyFunc)
#tdf['tweet_split'] = tdf['tweet'].str.strip('()').str.split(',')
tdf['tokenized_tweets'] = tdf.apply(lambda row: word_tokenize(row['tweet']), axis=1) #tokenized tweets
tdf['cleaned_tweets'] = tdf.apply(lambda row: clean_data(row['tokenized_tweets'],stop_words=stop_words), axis=1) #cleanedtweets
tdf['cleaned_tweets'] = tdf['cleaned_tweets'].apply(', '.join)


#calculations
avg_tweet_length = np.average(tdf['tweet_length'])
most_tweets_on = np.max(tdf['tweet_date'])
number_max_tweets = len(tdf.loc[(tdf['tweet_date']==np.max(tdf['tweet_date'])),:])
try: 
    percent_capslock = "{:.1f}".format(sum(map(str.isupper,str([i for i in tdf['tweet']]).split()))/len(str([i for i in tdf['tweet']]).split())*100)
except:
    percent_capsolock = "N/A"
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

table_most_frequent_hour = tdf.groupby(['tweet_timerange'], as_index=False).agg({
    "id":np.count_nonzero,
    }).sort_values('id',ascending=False).rename({'id':'count'},axis='columns')
most_frequent_hour = table_most_frequent_hour[:1]['tweet_timerange'].values[0]

#ThisWeek Dataframe
thisweek_tdf = tdf.loc[(tdf['tweeted_at']<=todaydate) & (tdf['tweeted_at']>=lastweekdate),:]

#Text of all tweets
text = ' '.join(tdf['tweet'].tolist()).lower()

#Text of this week tweets
thisweek_text = ' '.join(thisweek_tdf['tweet'].tolist()).lower()

####NLP ADDITIONAL WORDS AND CLEANING

#Append more stop_words for distribution
stop_words.append(f"{selected_name.lower()}")
other_stop_words = ['rt',"..." , "http", "'", "...", '"' '"' "rt", "amp", '”', '“', "'s", "''", "n't", 'n"t', '’', '', '``', "get", "go", "https", "''",'co','.co','co','‘','//t.co/']
stop_words = stop_words+other_stop_words

#NLP Cleaning
tokens = word_tokenize(text)
cleaned_tokens = clean_data(tokens, stop_words = stop_words)
freq_dist = FreqDist(cleaned_tokens)
top_twenty_words = pd.DataFrame(freq_dist.most_common(10)).rename({0:'word',1:'count'},axis='columns')
cleaned_text = ' '.join(cleaned_tokens).lower()


#sentiment analysis #https://www.kaggle.com/ankkur13/sentiment-analysis-nlp-wordcloud-textblob
bloblist_desc = list()

tdf_cleaned_string=tdf['cleaned_tweets']
for row in tdf_cleaned_string:
    blob = TextBlob(row)
    bloblist_desc.append((row,blob.sentiment.polarity, blob.sentiment.subjectivity))
    tdf_cleaned_string_desc = pd.DataFrame(bloblist_desc, columns = ['sentence','sentiment','polarity'])
 
def f(tdf_cleaned_string_desc):
    if tdf_cleaned_string_desc['sentiment'] > 0:
        val = "Positive"
    elif tdf_cleaned_string_desc['sentiment'] == 0:
        val = "Neutral"
    else:
        val = "Negative"
    return val

tdf_cleaned_string_desc['sentiment_type'] = tdf_cleaned_string_desc.apply(f, axis=1)
tdf_sentiments = tdf_cleaned_string_desc.groupby(['sentiment_type'],as_index=False)['sentence'].count()
tdf_sentiments = tdf_sentiments.rename({'sentence':'count'},axis='columns').sort_values('count',ascending=False).reset_index(drop=True)
try: 
    to_val = tdf_sentiments['count'][:1]/np.sum(tdf_sentiments['count'])*100
    percent_top_sentiment = "{:.1f}".format(to_val.values[0])
except: 
    percent_top_sentiment = 'N/A'


#append a hashtag if source = hashtag
if source == 'hashtag':
    selected_name = '#'+selected_name

### {# of tweets extracted -> from X to Y [Z Days]}
if len(thisweek_tdf) > 1:
    print(f"{len(thisweek_tdf)} Tweets this week")
print(f'Data from {first_tweet} to {last_tweet} ({delta} days).')
print("")
print('-----------------------------------')
print('-----------------------------------')
print("")

####RESULTS
print(f'Average Tweet length: {"{:.1f}".format(avg_tweet_length)} characters.')
try:
    print(f"Average Tweets Per Day: {'{:.1f}'.format(len(tdf)/delta)}.")
except:
    pass
print(f'Most Tweets on: {most_tweets_on} for a total of {number_max_tweets} tweets.')
print(f'Most retweeted: "{retweet_most_tweet}" with {retweet_most_retweets} retweets (posted on {retweet_most_date}).')
print(f'Most liked: "{likes_most_tweet}" with {likes_most_retweets} likes (posted on {likes_most_date}).')
print("")
print('-----------------------------------')

print("")
print("Primary source of tweets:")
print(tdf.groupby(['source'],as_index=False)[['id']].count().sort_values('id',ascending=False).rename({'id':'count'},axis='columns').to_string(index=False)) ## Remove to_string for DF
print("")
print('-----------------------------------')

print("")
print(f"Most Frequent Day to Tweet: {most_frequent_day}")
print("")
print(table_most_frequent_day.to_string(index=False)) ## Remove to_string for DF
print("")
print('-----------------------------------')

print("")
print(f"Most Frequent Time of Day to Tweet: {most_frequent_hour}")
print(f"{len(tdf.loc[(tdf['tweet_hour']>=0) & (tdf['tweet_hour']<5),:][['id']])/len(tdf)*100}% of {selected_name} Tweets happen from 12am-4am EST.")
print("")
print(table_most_frequent_hour.to_string(index=False)) ## Remove to_string for DF
print("")
print('-----------------------------------')

print("")
print(f"Tweets written entirely in ALL CAPS: {fully_capslock_tweet} of {len(tdf)}")
print(f"Individual words written in ALL CAPS: {percent_capslock}%")
print(f"Tweets with one excalamation mark: {sum(tdf.tweet.str.count('!'))}! Tweets with two exclamation marks: {sum(tdf.tweet.str.count('!!'))}!!  Exciting!!!")
print(f"Top 10 Words by Frequency for {selected_name}:")
print("")
print(top_twenty_words.to_string(index=False))
print("")
print('-----------------------------------')
print('-----------------------------------')
print("")
print(f"{selected_name.upper()} TWEETS ARE GENERALLY{tdf_sentiments['sentiment_type'][:1].to_string(index=False).upper()} ({percent_top_sentiment}%).")
print("")
print(tdf_sentiments.to_string(index=False).upper())
print('-----------------------------------')
print('-----------------------------------')


# ## BAR OF TOP 20

# import matplotlib.pyplot as plt
# import statsmodels.formula.api as smf
# fig, ax = plt.subplots()
# top_twenty_words.groupby(['word'])[['count']].sum().sort_values(['count'],ascending=False).plot(kind='bar', 
#                   ax=ax, 
#                   figsize=(13,6), 
#                   color=['mediumblue','red','pink'],
#                   alpha=.8
#                  #ylim=(200,600)                            
#                  )

# ax.set_title(f'{selected_name}: Top 20 Words by Frequency',
#              size=20)
# # #ax.get_children()[list(ytcatcount.index).index('Entertainment')].set_color('dimgrey')

# # Tufte-like axes
# ax.spines['left'].set_position(('outward', 10))
# ax.spines['bottom'].set_position(('outward', 10))
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
# ax.yaxis.set_ticks_position('left')
# ax.xaxis.set_ticks_position('bottom')
# ax.set_ylabel('Count',size=10)
# ax.set_xlabel('Word',size=10)
# plt.xticks(rotation=90)


# ##WORDCLOUD
# wordcloud = WordCloud(width=1000, height=1000, margin=0).generate(cleaned_text)
 
# # Display the generated image:
# plt.figure( figsize=(20,10) )
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.margins(x=0, y=0)
# plt.show()

# ##Sentiment Plot
# tdf_cleaned_string_desc.groupby(['sentiment_type'],as_index=True)['sentence'].count().plot(kind='bar');