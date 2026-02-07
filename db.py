import sqlite3

conn = sqlite3.connect("messages.db", check_same_thread=False)
cursor = conn.cursor()

def save_message(text):
    cursor.execute(
        "INSERT INTO messages (text) VALUES (?)",
        (text,)
    )
conn.commit()

def save_message(payload):
    cursor.execute(
        "INSERT INTO messages (payload) VALUES (?)",
        (str(payload),)
    )
    conn.commit()
