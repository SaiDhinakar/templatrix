"""
Database connection and initialization module
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash

def get_db_connection(db_path):
    """Get a database connection"""
    return sqlite3.connect(db_path)

def init_db(db_path):
    """Initialize the database with required tables"""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        
        conn.commit()
