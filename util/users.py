import util.config

def create_db():
    db, c = util.config.start_db()
    c.execute('''
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            pass_hash BLOB NOT NULL,
            salt BLOB NOT NULL
        )
    ''')
    util.config.end_db(db)
