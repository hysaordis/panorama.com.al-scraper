import base64
import bson
from bson.binary import Binary
import json


# create a news model class
# and define the fields of the class
class News():
    def __init__(self, title, category, date, url, content, image):
        self.title = title
        self.date = date
        self.url = url
        self.category = category
        self.content = content
        # if the image is not empty then encode it
        if image:
            self.image = image

    # tojson method
    def to_json(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)


# create image model class and define the fields of the class
class Image():
    def __init__(self, name, content):
        self.name = name
        # if the content is not empty then encode it as base64
        self.content = base64.b64encode(content).decode('utf-8')

    # tojson method
    def to_json(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)