import sqlite3
import hashlib



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



def register_user(username, password):
    conn = sqlite3.connect('surveillance.db')
    c = conn.cursor()

    hashed_pw = hash_password(password)

    c.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        (username, hashed_pw)
    )
    conn.commit()
    conn.close()



def login_user(username, password):
    conn = sqlite3.connect('surveillance.db')
    c = conn.cursor()

    hashed_pw = hash_password(password)

    c.execute(
        'SELECT * FROM users WHERE username=? AND password=?',
        (username, hashed_pw)
    )

    data = c.fetchone()

    conn.close()
    return data