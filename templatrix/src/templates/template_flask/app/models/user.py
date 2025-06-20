"""
User model for the application
"""

class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def __repr__(self):
        return f'<User {self.username}>'
        
    def to_dict(self):
        """Convert user to dictionary representation"""
        return {
            'id': self.id,
            'username': self.username
        }
