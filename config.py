import os
from dotenv import load_dotenv

load_dotenv()  # load local .env for development

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-to-a-strong-secret-key-12345")
    
    # For local development, use SQLite
    # For production (PythonAnywhere), use PostgreSQL from environment
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if DATABASE_URL:
        # Fix for SQLAlchemy 1.4+ which doesn't support postgres://
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Local SQLite fallback
        SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before using them
        'pool_recycle': 300,    # Recycle connections after 5 minutes
    }
    
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "adminpass")