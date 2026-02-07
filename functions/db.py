import sqlite3
from pathlib import Path

def init_db():
    current_dir = Path(__file__).resolve().parent
    
    db_path = (current_dir / ".." / 'db' / "users.db").resolve()
    
    conn = sqlite3.connect(str(db_path))
    
    statement = '''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT, 
        password TEXT, 
        id INTEGER PRIMARY KEY AUTOINCREMENT
    )'''
    
    conn.execute(statement)
    conn.commit()
    conn.close()

init_db()