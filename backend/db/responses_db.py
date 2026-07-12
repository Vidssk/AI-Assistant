# db/responses_db.py

import sqlite3

DB_PATH = "db/jarvis.db"


def init_responses_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        agent TEXT,
        response TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def add_response(response, agent=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT INTO responses(agent, response) VALUES(?, ?)",
        (agent, response)
    )

    conn.commit()
    conn.close()

    prune_responses()


def get_latest_response():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT timestamp, agent, response
        FROM responses
        ORDER BY id DESC
        LIMIT 1
    """)

    row = c.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "timestamp": row[0],
        "agent": row[1],
        "response": row[2]
    }


def get_responses(limit=20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if limit is None:
        c.execute("""
            SELECT timestamp, agent, response
            FROM responses
            ORDER BY id DESC
        """)
    else:
        c.execute("""
            SELECT timestamp, agent, response
            FROM responses
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

    rows = c.fetchall()

    conn.close()

    return [
        {
            "timestamp": row[0],
            "agent": row[1],
            "response": row[2]
        }
        for row in rows
    ]


def get_recent_responses(limit=3):
    """Return the most recent responses, newest first."""
    return get_responses(limit)


def prune_responses(max_responses=1000):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        DELETE FROM responses
        WHERE id NOT IN (
            SELECT id
            FROM responses
            ORDER BY id DESC
            LIMIT ?
        )
    """, (max_responses,))

    conn.commit()
    conn.close()
