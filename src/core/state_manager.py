import sqlite3
from sqlite3 import Error
import json


conn = sqlite3.connect("messages.db")
cursor = conn.cursor()
messages=[
    {"role": "system", "content": "Tu es un assistant personnel pour un developpeur junior. Réponds en texte brut, sans Markdown, sans astérisques ni tableaux."}
]

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


def add_message(role: str, content: str):
    messages.append({{"role": role, "content": content}})

def get_messages():
    return messages.copy()