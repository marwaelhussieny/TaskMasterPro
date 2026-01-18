
import hashlib
from datetime import datetime

class User:
    """User model representing a system user"""
    
    def __init__(self, user_id, first_name, last_name, email, password_hash, 
                 mobile, status="active", role="Regular User", created_at=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.mobile = mobile
        self.status = status
        self.role = role
        self.created_at = created_at or datetime.now().isoformat()
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        """Verify password"""
        return self.password_hash == User.hash_password(password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password_hash": self.password_hash,
            "mobile": self.mobile,
            "status": self.status,
            "role": self.role,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create user from dictionary"""
        return cls(**data)