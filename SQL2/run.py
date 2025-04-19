import sqlite3

conn = sqlite3.connect('personal.db')
cur = conn.cursor()

cur.execute("")

cur.execute(
"""
CREATE TABLE IF NOT EXISTS anstalld (
    id INTEGER PRIMARY KEY,
    namn TEXT NOT NULL,
    telefon TEXT,
    lon INTEGER,
    chef INTEGER REFERENCES anstalld(id),
    avdelning TEXT REFERENCES avdelning(avd_id)
)
"""
)

cur.execute(
"""
CREATE TABLE IF NOT EXISTS avdelning (
    avd_id TEXT PRIMARY KEY,
    namn TEXT
)
"""
)

anställda = [
    ('Stina', '2677', 30000, None, 'H'),
    ('Saddam', '1088', 22000, 1, 'S'),
    ('Lotta', '4590', 28000, 2, 'H'),
    ('Olle', '2688', 20000, 3, 'S'),
    ('Maria', '2690', 25000, 4, 'C'),
    ('Ulrik', '2698', 26000, 3, 'C'),
    ('Petter', '2645', 22000, 3, 'C')
]

cur.executemany("INSERT INTO anstalld (namn, telefon, lon, chef, avdelning) VALUES (?, ?, ?, ?, ?)", anställda)

avdelningar = [
('H', 'Högkvarteret'),
('S', 'Säkerhet'),
('C', 'Data')
]

cur.executemany("INSERT INTO avdelning (avd_id, namn) VALUES (?, ?)", avdelningar)

conn.commit()
conn.close()