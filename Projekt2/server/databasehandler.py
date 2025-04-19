import sqlite3

DB_PATH = "personal.db"

def connect(db_path=DB_PATH):
    try:
        return sqlite3.connect(db_path)
    except sqlite3.Error as e:
        print(e)
        
def get_list(query, params="") -> list:
    conn = connect()
    cur = conn.cursor()
    
    cur.execute(query, params)
    array = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return array

def execute(query, params="") -> None:
    conn = connect()
    cur = conn.cursor()
    
    cur.execute(query, params)
    conn.commit()
    
    cur.close()
    conn.close()