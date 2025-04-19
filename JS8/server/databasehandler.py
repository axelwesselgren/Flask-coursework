import sqlite3

DB_PATH = "users.db"

def connect(db_path=DB_PATH):
    try:
        return sqlite3.connect(db_path)
    except sqlite3.DatabaseError as e:
        print(e)
        
def execute(query, params=""):
    conn = connect()
    cur = conn.cursor()

    cur.execute(query, params)
    conn.commit()
    
    cur.close()
    conn.close()
    
def get_item(query, params=""):
    conn = connect()
    cur = conn.cursor()

    cur.execute(query, params)
    item = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return item

def get_tuple(query, params=""):
    conn = connect()
    cur = conn.cursor()

    cur.execute(query, params)
    array = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return array
        
def init_database():
    conn = connect()
    cur = conn.cursor()
    
    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        hash TEXT NOT NULL
    )
    """)
    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER,
        title TEXT DEFAULT null,
        content TEXT,
        date TEXT,
        parent_id INTEGER DEFAULT null,
        author_id INTEGER,
        FOREIGN KEY('parent_id') REFERENCES 'posts'('id'),
        FOREIGN KEY('author_id') REFERENCES 'users'('id'),
        PRIMARY KEY('id' AUTOINCREMENT)
    )
    """
    )
    conn.commit()
    
    cur.close()
    conn.close()