import sqlite3

DB_PATH = 'my_db.db'
def create_connection(db_file = DB_PATH):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn