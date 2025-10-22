import os
from dotenv import load_dotenv
from sqlalchemy import inspect
from app import create_app
from models import db, Message

load_dotenv()

def init_database():
    app = create_app()
    
    with app.app_context():
        try:
            # ✅ Test DB connection
            db.engine.connect()
            print("✅ Database connection successful!")

            inspector = inspect(db.engine)

            # ✅ Drop only the messages table if it exists
            if inspector.has_table('messages'):
                print("⚙️ Dropping existing 'messages' table...")
                Message.__table__.drop(db.engine)
            else:
                print("ℹ️ 'messages' table not found — creating fresh table.")

            # ✅ Create table from model
            print("🧱 Creating 'messages' table...")
            Message.__table__.create(db.engine)
            print("✅ 'messages' table created successfully!")

            # ✅ Print database info
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if 'sqlite' in db_uri:
                print(f"📊 Using SQLite database: {db_uri}")
            else:
                safe_uri = db_uri.split('@')[1] if '@' in db_uri else db_uri
                print(f"📊 Using PostgreSQL database: {safe_uri}")

            return True

        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            return False


if __name__ == "__main__":
    init_database()
