# flask_ngrok_example.py
from datetime import date
import pymongo
from Models.NewsModel import News
from flask import Flask, jsonify, request
from flask_ngrok import run_with_ngrok
# import app as app
import json
import pymongo
import getPosts as GetPosts
import getNews as GetNews

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run
# connect to mongodb
client = pymongo.MongoClient("mongodb://localhost:27017/")
# if database doesn't exist, create it
if not client.panorama:
    client.panorama = pymongo.database.Database(client, 'panorama')
# if collection doesn't exist, create it
if not client.panorama.news:
    client.panorama.news = pymongo.collection.Collection(
        client.panorama, 'posts')

# define database and collection
db = client.panorama
collection = db.posts


@app.route("/")
def GetNews():
    # get last 10 documents from collection first 10 documents
    news = collection.find()

    newslist = []
    for n in news:
        title = n['title']
        date = n['date']
        # convert date to string
        date = date.strftime("%d/%m/%Y")
        url = n['url']
        content = n['content']
        imagelist = n['images']
        imagejson = imagelist[0]
        # load image json to get image name and content
        image = json.loads(imagejson)
        name = image['name']
        imagecontent = image['content']

        news = News(title, date, url, content, None)
        # create news object
        newslist.append(news)
    # return json of news
    json_string = json.dumps([ob.__dict__ for ob in newslist])
    response = app.response_class(response=json_string,
                                  status=200,
                                  mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run()