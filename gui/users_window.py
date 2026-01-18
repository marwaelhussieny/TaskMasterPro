
import tkinter as tk
from tkinter import messagebox
from config.settings import Config
from services.auth_service import AuthService
from gui.widgets import ModernButton

class UsersWindow:
    """Admin: View all users"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("User Management")
        self.window.geometry("800x600")
        self.window.configure(bg=Config.BG_COLOR)
        self.window.transient(parent)
        
        self._create_ui()
    
    def _create_ui(self):
        container = tk.Frame(self.window, bg=Config.BG_COLOR, padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(container, text="All Users", font=Config.FONT_HEADING,
                bg=Config.BG_COLOR, fg=Config.TEXT_COLOR).pack(anchor='w', pady=(0, 15))
        
        users = AuthService.get_all_users()
        
        for user in users:
            self._create_user_card(container, user)
    
    def _create_user_card(self, parent, user):
        card = tk.Frame(parent, bg=Config.CARD_BG, padx=15, pady=12)
        card.pack(fill=tk.X, pady=(0, 10))
        
        info = tk.Frame(card, bg=Config.CARD_BG)
        info.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        name = f"{user.first_name} {user.last_name}"
        tk.Label(info, text=name, font=Config.FONT_SUBHEADING,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR).pack(anchor='w')
        
        tk.Label(info, text=f"Email: {user.email}  |  Role: {user.role}  |  Status: {user.status}",
                font=Config.FONT_SMALL, bg=Config.CARD_BG,
                fg=Config.TEXT_SECONDARY).pack(anchor='w', pady=(3, 0))
        
        if user.status == "active":
            ModernButton(card, "Deactivate", lambda u=user: self._deactivate_user(u),
                        bg_color=Config.DANGER_COLOR, width=100, height=30).pack(side=tk.RIGHT)
    
    def _deactivate_user(self, user):
        if messagebox.askyesno("Confirm", f"Deactivate user {user.email}?"):
            success, message = AuthService.deactivate_user(user.email)
            if success:
                messagebox.showinfo("Success", message)
                self.window.destroy()
                UsersWindow(self.parent)
            else:
                messagebox.showerror("Error", message)

