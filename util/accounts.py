import sqlite3  # Enable control of an sqlite database
import csv  # Facilitates CSV I/O
import os
import hashlib
import hmac

import util.config


def create_table():
    """Creates the SQLite database 'users'"""
    db, c = util.config.start_db()
    try:
        c.execute('''
            CREATE TABLE users (
                username TEXT PRIMARY KEY,
                pass_hash BLOB NOT NULL,
                salt BLOB NOT NULL,
                goal TEXT,
                last_goal_time INT
            )
        ''')
    except sqlite3.OperationalError:  # Table already exists
        pass
    util.config.end_db(db)


def user_exists(username):
    """Returns whether user `username` exists"""
    db, c = util.config.start_db()
    # Check whether there is a row in 'users' where the column 'username' has
    # the value of `username`
    c.execute(
        'SELECT EXISTS(SELECT 1 FROM users WHERE username=? LIMIT 1)',
        (username,)
    )
    result = c.fetchone()[0]  # 1 if user exists, else 0
    util.config.end_db(db)
    return result == 1


def hash_pass(password, salt):
    """Returns the hash of `password` with salt `salt`"""
    return hashlib.pbkdf2_hmac('sha512', password.encode(), salt, 100000)


def get_salt():
    """Returns a random salt"""
    return os.urandom(32)


def valid_username(username):
    """Returns whther `username` is a valid username"""
    if username is None:  # SQLite integrity check
        return False
    if len(username) > 32:  # Arbitrary length cap
        return False
    if len(username) < 1:  # Not-as-arbitrary length minimum
        return False
    for i in username:
        if i not in util.config.CHARSET:
            return False
    return True


def valid_password(password):
    """Returns whether `password` is a valid password"""
    if password is None:  # SQLite integrity check
        return False
    if len(password) < 8:  # Arbitrary length minimum
        return False
    return True


def add_user(username, password):
    """Add user `username` with password `passowrd` to database"""
    db, c = util.config.start_db()
    if not valid_username(username):
        return False
    if not valid_password(password):
        return False
    salt = get_salt()
    pass_hash = hash_pass(password, salt)
    c.execute(
        'INSERT INTO users VALUES (?, ?, ?, "", 0)',
        (username, pass_hash, salt)
    )
    util.config.end_db(db)
    return True


def auth_user(username, password):
    """Return wihether user `username` exists with password `password`"""
    db, c = util.config.start_db()
    c.execute(
        'SELECT pass_hash, salt FROM users WHERE username=? LIMIT 1',
        (username,)
    )
    result = c.fetchone()
    util.config.end_db(db)
    if result is None:
        return False

    pass_hash, salt = result
    if hmac.compare_digest(pass_hash, hash_pass(password, salt)):
        return True
    else:
        return False


def login_user(session, username):
    """Add user `username` to session `session`"""
    session['user'] = username


def is_logged_in(session):
    """Return whether user is logged into session `session`"""
    return 'user' in session


def logout_user(session):
    """Log out user from session `session`"""
    del session['user']


def get_logged_in_user(session):
    """Return user logged into session `session`"""
    if is_logged_in(session):
        return session['user']
    else:
        return None


def remove_user(username):
    """Remove user `username` from database"""
    db, c = util.config.start_db()
    c.execute(
        'DELETE FROM users WHERE username=?',
        (username,)
    )
    util.config.end_db(db)


def updateGoal(new, username):
    """Updates goal of the day"""
    db, c = util.config.start_db()
    c.execute(
        "UPDATE users SET goal =\"{}\" WHERE username =\"{}\"".format(new, username)
    )
    util.config.end_db(db)


def getGoal(username):
    """Accessor for goal"""
    db, c = util.config.start_db()
    c.execute(
        'SELECT goal FROM users WHERE username=?',
        (username,)
    )
    result = c.fetchone()
    util.config.end_db(db)
    return result[0]


def rmGoal(username):
    """Removes old goal of the day"""
    db, c = util.config.start_db()
    c.execute(
        'UPDATE users SET goal = "" WHERE username=?',
        (username,)
    )
    util.config.end_db(db)

