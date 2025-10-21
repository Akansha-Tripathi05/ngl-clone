import os
from dotenv import load_dotenv

load_dotenv()  # load local .env for development

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-to-a-strong-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "adminpass")