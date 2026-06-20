import sqlite3

DB_NAME = "memory/memory.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT,
        assistant_response TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        memory_key TEXT UNIQUE,
        memory_value TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_memory(user_input, assistant_response):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO memories
    (user_input, assistant_response)
    VALUES (?, ?)
    """, (user_input, assistant_response))

    conn.commit()
    conn.close()


def get_memory_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM memories")

    count = cursor.fetchone()[0]

    conn.close()

    return count


def save_user_memory(key, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO user_memory
    (memory_key, memory_value)
    VALUES (?, ?)
    """, (key, value))

    conn.commit()
    conn.close()


def get_user_memory(key):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT memory_value
    FROM user_memory
    WHERE memory_key=?
    """, (key,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None