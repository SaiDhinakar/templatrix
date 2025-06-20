import pytest
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.db.database import get_db_connection, init_db
from app.auth.auth import UserAuth


class TestRoutes:
    """Test basic route functionality"""
    
    def test_login_page(self, client):
        """Test if login page loads correctly"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Login' in response.data
        assert b'Demo Credentials' in response.data
    
    def test_protected_routes(self, client):
        """Test that protected routes redirect to login"""
        # Try to access protected pages
        for endpoint in ['/welcome', '/users']:
            response = client.get(endpoint, follow_redirects=True)
            assert response.status_code == 200
            assert b'Login' in response.data


class TestUserModel:
    """Test user model functionality"""
    
    def test_user_creation(self):
        """Test creating a user instance"""
        user = User(id=1, username="testuser")
        assert user.id == 1
        assert user.username == "testuser"
    
    def test_user_representation(self):
        """Test user string representation"""
        user = User(id=1, username="testuser")
        assert repr(user) == '<User testuser>'
    
    def test_user_to_dict(self):
        """Test user to_dict method"""
        user = User(id=1, username="testuser")
        user_dict = user.to_dict()
        assert user_dict == {'id': 1, 'username': 'testuser'}


class TestUserAuthClass:
    """Test UserAuth class directly"""
    
    @pytest.fixture
    def user_auth(self, app):
        """Create a UserAuth instance for testing"""
        return UserAuth(app.config['DATABASE'])
    
    def test_verify_valid_user(self, user_auth, test_user):
        """Test verifying a valid user"""
        result = user_auth.verify_user(test_user['username'], test_user['password'])
        assert result is True
    
    def test_verify_invalid_password(self, user_auth, test_user):
        """Test verifying a user with invalid password"""
        result = user_auth.verify_user(test_user['username'], 'wrongpassword')
        assert result is False
    
    def test_verify_nonexistent_user(self, user_auth):
        """Test verifying a non-existent user"""
        result = user_auth.verify_user('nonexistentuser', 'password')
        assert result is False
    
    def test_add_and_get_users(self, user_auth, app):
        """Test adding a user and then retrieving all users"""
        # Add a new test user
        result = user_auth.add_user('newuser', 'password123')
        assert result is True
        
        # Get all users
        users = user_auth.get_users()
        
        # Check that the new user is in the list
        usernames = [user[1] for user in users]  # username is in position 1
        assert 'newuser' in usernames
        assert 'testuser' in usernames
    
    def test_add_duplicate_user(self, user_auth):
        """Test adding a duplicate user"""
        # Try to add a user with the same username
        result = user_auth.add_user('testuser', 'anotherpassword')
        assert result is False
    
    def test_delete_user(self, user_auth, app):
        """Test deleting a user"""
        # Add a user to delete
        user_auth.add_user('userToDelete', 'password123')
        
        # Get the user's ID
        with get_db_connection(app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE username = ?', ('userToDelete',))
            user_id = cursor.fetchone()[0]
        
        # Delete the user
        user_auth.delete_user(user_id)
        
        # Verify user was deleted
        with get_db_connection(app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', ('userToDelete',))
            user = cursor.fetchone()
            assert user is None


class TestUserAuth:
    """Test the UserAuth class directly"""
    
    @pytest.fixture(scope="function")
    def temp_auth(self, test_db_path):
        """Create a UserAuth instance with a temporary database"""
        # Initialize the database
        init_db(test_db_path)
        
        # Add test user
        auth = UserAuth(test_db_path)
        auth.add_user("testuser", "testpassword")
        
        return auth
    
    def test_verify_valid_user(self, temp_auth):
        """Test verifying a valid user"""
        assert temp_auth.verify_user("testuser", "testpassword") is True
    
    def test_verify_invalid_password(self, temp_auth):
        """Test verifying a user with invalid password"""
        assert temp_auth.verify_user("testuser", "wrongpassword") is False
    
    def test_verify_nonexistent_user(self, temp_auth):
        """Test verifying a non-existent user"""
        assert temp_auth.verify_user("nonexistentuser", "password") is False
    
    def test_add_user(self, temp_auth, test_db_path):
        """Test adding a new user"""
        # Add a new user
        result = temp_auth.add_user("newuser", "newpassword")
        assert result is True
        
        # Verify user was added to database
        with get_db_connection(test_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE username = ?", ("newuser",))
            user = cursor.fetchone()
            assert user is not None
            assert user[0] == "newuser"
    
    def test_add_duplicate_user(self, temp_auth):
        """Test adding a duplicate user"""
        # Try to add a user with existing username
        result = temp_auth.add_user("testuser", "anotherpassword")
        assert result is False
    
    def test_delete_user(self, temp_auth, test_db_path):
        """Test deleting a user"""
        # Add a user to delete
        temp_auth.add_user("deleteuser", "password123")
        
        # Get the user's ID
        with get_db_connection(test_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", ("deleteuser",))
            user_id = cursor.fetchone()[0]
        
        # Delete the user
        temp_auth.delete_user(user_id)
        
        # Verify user was deleted
        with get_db_connection(test_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", ("deleteuser",))
            user = cursor.fetchone()
            assert user is None
    
    def test_get_users(self, temp_auth):
        """Test retrieving all users"""
        # Add additional users
        temp_auth.add_user("user1", "password1")
        temp_auth.add_user("user2", "password2")
        
        # Get all users
        users = temp_auth.get_users()
        
        # Check that we have at least 3 users (testuser + user1 + user2)
        assert len(users) >= 3
        
        # Extract usernames for easier checking
        usernames = [user[1] for user in users]  # username is in position 1
        assert "testuser" in usernames
        assert "user1" in usernames
        assert "user2" in usernames
