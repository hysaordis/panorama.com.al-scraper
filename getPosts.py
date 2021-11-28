import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from Models.NewsModel import News


def getPosts(url):
    print('Getting posts from: ' + url)
    r = requests.get(url)
    postsresult = []
    soup = BeautifulSoup(r.content, 'html.parser')
    posts = soup.find_all(
        'div', class_='td_module_10 td_module_wrap td-animation-stack')
    for post in posts:
        link = post.find('a')['href']
        time = post.find('time')
        date = time.get('datetime')
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+00:00')
        # convert date to Day Month Year hour:minute format
        date = date.strftime('%d/%m/%Y %H:%M')
        # convert date to datetime
        date = datetime.strptime(date, '%d/%m/%Y %H:%M')
        # replace link with https://www.panorama.com.al/
        title = link.replace('http://www.panorama.com.al/',
                             '').replace('/', '')
        # define News object and append to list
        news = News(title, None, date, link, 'tets', None)
        # append News object to list
        postsresult.append(news)
    print('Posts found: ' + str(len(postsresult)))
    return postsresult
