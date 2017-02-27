from flask import send_file, jsonify
from flask import Flask
import certifi
from elasticsearch import Elasticsearch
import secretsAndSettings as sas

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
    res = elasticsearch.search(index="tweets", size=1000, body={"query": {"match_all": {}}})
    def getSource(result): return result['_source']
    resSources = list(map(getSource, res['hits']['hits']))
    print(jsonify(resSources))
    simplifiedTweets = []
    for tweet in resSources:
        try:
            #are the bounding_boxes always squares? find out may need to make this more robust
            coordinates = tweet['quoted_status']['place']['bounding_box']['coordinates'][0]

            averageCoordinates = {
                'lat' : 0.,
                'long' : 0.,
            }

            for coordinate in coordinates:
                averageCoordinates['lat'] += float(coordinate[0])
                averageCoordinates['long'] += float(coordinate[1])

            averageCoordinates['lat'] /= float(len(coordinates))
            averageCoordinates['lat'] /= float(len(coordinates))


            simplifiedTweet = {
                'coordinates': averageCoordinates,
                'text': tweet['quoted_status']['text']
            }

            simplifiedTweets.append(simplifiedTweet)


        except (LookupError, AttributeError, TypeError) as e:
            try:
                print("trying geo")
                coordinates = tweet["geo"]["coordinates"]
                print(coordinates)
                simplifiedTweet = {
                    'coordinates': {'lat':  float(coordinates[0]),
                                    'long': float(coordinates[1])},
                    'text': tweet['text']
                }
                print("after creating tweet")
                simplifiedTweets.append(simplifiedTweet)
            except (LookupError, AttributeError, TypeError) as e:
                print(tweet)
                print(e)
                pass


    print("returning " + str(len(simplifiedTweets)) + " tweets.")
    return jsonify(simplifiedTweets)

@application.route('/unformattedTweets')
def getAllTweetsUnformatted():
    res = elasticsearch.search(index="tweets", size=20, body={"query": {"match_all": {}}})
    def getSource(result): return result['_source']
    resSources = list(map(getSource, res['hits']['hits']))
    print("returning " + str(len(resSources)) + " tweets.")
    return(jsonify(resSources))

if __name__ == '__main__':
    application.debug = True
    application.run()
