import base64
import bson
from bson.binary import Binary


# create a news model class
# and define the fields of the class
class News():
    def __init__(self, title, date, url, content, image):
        self.title = title
        self.date = date
        self.url = url
        self.content = content
        # if the image is not empty then encode it
        if image:
            self.image = image


# create image model class and define the fields of the class
class Image():
    def __init__(self, name, content):
        self.name = name
        # if the content is not empty then encode it as base64
        self.content = base64.b64encode(content).decode('utf-8')