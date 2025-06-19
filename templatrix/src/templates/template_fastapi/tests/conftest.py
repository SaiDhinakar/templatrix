# Test configuration
import os
import sys

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test settings
TEST_DATABASE_PATH = ":memory:"  # Use in-memory database for tests
TEST_HOST = "127.0.0.1"
TEST_PORT = 8001
