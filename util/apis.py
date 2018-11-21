import urllib
import json
import random

def image_of_the_day():
    num_images = 8
    url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0' \
            '&n={num}&mkt=en-US'.format(num=num_images)
    prefix = 'https://www.bing.com/'
    with urllib.request.urlopen(url) as f:
        result = json.loads(f.read())
    images = result['images']  # All images
    rand_image = random.choice(images)
    image_path = rand_image['url']
    return prefix + image_path

