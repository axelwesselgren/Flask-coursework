from server.dbhandler import create_connection

conn = create_connection()
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS worms")

cur.execute(
"""
CREATE TABLE IF NOT EXISTS worms (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    length INTEGER NOT NULL
)
"""
)

cur.execute(
"""
CREATE TABLE IF NOT EXISTS apples (
    id INTEGER PRIMARY KEY,
    color TEXT NOT NULL,
    tree_id INTEGER REFERENCES worms(id)
)
"""
)

cur.execute(
"""
INSERT INTO worms(name, length) 
VALUES ('Adam', 10), ('Oskar', 9), ('William', 5)
"""
)

cur.execute(
"""
INSERT INTO apples(color, tree_id)
VALUES ('Red', 1), ('Yellow', 1), ('Green', 2)
"""
)

conn.commit()
cur.close()
conn.close()