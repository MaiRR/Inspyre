import util.config

def create_db():
    db, c = util.config.start_db()
    c.execute('''
        CREATE TABLE favorites (
            username TEXT NOT NULL,
            data BLOB NOT NULL
        )
    ''')
    util.config.end_db(db)

