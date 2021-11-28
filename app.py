import pymongo
import getPosts as GetPosts
import getNews as GetNews
from Models.NewsModel import Image

url = 'http://www.panorama.com.al/category/lajmi-i-fundit/'

# connect to mongodb
client = pymongo.MongoClient("mongodb://localhost:27017/")
# if database doesn't exist, create it
if not client.panorama:
    client.panorama = pymongo.database.Database(client, 'panorama')
# if collection doesn't exist, create it
if not client.panorama.news:
    client.panorama.news = pymongo.collection.Collection(
        client.panorama, 'news')

# define database and collection
db = client.panorama
collection = db.news

count = 0
# if collection contain document with same title and date, skip it
for post in GetPosts.getPosts(url):
    if collection.find_one({'title': post.title, 'date': post.date}):
        continue
    else:
        news = GetNews.getNews(post)
        # insert document into collection
        print('Inserting document: ' + post.title[10:])
        collection.insert_one({
            'title': post.title,
            'date': post.date,
            'url': news.url,
            'content': news.content,
            'images': news.images
        })
        count += 1
# print done saving count of documents
print('Done saving ' + str(count) + ' documents')