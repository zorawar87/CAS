from flask import Flask, url_for, render_template, request
from .TextAnalyser import TextAnalyser
import json

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return "index page."

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_path(subpath):
    return "Subpath: %s" % subpath

@app.route('/cas/', methods=['POST','GET'])
def cas_app():
    if request.method == "POST":
        print(TextAnalyser(request.form["blogpost"]).retrieve())
        info = TextAnalyser(request.form["blogpost"]).getKeyInfo()
        print(info)
        return render_template('cas-analysis.html', 
                blogpost = request.form["blogpost"],
                analysis = {"keyphrase" : info["keyPhrases"][0],"score": info["score"]*100},
                articles = [
                    {"score":0.5, "description": "this is positive", "link":"https://google.com", "website":"google.com"},
                    {"score":0.6, "description": "this is negative", "link":"https://yahoo.com", "website":"yahoo.com"}
                    ]
                )
    return render_template('cas-analysis.html')


