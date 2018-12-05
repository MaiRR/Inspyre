import urllib
import urllib.request as urlrequest
from urllib.request import urlopen
import urllib.parse
import json
import random
import time


import urllib.request as urlrequest
from urllib.request import urlopen


import util.config

def image_of_the_day():
    num_images = 8
    url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0' \
            '&n={num}&mkt=en-US'.format(num=num_images)
    prefix = 'https://www.bing.com/'
    with urllib.request.urlopen(url) as f:
        result = json.loads(f.read())
    images = result['images']  # All images
    random.seed(time.time())
    rand_image = random.choice(images)
    image_path = rand_image['url']
    return prefix + image_path

def word_pair_of_the_day():
    """
    Returns a random word pair (a tuple of id, word)
    seeded by the day in UTC time
    """
    app_id = util.config.get_oxford_api_id()
    app_key = util.config.get_oxford_api_keys()
    source_lang = 'en'
    filters_raw = 'lexicalCategory=noun,adjective,adverb,verb'
    filters_basic = urllib.parse.quote(filters_raw)
    url = \
        'https://od-api.oxforddictionaries.com/api/v1/wordlist/' \
        f'{source_lang}/{filters_basic}'
    headers = {'app_id': app_id, 'app_key': app_key}
    r = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(r) as f:
        result = json.load(f)
    words = result['results']
    sec_in_day = 60 * 60 * 24  # 60 sec/min * 60 min/hr * 24 hr/day
    day_num = int(time.time() / sec_in_day)
    random.seed(day_num)  # Seed the word based on the current day
    word_dict = random.choice(words)
    return word_dict['id'], word_dict['word']

def definition_of_the_day():
    """
    Returns the pair (word, definition) for a given day
    """
    app_id = util.config.get_oxford_api_id()
    app_key = util.config.get_oxford_api_keys()
    word_id, word = word_pair_of_the_day()
    source_lang = 'en'
    url = \
        'https://od-api.oxforddictionaries.com/api/v1/entries/' \
        f'{source_lang}/{word_id}'
    headers = {'app_id': app_id, 'app_key': app_key}
    r = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(r) as f:
        result = json.load(f)
    definition = result \
        ['results'][0] \
        ['lexicalEntries'][0] \
        ['entries'][0] \
        ['senses'][0] \
        ['definitions'][0]
    return word.title(), definition[0].upper() + definition[1:]


def poem():
    poem = urllib.request.urlopen("https://www.poemist.com/api/v1/randompoems")
    response = poem.read()
    data = json.loads(response)
    return data[0]["title"], data[0]["content"]


def recommendations():
    key = '325077-Inspyre-THCC3LLO'
    req = urlrequest.Request('https://tastedive.com/api/similar?q=titanic&info=1&k=' + key, headers={'User-Agent': 'Mozilla/5.0'})
    r = urlopen(req).read()
    d = json.loads(r.decode('utf-8'))
    return d['Similar']['Info'][0]['Name'] + ':' + d['Similar']['Info'][0]['wTeaser']
