
import tkinter as tk
from data.storage import Storage
from gui.login_screen import LoginScreen
from gui.register_screen import RegisterScreen
from gui.dashboard import Dashboard
from config.settings import Config

class TaskManagementApp:
    """Main application controller"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(Config.APP_NAME)
        self.root.geometry("1200x800")
        self.root.configure(bg=Config.BG_COLOR)
        
        self.current_screen = None
        self.current_user = None
        
        Storage.ensure_directory()
        self.show_login()
        
    def show_login(self):
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = LoginScreen(
            self.root,
            self.on_login_success,
            self.show_register
        )
    
    def show_register(self):
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = RegisterScreen(
            self.root,
            self.show_login,
            self.show_login
        )
    
    def on_login_success(self, user):
        self.current_user = user
        
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = Dashboard(
            self.root,
            user,
            self.logout
        )
    
    def logout(self):
        if self.current_user:
            Storage.log_activity(self.current_user.email, "Logout", "User logged out")
        
        self.current_user = None
        self.show_login()
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TaskManagementApp()
    app.run()