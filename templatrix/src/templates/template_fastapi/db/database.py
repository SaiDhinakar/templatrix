import sqlite3
from typing import List, Optional
from models.user import User, UserCreate

class UserDataBase:
    def __init__(self):
        self.conn = sqlite3.connect('./databases/users.db', check_same_thread=False)
        self.cur = self.conn.cursor()
    
    def add_user(self, user: UserCreate) -> bool:
        """Add a new user to the database"""
        try:
            query = "INSERT INTO Users (username, email) VALUES (?, ?);"
            self.cur.execute(query, (user.username, user.email))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def remove_user(self, username: str) -> bool:
        """Remove a user from the database by username"""
        try:
            query = "DELETE FROM Users WHERE username = ?;"
            result = self.cur.execute(query, (username,))
            self.conn.commit()
            return result.rowcount > 0
        except Exception as e:
            print(f"Error removing user: {str(e)}")
            return False
    
    def get_user(self, username: str) -> Optional[User]:
        """Get a specific user by username"""
        query = "SELECT username, email FROM Users WHERE username = ?;"
        result = self.cur.execute(query, (username,)).fetchone()
        if result:
            return User(username=result[0], email=result[1])
        return None
    
    def get_users(self) -> List[User]:
        """Get all users from the database"""
        query = "SELECT username, email FROM Users;"
        userdata = self.cur.execute(query).fetchall()
        return [User(username=row[0], email=row[1]) for row in userdata]

    def close(self):
        """Explicitly close the database connection"""
        try:
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
        except Exception:
            pass  # Ignore errors during cleanup

    def __del__(self):
        """Destructor - safely close connection"""
        try:
            self.close()
        except Exception:
            pass  # Ignore all errors in destructor        