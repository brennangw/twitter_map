from flask import Flask, render_template, request, send_from_directory, send_file, jsonify,app, session
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    #return send_from_directory('html', 'index.html') why doesnt this work??
    return send_file('static/html/index.html')

if __name__ == '__main__':
    app.run()
