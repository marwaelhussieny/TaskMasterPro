
import tkinter as tk
from tkinter import messagebox
from config.settings import Config
from services.auth_service import AuthService
from gui.widgets import ModernButton

class LoginScreen:
    """Modern login screen"""
    
    def __init__(self, parent, on_login_success, on_register):
        self.parent = parent
        self.on_login_success = on_login_success
        self.on_register = on_register
        
        self.frame = tk.Frame(parent, bg=Config.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self._create_ui()
    
    def _create_ui(self):
        container = tk.Frame(self.frame, bg=Config.CARD_BG, padx=50, pady=40)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(container, text=Config.APP_NAME, font=Config.FONT_TITLE,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR).pack(pady=(0, 10))
        
        tk.Label(container, text="Sign in to your account", font=Config.FONT_NORMAL,
                bg=Config.CARD_BG, fg=Config.TEXT_SECONDARY).pack(pady=(0, 30))
        
        tk.Label(container, text="Email", font=Config.FONT_NORMAL,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR, anchor='w').pack(fill=tk.X, pady=(0, 5))
        self.email_entry = tk.Entry(container, font=Config.FONT_NORMAL, width=30,
                                     bg=Config.BG_COLOR, fg=Config.TEXT_COLOR,
                                     insertbackground=Config.TEXT_COLOR)
        self.email_entry.pack(pady=(0, 20))
        
        tk.Label(container, text="Password", font=Config.FONT_NORMAL,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR, anchor='w').pack(fill=tk.X, pady=(0, 5))
        self.password_entry = tk.Entry(container, show="●", font=Config.FONT_NORMAL, width=30,
                                       bg=Config.BG_COLOR, fg=Config.TEXT_COLOR,
                                       insertbackground=Config.TEXT_COLOR)
        self.password_entry.pack(pady=(0, 30))
        
        ModernButton(container, "Sign In", self._handle_login, width=280).pack(pady=(0, 15))
        
        link_frame = tk.Frame(container, bg=Config.CARD_BG)
        link_frame.pack()
        
        tk.Label(link_frame, text="Don't have an account?", font=Config.FONT_SMALL,
                bg=Config.CARD_BG, fg=Config.TEXT_SECONDARY).pack(side=tk.LEFT)
        
        register_btn = tk.Label(link_frame, text="Register", font=Config.FONT_SMALL,
                               bg=Config.CARD_BG, fg=Config.SECONDARY_COLOR, cursor="hand2")
        register_btn.pack(side=tk.LEFT, padx=(5, 0))
        register_btn.bind("<Button-1>", lambda e: self.on_register())
    
    def _handle_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        user, message = AuthService.login(email, password)
        
        if user:
            self.on_login_success(user)
        else:
            messagebox.showerror("Login Failed", message)
    
    def destroy(self):
        self.frame.destroy()
