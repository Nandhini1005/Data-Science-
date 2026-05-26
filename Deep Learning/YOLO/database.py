import sqlite3


def create_table():
    conn = sqlite3.connect('surveillance.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
        username TEXT,
        password TEXT
        )
    ''')

    conn.commit()
    conn.close()


create_table()