import json
import os
from datetime import datetime

class Storage:
    """Handle JSON file operations"""
    
    @staticmethod
    def ensure_directory():
        """Create storage directory if it doesn't exist"""
        os.makedirs("storage", exist_ok=True)
    
    @staticmethod
    def read_json(filepath, default=None):
        """Read data from JSON file"""
        Storage.ensure_directory()
        if default is None:
            default = []
        
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return default
    
    @staticmethod
    def write_json(filepath, data):
        """Write data to JSON file"""
        Storage.ensure_directory()
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False
    
    @staticmethod
    def log_activity(user_email, action, details=""):
        """Log user activity"""
        from config.settings import Config
        
        logs = Storage.read_json(Config.LOG_FILE, default=[])
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_email,
            "action": action,
            "details": details
        }
        logs.append(log_entry)
        Storage.write_json(Config.LOG_FILE, logs)
