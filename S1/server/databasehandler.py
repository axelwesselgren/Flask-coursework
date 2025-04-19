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
    conn.commit()
    
    cur.close()
    conn.close()