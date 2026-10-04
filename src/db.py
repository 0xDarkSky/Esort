import sqlite3
from config import DB_FILE


def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY, 
        sender TEXT, 
        received_at TEXT NOT NULL, 
        is_read INTEGER NOT NULL DEFAULT 0 CHECK (is_read IN (0, 1)))
    """)   
    conn.commit()
    conn.close() 
