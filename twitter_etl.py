import tweepy
import pandas as pd
import json
from datetime import datetime
import s3fs


def run_twitter_etl():

    access_key = "YvYF0WM91GP2JKa6PAOOBJh8S"
    access_secret = "0hFRNebQ3PpWtoGIfKqOfM3bm28AsBWeHmeFYHQcSW0deRWW7i"
    consumer_key = "1757258948069957633-tW16qFbEnuEYlcXwqz0dPCBwlmMPpz"
    consumer_secret = "X24bVeGrq9oTZeoEJdP0StO0dAw4YeW2fgz3JkdzLcbkq"

    # Twitter authentication
    auth = tweepy.OAuthHandler(access_key, access_secret)
    auth.set_access_token(consumer_key, consumer_secret)

    # # # Creating an API object
    api = tweepy.API(auth)
    tweets = api.user_timeline(
        screen_name="@elonmusk",
        # 200 is the maximum allowed count
        count=200,
        include_rts=False,
        # Necessary to keep full_text
        # otherwise only the first 140 words are extracted
        tweet_mode="extended",
    )

    list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {
            "user": tweet.user.screen_name,
            "text": text,
            "favorite_count": tweet.favorite_count,
            "retweet_count": tweet.retweet_count,
            "created_at": tweet.created_at,
        }

        list.append(refined_tweet)

    df = pd.DataFrame(list)
    df.to_csv("refined_tweets.csv")
