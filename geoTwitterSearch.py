import tweepy, json
from elasticsearch import Elasticsearch
from datetime import datetime
import certifi
import secretsAndSettings as sas
import prototypeSettings as ps

#Sign into Twitter
auth = tweepy.OAuthHandler(sas.twitterKeys['consumer_key'], sas.twitterKeys['consumer_secret'])
auth.set_access_token(sas.twitterKeys['access_token'], sas.twitterKeys['access_token_secret'])
api = tweepy.API(auth)

#Sign into Elasticsearch
elasticsearch = Elasticsearch(sas.elasticSearch['uri'],
                              port=sas.elasticSearch['port'],
                              use_ssl=sas.elasticSearch['use_ssl'])


index = "geo-tweets"

query = {
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      # "filter": {
      #   "geo_distance": {
      #     "distance": "200000000km",
      #     "location": {
      #       "lat": 28.67,
      #       "lon": 77.42
      #     }
      #   }
      # }
    }
  }
}

response = elasticsearch.search(index=index, doc_type="tweet", body=query)
print response