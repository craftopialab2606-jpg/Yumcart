import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "yumcart.db")

def get_db():
    return sqlite3.connect(DB_PATH)

def setup_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            category TEXT
        )
    """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT,
                quantity INTEGER,
                total_price REAL,
                order_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)


    conn.commit()
    conn.close()
