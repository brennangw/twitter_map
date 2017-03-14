from flask import send_file, jsonify, request
from flask import Flask
import certifi
from elasticsearch import Elasticsearch
import secretsAndSettings as sas
index = "geo-tweets"
#elasticsearch set up
elasticsearch = Elasticsearch(sas.elasticSearch['uri'],
                              port=sas.elasticSearch['port'],
                              use_ssl=sas.elasticSearch['use_ssl'])




application = Flask(__name__)

@application.route('/')
def hello_world():
    #return send_from_directory('html', 'index.html') why doesnt this work??
    return send_file('static/html/index.html')

@application.route('/tweets')
def getTweets():
    query = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "text" : "soccer football basketball"
                    }
                },
            }
        }
    }
    res = elasticsearch.search(index=index, doc_type="tweet", size=1000, body=query)
    # print res
    def getSource(result): return result['_source']
    resSources = list(map(getSource, res['hits']['hits']))
    simplifiedTweets = []
    for tweet in resSources:
        simplifiedTweet = {
            'coordinates': {
                'lat': tweet['location']['lat'],
                'long' : tweet['location']['lon']
            },
            'text': tweet['text']
        }

        simplifiedTweets.append(simplifiedTweet)

    print("returning " + str(len(simplifiedTweets)) + " tweets.")
    return jsonify(simplifiedTweets)

@application.route('/geoSearch', methods=['POST'])
def searchTweetsByGeoLocation():

    lat = request.form["lat"]
    lon = request.form["lng"]
    distance = request.form["distance"]

    print(distance)

    query = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "text" : "soccer football basketball"
                    }
                },
                "filter": {
                    "geo_distance": {
                        "distance": distance + "km",
                        "location": {
                            "lat": lat,
                            "lon": lon
                        }
                    }
                }
            }
        }
    }
    res = elasticsearch.search(index=index, doc_type="tweet", size=1000, body=query)
    # print res
    def getSource(result): return result['_source']
    resSources = list(map(getSource, res['hits']['hits']))
    simplifiedTweets = []
    for tweet in resSources:
        simplifiedTweet = {
            'coordinates': {
                'lat': tweet['location']['lat'],
                'long' : tweet['location']['lon']
            },
            'text': tweet['text']
        }

        simplifiedTweets.append(simplifiedTweet)

    print("returning " + str(len(simplifiedTweets)) + " tweets.")
    return jsonify(simplifiedTweets)

@application.route('/unformattedTweets')
def getAllTweetsUnformatted():
    res = elasticsearch.search(index=index, size=20, body={"query": {"match_all": {}}})
    def getSource(result): return result['_source']
    resSources = list(map(getSource, res['hits']['hits']))
    print("returning " + str(len(resSources)) + " tweets.")
    return(jsonify(resSources))

if __name__ == '__main__':
    application.debug = True
    application.run()
