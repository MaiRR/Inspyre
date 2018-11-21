import urllib
import json

def image_of_the_day():
    url = \
        'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
    prefix = 'https://www.bing.com/'
    with urllib.request.urlopen(url) as f:
        result = json.loads(f.read())
    return prefix + result['images'][0]['url']

