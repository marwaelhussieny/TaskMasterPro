
from models.user import User
from data.storage import Storage
from config.settings import Config

class AuthService:
    """Authentication and user management service"""
    
    @staticmethod
    def get_all_users():
        """Get all users from storage"""
        users_data = Storage.read_json(Config.USERS_FILE, default=[])
        return [User.from_dict(u) for u in users_data]
    
    @staticmethod
    def save_users(users):
        """Save users to storage"""
        users_data = [u.to_dict() for u in users]
        return Storage.write_json(Config.USERS_FILE, users_data)
    
    @staticmethod
    def register_user(user_id, first_name, last_name, email, password, mobile, role="Regular User"):
        """Register a new user"""
        users = AuthService.get_all_users()
        
        # Check if email or ID already exists
        for user in users:
            if user.email == email:
                return False, "Email already registered"
            if user.user_id == user_id:
                return False, "ID number already registered"
        
        # Create new user
        new_user = User(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=User.hash_password(password),
            mobile=mobile,
            role=role
        )
        
        users.append(new_user)
        AuthService.save_users(users)
        Storage.log_activity(email, "User Registration", f"{first_name} {last_name}")
        
        return True, "Registration successful"
    
    @staticmethod
    def login(email, password):
        """Authenticate user"""
        users = AuthService.get_all_users()
        
        for user in users:
            if user.email == email:
                if user.status != "active":
                    return None, "Account is inactive"
                if user.check_password(password):
                    Storage.log_activity(email, "Login", "Successful login")
                    return user, "Login successful"
                return None, "Invalid password"
        
        return None, "Email not found"
    
    @staticmethod
    def update_profile(email, first_name, last_name, mobile):
        """Update user profile"""
        users = AuthService.get_all_users()
        
        for user in users:
            if user.email == email:
                user.first_name = first_name
                user.last_name = last_name
                user.mobile = mobile
                AuthService.save_users(users)
                Storage.log_activity(email, "Profile Update", "Updated profile information")
                return True, "Profile updated successfully"
        
        return False, "User not found"
    
    @staticmethod
    def deactivate_user(email):
        """Deactivate a user (admin only)"""
        users = AuthService.get_all_users()
        
        for user in users:
            if user.email == email:
                user.status = "inactive"
                AuthService.save_users(users)
                return True, "User deactivated"
        
        return False, "User not found"
