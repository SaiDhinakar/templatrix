import os

class Config:
    SECRET_KEY = 'templatrix_secret_key'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Static user credentials for initial login
    STATIC_USER = 'admin'
    STATIC_PASS = 'password'

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = os.path.join(Config.BASE_DIR, 'app', 'databases', 'users.db')

class TestingConfig(Config):
    TESTING = True
    DATABASE = os.path.join(Config.BASE_DIR, 'app', 'databases', 'test_users.db')

class ProductionConfig(Config):
    DEBUG = False
    DATABASE = os.path.join(Config.BASE_DIR, 'app', 'databases', 'users.db')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}