import os
import sys
import pytest
import tempfile
from werkzeug.security import generate_password_hash

# Add the parent directory to sys.path to import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.db.database import get_db_connection, init_db
from app.auth.auth import UserAuth
from app.models.user import User

# Test settings
TEST_DATABASE_PATH = ":memory:"  # Use in-memory database for tests

@pytest.fixture(scope="function")
def test_db_path():
    """Create a temporary database file"""
    db_fd, db_path = tempfile.mkstemp()
    yield db_path
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope="function")
def app(test_db_path):
    """Create and configure a Flask app for testing"""
    # Configure the app to use the test database
    app = create_app('testing')
    app.config['DATABASE'] = test_db_path
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test_secret_key'
    
    # Initialize the test database
    init_db(test_db_path)
    
    # Add test user to database
    test_username = 'testuser'
    test_password = 'testpassword'
    
    with get_db_connection(test_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (test_username, generate_password_hash(test_password))
        )
        conn.commit()
    
    with app.app_context():
        yield app

@pytest.fixture(scope="function")
def client(app):
    """Create a test client for the app"""
    with app.test_client() as test_client:
        test_client.testing = True
        yield test_client

@pytest.fixture(scope="function")
def auth(test_db_path):
    """Create an auth instance for testing"""
    return UserAuth(test_db_path)

@pytest.fixture(scope="function")
def test_user():
    """Return test user credentials"""
    return {'username': 'testuser', 'password': 'testpassword'}
