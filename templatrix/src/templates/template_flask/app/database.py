import sqlite3
import os
from werkzeug.security import generate_password_hash

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self._initialize_db()
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)
        
    def _initialize_db(self):
        """Initialize database with tables and default user if needed"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )''')
            conn.commit()
            
    def setup_default_user(self, username, password):
        """Set up default user if it doesn't exist"""
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE username=?', (username,))
            if not c.fetchone():
                c.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                          (username, generate_password_hash(password)))
                conn.commit()
