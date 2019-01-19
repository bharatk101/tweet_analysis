# Gather tweets from twitter for article 13 effect on youtube
import tweepy
import pandas as pd
from textblob import TextBlob
from requests.exceptions import Timeout, ConnectionError
from requests.packages.urllib3.exceptions import ReadTimeoutError

# consumer key and access toke from twitter developer account
consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

# access twitter using OAuthHandler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# Polarity function
def get_polarity(analysis):
    if analysis.sentiment[0] == 0:
        return 'Netural'
    elif analysis.sentiment[0] > 0:
        return 'Positive'
    else:
        return 'Negative'

# subjectivity function
def get_subjectivity(analysis):
    if analysis.sentiment[1] < 0.5:
        return 'Objective'
    else:
        return 'Subjective'


# list to hold all the values
df_list = []

#function to get the tweets based on query
def get_tweets(query):
    try:
        for tweet in tweepy.Cursor(api.search, q = query + '-filter:retweets',
        lang='en', wait_on_rate_limit = True,
        wait_on_rate_limit_notify = True, count = 10000).items(10000):
            id = tweet.id_str
            text = tweet.text
            analysis = TextBlob(text)
            polarity_value = analysis.sentiment[0]
            subjectivity_value = analysis.sentiment[1]
            likes = tweet.favorite_count
            retweets = tweet.retweet_count
            date = tweet.created_at
            polarity = get_polarity(analysis)
            subjectivity = get_subjectivity(analysis)
            source = tweet.source
            place = tweet.place,
            name = tweet.user.name
            # append the values in the list
            df_list.append({'id': str(id),
                             'text' : str(text),
                            'polarity_value' : round(polarity_value, 2),
                            'subjectivity_value' : round(subjectivity_value, 2),
                            'polarity' : polarity,
                            'subjectivity' :subjectivity,
                            'name' : name,
                            'likes' : likes,
                            'retweets' : retweets,
                            'date' : date,
                            'source' : source
                            })
    # exceptions that might occur
    except tweepy.TweepError as e:
        print(e.reason)
    except (Timeout, ssl.SSLError, ReadTimeoutError, ConnectionError) as exc:
        print('Timeout')

# call function get_tweets()
get_tweets('#Article13')
get_tweets('#SaveYourInternet')
get_tweets('#Article11')
get_tweets('#SaveTheInternet')

# convert the list to a DataFrame
tweet_details = pd.DataFrame(df_list, columns = ['id', 'text', 'polarity_value',
 'subjectivity_value', 'polarity', 'subjectivity', 'name', 'likes', 'retweets',
 'date', 'source'])

# save the DataFrame to a csv file
tweet_details.to_csv('tweets.csv', encoding = 'utf-8')
