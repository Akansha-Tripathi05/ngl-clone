# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# db = SQLAlchemy()

# class Message(db.Model):
#     __tablename__ = "messages"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(128), nullable=True)
#     content = db.Column(db.Text, nullable=False)
#     user_agent = db.Column(db.String(300))
#     ip_address = db.Column(db.String(100))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=True)  # Format: "[fingerprint] → recipient"
    content = db.Column(db.Text, nullable=False)
    
    # Network info
    ip_address = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    
    # Device info (NEW)
    device_type = db.Column(db.String(50), nullable=True)  # iPhone, Android, iPad, etc.
    device_model = db.Column(db.String(100), nullable=True)  # iPhone 15 Pro, etc.
    browser = db.Column(db.String(100), nullable=True)  # Instagram App, Chrome, etc.
    os = db.Column(db.String(50), nullable=True)  # iOS, Android, etc.
    os_version = db.Column(db.String(50), nullable=True)  # 17.2, etc.
    
    # Location info (NEW)
    location_city = db.Column(db.String(100), nullable=True)
    location_region = db.Column(db.String(100), nullable=True)
    location_country = db.Column(db.String(100), nullable=True)
    timezone = db.Column(db.String(100), nullable=True)
    isp = db.Column(db.String(200), nullable=True)
    
    # Fingerprint for tracking
    fingerprint = db.Column(db.String(100), nullable=True)
    device_details = db.Column(db.Text, nullable=True)  # JSON string with all details
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Message {self.id} from {self.username or "Anonymous"}>'