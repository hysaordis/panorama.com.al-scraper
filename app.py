import pymongo
import getPosts as GetPosts
import getNews as GetNews

urllist = []
lajmidundit = ('lajmidundit',
               'http://www.panorama.com.al/category/lajmi-i-fundit/')
opinion = ('opinion', 'http://www.panorama.com.al/category/opinion/')
politike = ('politike', 'http://www.panorama.com.al/category/politike/')
aktualitet = ('aktualitet', 'http://www.panorama.com.al/category/aktualitet/')
argument = ('argument', 'http://www.panorama.com.al/category/argument/')
kronike = ('kronike', 'http://www.panorama.com.al/category/kronike/')
ekonomi = ('ekonomi', 'http://www.panorama.com.al/category/ekonomi/')
kosova = ('kosova', 'http://www.panorama.com.al/category/kosova/')
sport = ('sport', 'http://www.panorama.com.al/category/sport/')
kulture = ('kulture', 'http://www.panorama.com.al/category/kulture/')
dossier = ('dossier', 'http://www.panorama.com.al/category/dossier/')
kuriozitete = ('kuriozitete',
               'http://www.panorama.com.al/category/kuriozitete/')
lifestyle = ('lifestyle', 'http://www.panorama.com.al/category/lifestyle/')

# add all urls to urllist
urllist.append(lajmidundit)
urllist.append(opinion)
urllist.append(politike)
urllist.append(aktualitet)
urllist.append(argument)
urllist.append(kronike)
urllist.append(ekonomi)
urllist.append(kosova)
urllist.append(sport)
urllist.append(kulture)
urllist.append(dossier)
urllist.append(kuriozitete)
urllist.append(lifestyle)

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
