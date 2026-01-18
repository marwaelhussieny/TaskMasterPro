import re
from datetime import datetime

class Validator:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_id_number(id_number):
        """Validate Egyptian ID (14 digits)"""
        return id_number.isdigit() and len(id_number) == 14
    
    @staticmethod
    def validate_mobile(mobile):
        """Validate Egyptian mobile number"""
        # Egyptian mobile: starts with 01, followed by 9 digits (total 11)
        pattern = r'^01[0-2,5]{1}[0-9]{8}$'
        return re.match(pattern, mobile) is not None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        return True, "Valid"
    
    @staticmethod
    def validate_date(date_str):
        """Validate date format (YYYY-MM-DD)"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False