import sqlite3
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "gold.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gold_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            gold24 INTEGER NOT NULL,
            gold22 INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def subscribe(chat_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO subscribers(chat_id, created_at)
        VALUES (?, ?)
    """, (chat_id, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def unsubscribe(chat_id: int):
    conn = get_connection()

    conn.execute(
        "DELETE FROM subscribers WHERE chat_id=?",
        (chat_id,),
    )

    conn.commit()
    conn.close()


def get_subscribers():
    conn = get_connection()

    rows = conn.execute(
        "SELECT chat_id FROM subscribers"
    ).fetchall()

    conn.close()

    return [row[0] for row in rows]


def insert_price(city, gold24, gold22):
    conn = get_connection()

    conn.execute("""
        INSERT INTO gold_prices(
            city,
            gold24,
            gold22,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        city,
        gold24,
        gold22,
        datetime.now().isoformat(),
    ))

    conn.commit()
    conn.close()


def latest_price(city="Coimbatore"):
    conn = get_connection()

    row = conn.execute("""
        SELECT gold24, gold22
        FROM gold_prices
        WHERE city=?
        ORDER BY id DESC
        LIMIT 1
    """, (city,)).fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "24K": row[0],
        "22K": row[1],
    }

def load_subscribers():
    return get_subscribers()


def load_prices():
    return latest_price()


def insert_price(city, gold24, gold22):
    conn = get_connection()
    conn.execute("""
        INSERT INTO gold_prices(
            city,
            gold24,
            gold22,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        city,
        gold24,
        gold22,
        datetime.now().isoformat(),
    ))
    conn.commit()
    conn.close()
    