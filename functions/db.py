import sqlite3
from pathlib import Path

current_dir = Path(__file__).resolve().parent
db_path = (current_dir / ".." / "db" / "users.db").resolve()

def get_connection():
    return sqlite3.connect(str(db_path), check_same_thread=False)

def init_db():
    with get_connection() as conn:
        statement = '''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT UNIQUE, 
            password TEXT, 
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )'''
        conn.execute(statement)
        conn.commit()



def insert_user(username, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        
        statement = 'INSERT INTO users (username, password) VALUES (?, ?)'
        cursor.execute(statement, (username, password))
        conn.commit()
