import pymongo
import getPosts as GetPosts
import getNews as GetNews
import category as category

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


def importAll():
    for category, url in urllist:
        getNews(category, url)


# get news from all urls
importAll()
