"""
Database population for initial data setup
"""
from werkzeug.security import generate_password_hash
from app.db.database import get_db_connection

def populate_sample_data(db_path, config):
    """
    Populate the database with sample data
    """
    # Get static credentials from config
    static_user = config['STATIC_USER']
    static_pass = config['STATIC_PASS']
    
    # Connect to the database
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        
        # Add static admin user if it doesn't exist
        cursor.execute('SELECT * FROM users WHERE username=?', (static_user,))
        if not cursor.fetchone():
            cursor.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (static_user, generate_password_hash(static_pass))
            )
            print(f"Created admin user: {static_user} with provided password")
            
        # Add some sample users (only if table is practically empty)
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] <= 1:  # Only the admin exists
            sample_users = [
                ('johndoe', 'user123'),
                ('janedoe', 'user456')
            ]
            
            for username, password in sample_users:
                try:
                    cursor.execute(
                        'INSERT INTO users (username, password) VALUES (?, ?)',
                        (username, generate_password_hash(password))
                    )
                    print(f"Created sample user: {username}")
                except Exception as e:
                    print(f"Error creating sample user {username}: {e}")
        
        conn.commit()
