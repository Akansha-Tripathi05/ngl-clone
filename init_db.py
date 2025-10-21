import os
from dotenv import load_dotenv
from app import create_app
from models import db

load_dotenv()

# Test database connection and create tables
def init_database():
    app = create_app()
    
    with app.app_context():
        try:
            # Test connection
            db.engine.connect()
            print("✅ Database connection successful!")
            
            # Create all tables
            db.create_all()
            print("✅ All tables created successfully!")
            
            # Get database info
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if 'sqlite' in db_uri:
                print(f"📊 Using SQLite database: {db_uri}")
            else:
                # Mask password in output
                safe_uri = db_uri.split('@')[1] if '@' in db_uri else db_uri
                print(f"📊 Using PostgreSQL database: {safe_uri}")
            
            return True
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False

if __name__ == "__main__":
    init_database()