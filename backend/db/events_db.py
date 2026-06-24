# db/events_db.py

import sqlite3

DB_PATH = "db/jarvis.db"


def init_events_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        event TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def add_event(event):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT INTO events(event) VALUES(?)",
        (event,)
    )

    conn.commit()
    conn.close()

    prune_events()


def get_events(limit=20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT timestamp, event
        FROM events
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = c.fetchall()

    conn.close()

    return [
        {
            "timestamp": row[0],
            "event": row[1]
        }
        for row in rows
    ]

def prune_events(max_events=10000):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        DELETE FROM events
        WHERE id NOT IN (
            SELECT id
            FROM events
            ORDER BY id DESC
            LIMIT ?
        )
    """, (max_events,))

    conn.commit()
    conn.close()