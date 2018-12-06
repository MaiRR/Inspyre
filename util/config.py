import os.path  # Used for file locations
import sqlite3
import json
import random
import time
from string import ascii_letters, digits

CUR_DIR = os.path.dirname(__file__)  # Absolute path to current directory
ROOT_DIR = os.path.join(CUR_DIR, os.path.pardir)  # Location of root directory
DATA_DIR = os.path.join(ROOT_DIR, 'data')  # Location of data directory
DB_FILE = os.path.join(DATA_DIR, 'data.db')  # Location of database file
APIS_FILE = os.path.join(DATA_DIR, 'apis.json')  # Location of apis config file

# RFC 4648 "URL and Filename safe" Base 64 Alphabet
CHARSET = ascii_letters + digits + '-_'


def use_test_db():
    global DB_FILE
    DB_FILE = os.path.join(DATA_DIR, 'test.db')  # Use test database file


def start_db():
    db = sqlite3.connect(DB_FILE)  # Open if file exists, otherwise create
    c = db.cursor()  # Facilitate db operations
    return db, c


def end_db(db):
    db.commit()  # Save changes to database
    db.close()  # Close database


def get_oxford_api_id():
    with open(APIS_FILE) as f:
        result = json.load(f)
    return result['oxford_api']['id']


def get_oxford_api_keys():
    with open(APIS_FILE) as f:
        result = json.load(f)
    return random.choice(result['oxford_api']['keys'])


def get_taste_api_key():
    with open(APIS_FILE) as f:
        result = json.load(f)
    return result['taste_api']['key']
