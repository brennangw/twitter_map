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
    return jsonify(res['hits']['hits'])



if __name__ == '__main__':
    app.run()
