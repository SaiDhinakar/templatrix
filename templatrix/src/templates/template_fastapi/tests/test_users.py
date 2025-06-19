import pytest
from fastapi.testclient import TestClient
from fastapi import status
import tempfile
import os
import sqlite3

from __main__ import app
from models.user import UserCreate, User
from db.database import UserDataBase
from utils.database import get_database


class TestUserDataBase:
    """Test the UserDataBase class directly"""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing"""
        temp_fd, temp_path = tempfile.mkstemp(suffix='.db')
        os.close(temp_fd)
        
        # Create a test database instance
        original_path = './databases/users.db'
        
        # Patch the database path temporarily
        import db.database
        db.database.UserDataBase.__init__ = lambda self: self._init_temp_db(temp_path)
        
        def _init_temp_db(self, path):
            self.conn = sqlite3.connect(path, check_same_thread=False)
            self.cur = self.conn.cursor()
            # Create the table
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS Users(
                    username VARCHAR PRIMARY KEY,
                    email VARCHAR UNIQUE NOT NULL
                );
            """)
            self.conn.commit()
        
        db.database.UserDataBase._init_temp_db = _init_temp_db
        
        db_instance = UserDataBase()
        yield db_instance
        
        # Cleanup
        db_instance.close()
        try:
            os.unlink(temp_path)
        except FileNotFoundError:
            pass
    
    def test_add_user_success(self, temp_db):
        """Test adding a user successfully"""
        user = UserCreate(username="testuser", email="test@example.com")
        result = temp_db.add_user(user)
        assert result is True
    
    def test_add_duplicate_user(self, temp_db):
        """Test adding a duplicate user fails"""
        user = UserCreate(username="testuser", email="test@example.com")
        temp_db.add_user(user)
        
        # Try to add the same user again
        result = temp_db.add_user(user)
        assert result is False
    
    def test_get_user_exists(self, temp_db):
        """Test getting an existing user"""
        user = UserCreate(username="testuser", email="test@example.com")
        temp_db.add_user(user)
        
        retrieved_user = temp_db.get_user("testuser")
        assert retrieved_user is not None
        assert retrieved_user.username == "testuser"
        assert retrieved_user.email == "test@example.com"
    
    def test_get_user_not_exists(self, temp_db):
        """Test getting a non-existent user"""
        retrieved_user = temp_db.get_user("nonexistent")
        assert retrieved_user is None
    
    def test_get_all_users(self, temp_db):
        """Test getting all users"""
        users = [
            UserCreate(username="user1", email="user1@example.com"),
            UserCreate(username="user2", email="user2@example.com"),
            UserCreate(username="user3", email="user3@example.com")
        ]
        
        for user in users:
            temp_db.add_user(user)
        
        all_users = temp_db.get_users()
        assert len(all_users) == 3
        usernames = [user.username for user in all_users]
        assert "user1" in usernames
        assert "user2" in usernames
        assert "user3" in usernames
    
    def test_remove_user_success(self, temp_db):
        """Test removing an existing user"""
        user = UserCreate(username="testuser", email="test@example.com")
        temp_db.add_user(user)
        
        result = temp_db.remove_user("testuser")
        assert result is True
        
        # Verify user is removed
        retrieved_user = temp_db.get_user("testuser")
        assert retrieved_user is None
    
    def test_remove_user_not_exists(self, temp_db):
        """Test removing a non-existent user"""
        result = temp_db.remove_user("nonexistent")
        assert result is False


