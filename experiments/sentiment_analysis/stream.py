#!/usr/bin/env python3
# Derived from https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/ and following parts by Marco Bonzanini (http://marcobonzanini.com/) (licensed under a Creative Commons Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/))
import tweepy
from tweepy import OAuthHandler

consumer_key = "INSERT"
consumer_secret = "INSERT"
access_token = "INSERT"
access_secret = "INSERT" 

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

from tweepy import Stream
from tweepy.streaming import StreamListener
 
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('trump.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#trump'])
