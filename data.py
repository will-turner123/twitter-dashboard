# TODO: Sentiment over time
# TODO: Sentiment after & during GME situation
# TODO: Volume of tweets

import twint
import nest_asyncio
import pandas as pd 
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import schedule

analyzer = SentimentIntensityAnalyzer()


# should we lemmatize?
# should we use something other than vader sentiment?
def sentiment_analysis(tweet):
    text = tweet
    sentiment = analyzer.polarity_scores(text)
    compound = sentiment["compound"]
    pos = sentiment["pos"]
    return compound


def return_tweet(user):
    nest_asyncio.apply()
    # Configure
    c = twint.Config()
    c.Search = f"{user}"
    c.To = f"{user}"
    c.Pandas = True
    c.User_full=True
    c.Limit = 1
    # Run
    twint.run.Search(c)
    tweets_df = twint.storage.panda.Tweets_df
    return tweets_df


def get_historic_tweets(user):
    nest_asyncio.apply()
    # Configure
    c = twint.Config()
    c.Search = f"{user}"
    c.To = f"{user}"
    c.Pandas = True
    c.User_full=True
    c.Since = '2021-01-01'
    c.Hide_output = True
    # Run
    twint.run.Search(c)
    tweets_df = twint.storage.panda.Tweets_df
    # oh god this is lazy
    data = {'date': [], 'id': [], 'username': [], 'name': [], 'tweet': [], 'sentiment': []}
    counter = 0
    for row in tweets_df.iterrows():
        tweet = tweets_df['tweet'].iloc[counter]
        date = tweets_df['date'].iloc[counter]
        id = tweets_df['id'].iloc[counter]
        name = tweets_df['name'].iloc[counter]
        username = tweets_df['username'].iloc[counter]
        compound = sentiment_analysis(tweet)
        data['date'].append(date)
        data['id'].append(id)
        data['username'].append(username)
        data['name'].append(name)
        data['tweet'].append(tweet)
        data['sentiment'].append(compound)
        print(f'Tweet {counter}')
        counter += 1
    df = pd.DataFrame(data)
    df.set_index('date', inplace=True)
    print(df.head())
    return df




# if the file for the broker does not exist,
# makes the file and gets historic tweets & writes it
# otherwise returns existing df
def handle_csv(broker):
    file_path = f'data/{broker}.csv'
    try:
        df = pd.read_csv(file_path, index_col='date')
        return df
    except FileNotFoundError:
        # data = {'date': [], 'id': [], 'username': [], 'name': [], 'tweet': [], 'sentiment': []}
        # df = pd.DataFrame(data)
        # df.set_index('date', inplace=True)
        df = get_historic_tweets(broker)
        df.to_csv(file_path)
        return df


def main():
    # twitter usernames we're scraping
    brokers = ["RobinhoodApp", "etrade", "Fidelity", "TDAmeritrade", "MerrillEdge"]
    for broker in brokers:
        df = handle_csv(broker)
        # should probs be 0 instead of -1
        # maybe sort values just in case
        last_tweet = return_tweet(broker)
        tweet = last_tweet['tweet'].iloc[-1]
        date = last_tweet['date'].iloc[-1]
        id = last_tweet['id'].iloc[-1]
        name = last_tweet['name'].iloc[-1]
        username = last_tweet['username'].iloc[-1]
        compound = sentiment_analysis(tweet)

        # username, name, tweet, compound sentiment
        data = {'date': [date], 'id': [id], 'username': [username], 'name': [name], 'tweet': [tweet], 'sentiment': [compound]}
        data = pd.DataFrame(data).set_index('date')
        # if the tweet id is not in past tweets
        if int(id) not in list(df.id.unique()):
            df = df.append(data)
        df.to_csv(f'data/{broker}.csv')


schedule.every(10).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(30)