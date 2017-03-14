import tweepy
import json
from elasticsearch import Elasticsearch
from datetime import datetime
import certifi
import secretsAndSettings as sas

#Sign into Twitter
auth = tweepy.OAuthHandler(sas.twitterKeys['consumer_key'], sas.twitterKeys['consumer_secret'])
auth.set_access_token(sas.twitterKeys['access_token'], sas.twitterKeys['access_token_secret'])
api = tweepy.API(auth)

#Sign into Elasticsearch
elasticsearch = Elasticsearch(sas.elasticSearch['uri'],
                              port=sas.elasticSearch['port'],
                              use_ssl=sas.elasticSearch['use_ssl'])

#tracked workds
wordsToTrack = ['Baseball', 'Football', 'Darts', 'Soccer', 'Basketball']

def lowerCase(word): return str(word).lower()

wordsToTrack.extend(map(lowerCase, wordsToTrack))

def getGeoCode(tweet_data):
    location = {}
    location["lat"] = 10.10
    location["lon"] = 13.9
    return "10.19, 13.1"


tweetsSoFar = 0
lastTweetId = -9
maxTweet = 100
index = "get"

# from elasticsearch import Elasticsearch
# conntect es
# es = Elasticsearch([{'host': config.elastic_host, 'port': config.elastic_port}])
# delete index if exists
testIndex = "ti"
es = elasticsearch
if es.indices.exists(testIndex):
    es.indices.delete(index=testIndex)
# index settings
# settings = {
#     "settings": {
#         "number_of_shards": 1,
#         "number_of_replicas": 0
#     },
#     "mappings": {
#         "urls": {
#             "properties": {
#                 "url": {
#                     "type": "string"
#                 },
#                 "location": {
#                     "type": "geo_point"
#                 }
#             }
#         },
#
#      }
# }
# # # create index
# print es.indices.create(index=testIndex, ignore=400, body=settings)



# print json.dumps(es.indices.get_mapping(index="tweets", doc_type="tweet"), sort_keys=True, indent=4, separators=(',', ': '))

# mapping = '''
# {
#   "mappings":{
#     "logs_june":{
#       "_timestamp":{
#         "enabled":"true"
#       },
#       "properties":{
#         "logdate":{
#           "type":"date",
#           "format":"dd/MM/yyy HH:mm:ss"
#         }
#       }
#     }
#   }
# }'''
#
# elasticsearch.indices.create(index='test-index', ignore=400, body=mapping)
# elasticsearch.indices.create(index=)


# # Set up StreamListener for feeding twitter feeds to elastic search
# class ElasticSearchFeederStreamListener(tweepy.StreamListener):
#     def on_data(self, tweet_data):
#         geoTweet = {}
#         tweet = json.loads(tweet_data)
#         tweet['geo'] = getGeoCode(tweet_data)
#         print tweet
#         geoTweet["location"] = getGeoCode(tweet_data)
#
#         # if 'coordinates' in decoded and decoded['coordinates'] is not None:
#         print (elasticsearch.index(index="geo_tweet_test", doc_type="geo_tweet_test", body=tweet))
#
# elasticSearchFeederStreamListenerInstance = ElasticSearchFeederStreamListener()
# myStream = tweepy.Stream(auth = api.auth, listener=elasticSearchFeederStreamListenerInstance)
# myStream.filter(track=wordsToTrack)

# for tweet in tweepy.Cursor(api.search,q="*", index="geo_tweet_test", count=100000, geocode="5.29126,52.132633,1000000km").items(1000000):
#     if (tweet.geo != None):
#         print tweet.geo
#         print [tweet.created_at, tweet.text.encode('utf-8'), tweet.user.id, tweet.geo]




# api.geo_id()