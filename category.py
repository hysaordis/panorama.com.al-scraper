import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from Models.NewsModel import News


# function to get all category links from panorama.com.al website
def getAll(url):
    print('Getting posts from: ' + url)
    r = requests.get(url)
    categoryResult = []
    soup = BeautifulSoup(r.content, 'html.parser')
    menu = soup.find('div', class_='menu-menyja-container')
    categories = menu.find_all('li')
    for category in categories:
        link = category.find('a')['href']
        # if link is website link then continue
        if not link.startswith('http'):
            continue
        title = category.find('a').text
        # if title is equal to '\xa0' then skip this category
        if title == '\xa0':
            continue
        categoryResult.append((title, link))
    print('Posts category: ' + str(len(categoryResult)))
    return categoryResult