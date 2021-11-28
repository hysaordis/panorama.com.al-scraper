from bs4 import BeautifulSoup
import requests
from Models.NewsModel import News, Image
from bson.binary import Binary
import json


def getNews(post):
    print('Getting news from: ' + post.url)
    # define list of News objects
    r = requests.get(post.url)
    soup = BeautifulSoup(r.content, 'html.parser')
    postcontent = soup.find('div', 'td-post-content td-pb-padding-side')
    postdatetime = soup.find('div', 'meta-info').text.strip()
    postdatetime = postdatetime.split('|')
    paragraphs = postcontent.find_all('p')
    content = ''
    images = []
    # get all images postcontent and add download link to images
    for img in postcontent.find_all('img'):
        # download image from img src
        img_src = img['src']
        img_name = img_src.split('/')[-1]
        img_r = requests.get(img_src)
        # init Image object and add to list
        img_obj = Image(img_name, img_r.content)
        # convert Image object to json
        img_json = json.dumps(img_obj.__dict__)
        # add json to list
        images.append(img_json)

    for paragraph in paragraphs:
        text = paragraph.get_text()
        text = text.strip()
        content += text + '\n'
    # define new News object
    post.content = content
    post.images = images
    return post