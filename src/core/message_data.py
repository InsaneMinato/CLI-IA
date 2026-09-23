from typing import Any
import sqlite3
from sqlite3 import Error

def connect_db() -> sqlite3.Connection:
    return sqlite3.connect("messages.db")

def initialize_db(conn: sqlite3.Connection):
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
    print("✅ Base de données et table 'messages' initialisées avec succès.")

def check_and_add_system_message(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM messages")
    count = cursor.fetchone()[0]

    if count == 0:
        SYSTEM_ROLE = "system"
        SYSTEM_CONTENT = "Tu es un assistant personnel pour un développeur junior. Réponds en texte brut, sans Markdown, sans astérisques ni tableaux."

        try:
            cursor.execute(
                "INSERT INTO messages (role, content) VALUES (?, ?)",
                (SYSTEM_ROLE, SYSTEM_CONTENT)
            )
            conn.commit()
            print(f"✨ Premier message système ajouté avec succès. Rôle: {SYSTEM_ROLE}.")
        except Error as e:
            print(f"❌ Erreur lors de l'ajout du message système : {str(e)}")


def save_message(role: str, content: str, conn: sqlite3.Connection):
    try:
        conn.cursor().execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)",
            (role, content)
        )
        conn.commit()
        return True
    except Error as e:
        return f"Erreur lors de l'enregistrement du message : {str(e)}"

def add_message(role: str, content: str, conn: sqlite3.Connection):
    save_message(role, content, conn)

def get_messages(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    cursor = conn.cursor()
    cursor.execute("SELECT role, content, created_at FROM messages ORDER BY created_at ASC")
    messages = []
    for role, content, _created_at in cursor.fetchall():
        api_role = "assistant" if role == "IA" else role
        messages.append({"role": api_role, "content": content})
    return messages