class TestUserAPI:
    """Test the FastAPI user endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create a test client"""
        return TestClient(app)
    
    @pytest.fixture
    def mock_db(self, monkeypatch):
        """Mock the database for API testing"""
        test_users = []
        
        class MockUserDataBase:
            def get_users(self):
                return test_users
            
            def get_user(self, username: str):
                for user in test_users:
                    if user.username == username:
                        return user
                return None
            
            def add_user(self, user: UserCreate):
                # Check if user already exists
                if any(u.username == user.username for u in test_users):
                    return False
                test_users.append(User(username=user.username, email=user.email))
                return True
            
            def remove_user(self, username: str):
                for i, user in enumerate(test_users):
                    if user.username == username:
                        test_users.pop(i)
                        return True
                return False
        
        mock_db_instance = MockUserDataBase()
        monkeypatch.setattr("utils.database.get_database", lambda: mock_db_instance)
        return mock_db_instance
    
    def test_get_all_users_empty(self, client, mock_db):
        """Test getting all users when database is empty"""
        response = client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_create_user_success(self, client, mock_db):
        """Test creating a user successfully"""
        user_data = {"username": "testuser", "email": "test@example.com"}
        response = client.post("/api/v1/users/", json=user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    def test_create_user_duplicate(self, client, mock_db):
        """Test creating a duplicate user fails"""
        user_data = {"username": "testuser", "email": "test@example.com"}
        
        # Create user first time
        client.post("/api/v1/users/", json=user_data)
        
        # Try to create the same user again
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]
    
    def test_get_user_success(self, client, mock_db):
        """Test getting an existing user"""
        # Create a user first
        user_data = {"username": "testuser", "email": "test@example.com"}
        client.post("/api/v1/users/", json=user_data)
        
        # Get the user
        response = client.get("/api/v1/users/testuser")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    def test_get_user_not_found(self, client, mock_db):
        """Test getting a non-existent user"""
        response = client.get("/api/v1/users/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_delete_user_success(self, client, mock_db):
        """Test deleting an existing user"""
        # Create a user first
        user_data = {"username": "testuser", "email": "test@example.com"}
        client.post("/api/v1/users/", json=user_data)
        
        # Delete the user
        response = client.delete("/api/v1/users/testuser")
        assert response.status_code == status.HTTP_200_OK
        assert "deleted successfully" in response.json()["message"]
        
        # Verify user is deleted
        response = client.get("/api/v1/users/testuser")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_user_not_found(self, client, mock_db):
        """Test deleting a non-existent user"""
        response = client.delete("/api/v1/users/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]
    
    def test_update_user_success(self, client, mock_db):
        """Test updating an existing user"""
        # Create a user first
        user_data = {"username": "testuser", "email": "test@example.com"}
        client.post("/api/v1/users/", json=user_data)
        
        # Update the user
        updated_data = {"username": "testuser", "email": "updated@example.com"}
        response = client.put("/api/v1/users/testuser", json=updated_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "updated@example.com"
    
    def test_update_user_not_found(self, client, mock_db):
        """Test updating a non-existent user"""
        updated_data = {"username": "nonexistent", "email": "test@example.com"}
        response = client.put("/api/v1/users/nonexistent", json=updated_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_check_user_exists_true(self, client, mock_db):
        """Test checking if a user exists (true case)"""
        # Create a user first
        user_data = {"username": "testuser", "email": "test@example.com"}
        client.post("/api/v1/users/", json=user_data)
        
        response = client.get("/api/v1/users/testuser/exists")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert data["data"]["exists"] is True
    
    def test_check_user_exists_false(self, client, mock_db):
        """Test checking if a user exists (false case)"""
        response = client.get("/api/v1/users/nonexistent/exists")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert data["data"]["exists"] is False
    
    def test_create_user_invalid_data(self, client, mock_db):
        """Test creating a user with invalid data"""
        # Missing email
        invalid_data = {"username": "testuser"}
        response = client.post("/api/v1/users/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Missing username
        invalid_data = {"email": "test@example.com"}
        response = client.post("/api/v1/users/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_all_users_with_data(self, client, mock_db):
        """Test getting all users when there are multiple users"""
        users = [
            {"username": "user1", "email": "user1@example.com"},
            {"username": "user2", "email": "user2@example.com"},
            {"username": "user3", "email": "user3@example.com"}
        ]
        
        # Create multiple users
        for user_data in users:
            client.post("/api/v1/users/", json=user_data)
        
        response = client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 4
        
        usernames = [user["username"] for user in data]
        assert "user1" in usernames
        assert "user2" in usernames
        assert "user3" in usernames


class TestHealthAPI:
    """Test the health check endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create a test client"""
        return TestClient(app)
    
    def test_health_check(self, client):
        """Test the general health check endpoint"""
        response = client.get("/api/v1/health/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "app_name" in data["data"]
        assert "version" in data["data"]
        assert "database" in data["data"]
    
    def test_database_health_check(self, client):
        """Test the database health check endpoint"""
        response = client.get("/api/v1/health/database")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "status" in data["data"]


class TestRootEndpoint:
    """Test the root endpoint"""
    
    @pytest.fixture
    def client(self):
        """Create a test client"""
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "app_name" in data
        assert "version" in data
        assert "docs_url" in data
        assert "api_prefix" in data


# Run tests with: python -m pytest tests/test_users.py -v