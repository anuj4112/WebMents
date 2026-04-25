"""
Configuration file for WebMents Backend
Author: Anuj Singla (2210991317)
"""

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://127.0.0.1:27017/webments'
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'public/uploads'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # CORS Configuration
    CORS_HEADERS = 'Content-Type'
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    DEVELOPMENT = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
    # Override with production MongoDB URI
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://127.0.0.1:27017/webments'
    
    # Use strong secret key in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    MONGO_URI = 'mongodb://127.0.0.1:27017/webments_test'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
