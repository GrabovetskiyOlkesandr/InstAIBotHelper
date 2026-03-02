
import os
import sqlite3
from datetime import datetime

DB_FILE_DEFAULT = "contacts.db"

def _get_db_path() -> str:
    # Якщо в .env є DB_FILE, беремо його, інакше contacts.db
    return os.getenv("DB_FILE", DB_FILE_DEFAULT).strip() or DB_FILE_DEFAULT

def init_db() -> None:
    db_path = _get_db_path()
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()

def save_contact(chat_id: int, text: str) -> None:
    db_path = _get_db_path()
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO contacts (chat_id, text, created_at) VALUES (?, ?, ?)",
            (str(chat_id), (text or "").strip(), datetime.utcnow().isoformat(timespec="seconds"))
        )
        conn.commit()
    finally:
        conn.close()
