from functools import lru_cache
from db.database import UserDataBase
from utils.config import get_settings

@lru_cache()
def get_database() -> UserDataBase:
    """Get database instance (cached)"""
    return UserDataBase()

def init_database() -> None:
    """Initialize database with tables and sample data if needed"""
    from db.populate import check_data_exists, load_sample_data
    
    if check_data_exists():
        load_sample_data()

def health_check_database() -> bool:
    """Check if database is accessible"""
    try:
        db = get_database()
        # Try to execute a simple query
        db.cur.execute("SELECT 1")
        return True
    except Exception:
        return False
