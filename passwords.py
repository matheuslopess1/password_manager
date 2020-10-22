import sqlite3

MASTER_PASSWORD = 'TiXftTP0ady62T6fIX'

with sqlite3.connect('passwords.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        service TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
    ''')