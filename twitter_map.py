from flask import send_file, jsonify
from flask import Flask
import certifi
from elasticsearch import Elasticsearch
import secretsAndSettings as sas

#elasticsearch set up
elasticsearch = Elasticsearch(sas.elasticSearch['uri'],
                              port=sas.elasticSearch['port'],
                              use_ssl=sas.elasticSearch['use_ssl'])




app = Flask(__name__)



@app.route('/')
def hello_world():
    #return send_from_directory('html', 'index.html') why doesnt this work??
    return send_file('static/html/index.html')

@app.route('/tweets')
def getTweets():
    res = elasticsearch.search(index="tweets", body={"query": {"match_all": {}}})
    def getSource(result): return result['_source']
    resSources = list(map(getSource, res['hits']['hits']))
    simplifiedTweets = []
    for tweet in resSources:
        try:
            #are the bounding_boxes always squares? find out may need to make this more robust
            coordinates = tweet['quoted_status']['place']['bounding_box']['coordinates'][0]
            print(coordinates)
            averageCoordinates = {
                'lat' : 0.,
                'long' : 0.,
            }

            for coordinate in coordinates:
                print(coordinate)
                averageCoordinates['lat'] += float(coordinate[0])
                averageCoordinates['long'] += float(coordinate[1])

            averageCoordinates['lat'] /= float(len(coordinates))
            averageCoordinates['lat'] /= float(len(coordinates))

            print("got averages")

            simplifiedTweet = {
                'coordinates': averageCoordinates,
                'text': tweet['quoted_status']['text']
            }

            simplifiedTweets.append(simplifiedTweet)


        except Exception:
            print("failed to simplify tweet")
            pass
    print(simplifiedTweets)
    return jsonify(simplifiedTweets)



if __name__ == '__main__':
    app.run()
