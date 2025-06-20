"""User authentication module"""
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from app.db.database import get_db_connection

class UserAuth:
    def __init__(self, db_path):
        """Initialize with a database path"""
        self.db_path = db_path

    def verify_user(self, username, password):
        """Verify user credentials"""
        with get_db_connection(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT password FROM users WHERE username=?', (username,))
            row = c.fetchone()
            if row and check_password_hash(row[0], password):
                return True
        return False

    def add_user(self, username, password):
        """Add a new user to the database"""
        with get_db_connection(self.db_path) as conn:
            c = conn.cursor()
            try:
                c.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                          (username, generate_password_hash(password)))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def delete_user(self, user_id):
        """Delete a user from the database"""
        with get_db_connection(self.db_path) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM users WHERE id=?', (user_id,))
            conn.commit()

    def get_users(self):
        """Get all users from the database"""
        with get_db_connection(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id, username FROM users')
            return c.fetchall()
