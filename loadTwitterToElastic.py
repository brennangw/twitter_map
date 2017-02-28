import tweepy
import json
from elasticsearch import Elasticsearch
from datetime import datetime
import certifi
import secretsAndSettings as sas

#Sign into Twitter
auth = tweepy.OAuthHandler(sas.twitterKeys.consumer_key, sas.twitterKeys.consumer_secret)
auth.set_access_token(sas.twitterKeys.access_token, sas.twitterKeys.access_token_secret)
api = tweepy.API(auth)

#Sign into Elasticsearch
elasticsearch = Elasticsearch(sas.elasticSearch['uri'],
                              port=sas.elasticSearch['port'],
                              use_ssl=sas.elasticSearch['use_ssl'])

#tracked workds
wordsToTrack = ['Baseball', 'Football', 'Darts', 'Soccer', 'Basketball']

def lowerCase(word): return str(word).lower()

wordsToTrack.extend(map(lowerCase, wordsToTrack))

print wordsToTrack

#Set up StreamListener for feeding twitter feeds to elastic search
class ElasticSearchFeederStreamListener(tweepy.StreamListener):
    def on_data(self, tweet_data):
        decoded = json.loads(tweet_data)
        if 'coordinates' in decoded and decoded['coordinates'] is not None:
            print elasticsearch.index(index="tweets", doc_type="tweet", body=tweet_data)

elasticSearchFeederStreamListenerInstance = ElasticSearchFeederStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=elasticSearchFeederStreamListenerInstance)
myStream.filter(track=wordsToTrack)