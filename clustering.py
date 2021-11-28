import os
import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction import text

stopwords = []
#define stopwords read all line in file stopwords.txt
with open(".\stopwords.txt", "r") as f:
    # insert line one by one in stopwords
    for line in f:
        stopwords.append(line.strip())

# connect to mongodb with unicode support
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

documents = []


# function to replace character in string
def replace_char(string):
    # replace character in string and return string
    text = string.replace('ë', 'e')
    text = text.replace('ç', 'c')
    text = text.replace('Ë', 'E')
    text = text.replace('Ç', 'C')
    return text


# get all document in collection news and insert in documents
for document in collection.find():
    # if document is not empty
    if document:
        # get mongodb document and decode it to utf-8
        # content = to_utf_16le_string(document['content'])
        content = document['content']
        content = replace_char(content)
        # add document to documents
        documents.append(content)
# print found documents count in collection
print("Found %d documents" % len(documents))

vectorizer = TfidfVectorizer(stop_words=stopwords)
X = vectorizer.fit_transform(documents)

true_k = 3
model = KMeans(init="random",
               n_clusters=true_k,
               n_init=10,
               max_iter=300,
               random_state=42)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print()