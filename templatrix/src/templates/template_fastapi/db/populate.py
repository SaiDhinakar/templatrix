from .database import UserDataBase
from models.user import UserCreate

user_db = UserDataBase()

def create_table() -> None:
    """Create the Users table if it doesn't exist"""
    query = """
    CREATE TABLE IF NOT EXISTS Users(
        username VARCHAR PRIMARY KEY,
        email VARCHAR UNIQUE NOT NULL
    );
    """
    user_db.cur.execute(query)
    user_db.conn.commit()
    return

def check_data_exists() -> bool:
    """Check if the Users table exists and has data"""
    create_table()
    try:
        result = user_db.cur.execute("SELECT COUNT(*) FROM Users;").fetchone()
        return result[0] == 0  # Return True if no data exists (need to populate)
    except Exception:
        return True  # If there's an error, assume we need to populate

def load_sample_data() -> None:
    """Load sample user data into the database"""
    sample_users = [
        UserCreate(username="alex", email="alex@gmail.com"),
        UserCreate(username="bob", email="bob@yahoo.com"),
        UserCreate(username="qwen", email="qwen@gmail.com"),
        UserCreate(username="peter", email="peter@gmail.com")
    ]
    
    for user in sample_users:
        try:
            user_db.add_user(user)
        except Exception as e:
            print(f"Error adding user {user.username}: {str(e)}")
    
    return

    