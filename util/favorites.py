import sqlite3  # Enable control of an sqlite database

import util.config


def create_table():
    db, c = util.config.start_db()
    try:
        c.execute('''
            CREATE TABLE favorites (
                username TEXT NOT NULL,
                data BLOB NOT NULL
            )
        ''')
    except sqlite3.OperationalError:  # Table already exists
        pass
    util.config.end_db(db)

def add_favorite(username, data):
    db, c = util.config.start_db()
    try:
        c.execute(
            'INSERT INTO favorites VALUES(?, ?)',
            (username, data),
        )
    except sqlite3.OperationalError:  # Table already exists
        pass
    util.config.end_db(db)

