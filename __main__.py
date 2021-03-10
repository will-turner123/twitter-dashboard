from flask import Flask
import pandas as pd
import numpy as numpy
from flask import render_template
import os
import logging
from logging import Logger
from flask import jsonify
from flask import request
from datetime import datetime
import json


app = Flask(__name__)

def rank_brokers():
    ranks = {}
    rank_list = []
    for file in os.listdir('data'):
        f_path = 'data/' + file
        broker_name = file.replace('.csv', '')
        df = pd.read_csv(f_path, index_col='date', parse_dates=True, infer_datetime_format=True)
        ranks[broker_name] = df['sentiment'].sum()
        rank_list.append((df['sentiment'].sum(), broker_name))
    sort = sorted(rank_list, reverse=True)
    ranks = {}
    counter = 1
    for thing in sort:
        sentiment_score = thing[0]
        name = thing[1]
        ranks[counter] = {'name': name, 'sentiment': sentiment_score}
        counter += 1
    return ranks
    


@app.route('/data')
def read_data():
    broker = request.args.get('broker')
    df = pd.read_csv(f'data/{broker}.csv', index_col='date', parse_dates=True, infer_datetime_format=True)
    # data for sentiment over time, volume of tweets
    # highest sentiment tweet text & username
    # lowewst sentiment tweet text & user
    # 10 most recent positive tweets
    # 10 most recent negative tweets
    overall_sentiment = df['sentiment'].sum()
    # best tweet
    best = df.loc[df['sentiment'] == df['sentiment'].max()]
    best_tweet = best.tweet[0]
    best_username = best.username[0]
    # worst
    worst = df.loc[df['sentiment'] == df['sentiment'].min()]
    worst_tweet = worst.tweet[0]
    worst_user = worst.username[0]
    # sentiment over time
    time_data = df.resample('D').sentiment.sum()
    # tweet volume over time
    tweet_volume = df.resample('D').tweet.count()
    # loop to separate data and labels into list
    time_x = []
    time_y = []
    app.logger.info('looping...')
    time_df = json.loads(pd.DataFrame(time_data).to_json())
    app.logger.info(json.dumps(time_df, indent=2))
    for key in time_df['sentiment']:
        # turn this to formatted date str
        ts = int(key) / 1000
        print(ts)
        date_str = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        app.logger.info(date_str)
        time_x.append(date_str)
        time_y.append(time_df['sentiment'][key])
    # prepare data for bar chart
    volume_x = []
    volume_y = []
    volume_df = json.loads(pd.DataFrame(tweet_volume).to_json())
    for key in volume_df['tweet']:
        ts = int(key)/1000
        date_str = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        volume_x.append(date_str)
        volume_y.append(volume_df['tweet'][key])
    # get best 10 recent tweets
    recent_positive = pd.DataFrame(df.loc[df['sentiment'] > 0].head(n=10))
    recent_positive = json.loads(recent_positive.to_json())
    recent_positive_user = []
    recent_positive_tweet = []
    recent_positive_sentiment = []
    for column in recent_positive:
        for key in recent_positive[column]:
            if column == 'username':
                recent_positive_user.append(recent_positive[column][key])
            elif column == 'tweet':
                recent_positive_tweet.append(recent_positive[column][key])
            elif column == 'sentiment':
                recent_positive_sentiment.append(round(recent_positive[column][key],2))
    # ranks
    ranks = rank_brokers()
    # get worst 10 recent tweets
    recent_negative = pd.DataFrame(df.loc[df['sentiment'] < 0].head(n=10))
    recent_negative = json.loads(recent_negative.to_json())
    recent_negative_user = []
    recent_negative_tweet = []
    recent_negative_sentiment = []
    for column in recent_negative:
        for key in recent_negative[column]:
            if column == 'username':
                recent_negative_user.append(recent_negative[column][key])
            elif column == 'tweet':
                recent_negative_tweet.append(recent_negative[column][key])
            elif column == 'sentiment':
                recent_negative_sentiment.append(round(recent_negative[column][key],2))


    data = {
        'overall_sentiment': round(overall_sentiment, 2), 
        'best': {
            'user': best_username,
            'tweet': best_tweet
        },
        'worst':{
            'user': worst_user,
            'tweet': worst_tweet
        },
        'sentiment_over_time': {
            'x': time_x,
            'y': time_y
        },
        'tweet_volume': {
            'x': volume_x,
            'y': volume_y
        },
        'best_10': {
            'username': recent_positive_user,
            'tweet': recent_positive_tweet,
            'sentiment': recent_positive_sentiment
        },
        'worst_10': {
            'username': recent_negative_user,
            'tweet': recent_negative_tweet,
            'sentiment': recent_negative_sentiment
        },
        'ranks': ranks}
    app.logger.info('calling /data')
    app.logger.info(data['sentiment_over_time']['x'])
    app.logger.info(data['sentiment_over_time']['y'])
    return jsonify(data)

@app.route('/')
def main():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0')