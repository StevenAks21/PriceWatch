import sqlite3
from pathlib import Path
import bcrypt
import dotenv
import os

dotenv.load_dotenv()
SECRET = os.getenv('SECRET').encode()

current_dir = Path(__file__).resolve().parent
db_path = (current_dir / ".." / "db" / "db.db").resolve()

def get_connection():
    return sqlite3.connect(str(db_path), check_same_thread=False)

def get_user_id(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        statement = 'SELECT * FROM users WHERE username = ?'
        result = cursor.execute(statement, (username,)).fetchone()
        if result is None:
            return None
        return result[0]

def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS users_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            quantity REAL NOT NULL,
            entry_price REAL NOT NULL,
            side TEXT NOT NULL DEFAULT 'long',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

        # Lightweight migration for existing databases
        columns = [row[1] for row in conn.execute("PRAGMA table_info(users_data)").fetchall()]
        if "quantity" not in columns:
            conn.execute("ALTER TABLE users_data ADD COLUMN quantity REAL NOT NULL DEFAULT 0")
        if "side" not in columns:
            conn.execute("ALTER TABLE users_data ADD COLUMN side TEXT NOT NULL DEFAULT 'long'")
        if "created_at" not in columns:
            conn.execute("ALTER TABLE users_data ADD COLUMN created_at TEXT NOT NULL DEFAULT (datetime('now'))")

        conn.commit()

def insert_user(username, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        
        statement = 'INSERT INTO users (username, password) VALUES (?, ?)'
        cursor.execute(statement, (username, password))
        conn.commit()

def check_password(username, password):
    with get_connection() as conn:
        cursor = conn.cursor()

        statement = 'SELECT * FROM users WHERE username = ?'
        result = cursor.execute(statement, (username,)).fetchone()

        if result is None:
            return False

        stored_hash = result[2]
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode()
        return bcrypt.checkpw(password + SECRET, stored_hash)
def insert_position(user_id, symbol, quantity, entry_price, side):
    statement = """
    INSERT INTO users_data (user_id, symbol, quantity, entry_price, side)
    VALUES (?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(statement, (user_id, symbol, quantity, entry_price, side))
        conn.commit()
        return cursor.lastrowid

def list_positions(user_id):
    statement = """
    SELECT id, symbol, quantity, entry_price, side, created_at
    FROM users_data
    WHERE user_id = ?
    ORDER BY id DESC
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        result = cursor.execute(statement, (user_id, )).fetchall()
        return result

def delete_position(user_id, position_id):
    statement = "DELETE FROM users_data WHERE user_id = ? AND id = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(statement, (user_id, position_id))
        conn.commit()
        return cursor.rowcount > 0



        
