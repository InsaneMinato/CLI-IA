import sqlite3
from sqlite3 import Error
import json

conn = sqlite3.connect("messages.db")
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS messages (
                                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                       role TEXT NOT NULL,
                                                       content TEXT NOT NULL,
                                                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
               )
               """)
conn.commit()


def save_message(role, content):
    try:
        cursor.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)",
            (role, content)
        )
        conn.commit()
    except Error as e:
        return f"Erreur : {str(e)}"

