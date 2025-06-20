"""
Templatrix Flask Application Entry Point
"""
import os
from app import create_app

# Get configuration from environment or default to development
config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    print(f"Static login -> Username: {app.config['STATIC_USER']}, Password: {app.config['STATIC_PASS']}")
    print("Sample users created: johndoe/user123, janedoe/user456")
    app.run(debug=True)
