import util.config

def create_db():
    db, c = util.config.start_db()
    c.execute('''
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            pass_hash BLOB NOT NULL,
            salt BLOB NOT NULL,
            goal TEXT,
            last_goal_time INT
        )
    ''')
    util.config.end_db(db)
