import os
import pymongo
from numpy import vectorize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

# sample_files = [doc for doc in os.listdir() if doc.endswith('.txt')]

# read all files with encoding utf-8
# sample_contents = [open(doc, encoding='utf-8').read() for doc in sample_files]

vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])

# vectors = vectorize(sample_contents)
vectors = vectorize(documents)
# s_vectors = list(zip(sample_files, vectors))
s_vectors = list(zip(documents, vectors))


def check_plagiarism():
    results = set()
    global s_vectors
    for sample_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((sample_a, text_vector_a))
        del new_vectors[current_index]
        for sample_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            sample_pair = sorted((sample_a, sample_b))
            score = sample_pair[0], sample_pair[1], sim_score
            results.add(score)
    return results


for data in check_plagiarism():
    if data[2] > 0.4:
        print(data)