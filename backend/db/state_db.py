import sqlite3
from datetime import datetime

DB_PATH = "db/jarvis.db"
_UNSET = object()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS state (
        id INTEGER PRIMARY KEY,
        status TEXT,
        agent TEXT,
        updated_at TEXT
    )
    """)

    # ensure single row exists
    c.execute("INSERT OR IGNORE INTO state (id, status, agent, updated_at) VALUES (1, 'idle', NULL, '')")

    conn.commit()
    conn.close()


def update_state(status=None, agent=_UNSET):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if status:
        c.execute("UPDATE state SET status=?, updated_at=? WHERE id=1",
                  (status, datetime.utcnow().isoformat()))

    if agent is not _UNSET:
        c.execute("UPDATE state SET agent=?, updated_at=? WHERE id=1",
                  (agent, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()


def get_state():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT status, agent, updated_at FROM state WHERE id=1")
    row = c.fetchone()

    conn.close()

    return {
        "status": row[0],
        "agent": row[1],
        "updated_at": row[2]
    }

# def update_state(status=None, agent=None):
#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()

#     if status is not None:
#         cur.execute(
#             "UPDATE state SET status=? WHERE id=1",
#             (status,)
#         )

#     if agent is not None:
#         cur.execute(
#             "UPDATE state SET agent=? WHERE id=1",
#             (agent,)
#         )
# def get_state():
#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()

#     cur.execute("SELECT status, agent FROM state WHERE id=1")
#     row = cur.fetchone()

#     conn.close()

#     return {
#         "status": row[0],
#         "agent": row[1],
#     }

#     conn.commit()
#     conn.close()
