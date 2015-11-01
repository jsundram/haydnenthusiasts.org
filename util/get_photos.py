import json
import requests
import os
from PIL import Image


directory = '../static/assets/event_photos/'
with open('../static/data.json') as f:
    data = json.load(f)

for event in data['events']:
    photo_url = event['photo']
    # name only; Get rid of query string if present
    name = photo_url.split('/')[-1].split('?')[0]
    to_write = directory + name
    if not os.path.exists(to_write):
        print("downloading %s" % name)
        r = requests.get(photo_url)
        with open(to_write, 'wb') as f:
            f.write(r.content)

        im = Image.open(to_write)
        if im.size != (400, 300):
            print("%s (date: %s) needs resizing: (%s)" % (name, event['date'], im.size))

