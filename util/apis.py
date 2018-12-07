import urllib
import urllib.request
import urllib.parse
import json
import random
import time


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
    url = 'https://www.poemist.com/api/v1/randompoems'
    poem = None
    while poem is None or len(poem) > 2500:
        with urllib.request.urlopen(url) as f:
            result = json.loads(f.read())
        poem = result[0]['content']
    title = result[0]['title']
    return title, poem


def recommendations(title):
    key = util.config.get_taste_api_key()
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://tastedive.com/api/similar?q={title}&info=1&k={key}'.format(
        title=urllib.parse.quote(title),
        key=key,
    )
    r = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(r) as f:
        result = json.load(f)
    results = result['Similar']['Results']
    print(results, 'WOW')
    return results


def rec_book(title):
    results = util.apis.recommendations(title)
    for i in results: print(i['Type'])
    book_results = [i for i in results if i['Type'] == 'book']
    print(book_results, '\n_______')
    return book_results[0] if book_results else None


def rec_movie(title):
    results = util.apis.recommendations(title)
    movie_results = [i for i in results if i['Type'] == 'movie']
    return movie_results[0] if movie_results else None


def rec_song(title):
    results = util.apis.recommendations(title)
    #  print(results)
    song_results = [i for i in results if i['Type'] == 'music']
    return song_results[0] if song_results else None

