"""
Simple Flask Application Package
"""
from flask import Flask
import os

from app.routes.routes import routes_bp
from app.auth.auth import UserAuth
from app.db import init_db, populate_sample_data

def create_app(config_name='default'):
    """Create and configure the Flask app"""
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Setup and initialize database
    db_path = app.config['DATABASE']
    init_db(db_path)
    
    # Initialize auth
    auth = UserAuth(db_path)
    app.auth = auth
    
    # Populate database with initial data
    populate_sample_data(db_path, app.config)
    
    # Register blueprints
    app.register_blueprint(routes_bp)
    
    return app
