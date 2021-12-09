import pymongo
import getPosts as GetPosts
import getNews as GetNews
import category as category
import threading
import time
from apscheduler.schedulers.background import BackgroundScheduler

# config for scheduler to run every 10 minutes
scheduler = BackgroundScheduler()

urllist = category.getAll('http://www.panorama.com.al/')

# connect to mongodb
client = pymongo.MongoClient("mongodb://localhost:27017/")

# if database panorama doesn't exist, create it
if not client.panorama:
    client.create_database('panorama')
# if collection panorama.posts doesn't exist, create it
collection = client.panorama.posts


# function to get news from url
def getNews(category, url):
    count = 0
    # if collection contain document with same title and date, skip it
    for post in GetPosts.getPosts(url):
        if collection.find_one({'title': post.title, 'date': post.date}):
            continue
        else:
            news = GetNews.getNews(post)
            # if news is not None, add it to collection
            if news:
                print('Inserting document: ' + post.title[5:])
                collection.insert_one(news.__dict__)
                count += 1
            count += 1
    # print done saving count of documents
    print('Done saving ' + str(count) + ' documents')


def getAllNews():
    # for each url in urllist, create thread and start it
    for category, url in urllist:
        t = threading.Thread(target=getNews, args=(category, url))
        # print thread name
        t.start()
    # print mesage when all threads are done
    print('All threads are done')


# add job to scheduler to run every 10 minutes and start it immediately
scheduler.add_job(getAllNews, 'interval', minutes=15)
scheduler.start()
try:
    # This is here to simulate application activity (which keeps the main thread alive).
    while True:
        time.sleep(10)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
    scheduler.shutdown()
