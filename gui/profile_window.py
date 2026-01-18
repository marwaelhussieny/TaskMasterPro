
import tkinter as tk
from tkinter import messagebox
from config.settings import Config
from services.auth_service import AuthService
from data.validator import Validator
from gui.widgets import ModernButton

class ProfileWindow:
    """User profile window"""
    
    def __init__(self, parent, user):
        self.user = user
        
        self.window = tk.Toplevel(parent)
        self.window.title("Profile")
        self.window.geometry("400x500")
        self.window.configure(bg=Config.BG_COLOR)
        self.window.transient(parent)
        self.window.grab_set()
        
        self._create_ui()
    
    def _create_ui(self):
        container = tk.Frame(self.window, bg=Config.CARD_BG, padx=30, pady=30)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(container, text="My Profile", font=Config.FONT_HEADING,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR).pack(pady=(0, 20))
        
        fields = [
            ("ID Number", self.user.user_id, False),
            ("Email", self.user.email, False),
            ("Role", self.user.role, False),
            ("Status", self.user.status, False),
        ]
        
        for label, value, editable in fields:
            tk.Label(container, text=label, font=Config.FONT_NORMAL,
                    bg=Config.CARD_BG, fg=Config.TEXT_COLOR, anchor='w').pack(fill=tk.X, pady=(0, 5))
            entry = tk.Entry(container, font=Config.FONT_NORMAL,
                           bg=Config.BG_COLOR if editable else Config.TEXT_SECONDARY,
                           fg=Config.TEXT_COLOR, insertbackground=Config.TEXT_COLOR)
            entry.insert(0, value)
            entry.config(state='normal' if editable else 'disabled')
            entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(container, text="First Name", font=Config.FONT_NORMAL,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR, anchor='w').pack(fill=tk.X, pady=(0, 5))
        self.first_name_entry = tk.Entry(container, font=Config.FONT_NORMAL,
                                        bg=Config.BG_COLOR, fg=Config.TEXT_COLOR,
                                        insertbackground=Config.TEXT_COLOR)
        self.first_name_entry.insert(0, self.user.first_name)
        self.first_name_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(container, text="Last Name", font=Config.FONT_NORMAL,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR, anchor='w').pack(fill=tk.X, pady=(0, 5))
        self.last_name_entry = tk.Entry(container, font=Config.FONT_NORMAL,
                                       bg=Config.BG_COLOR, fg=Config.TEXT_COLOR,
                                       insertbackground=Config.TEXT_COLOR)
        self.last_name_entry.insert(0, self.user.last_name)
        self.last_name_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(container, text="Mobile Number", font=Config.FONT_NORMAL,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR, anchor='w').pack(fill=tk.X, pady=(0, 5))
        self.mobile_entry = tk.Entry(container, font=Config.FONT_NORMAL,
                                    bg=Config.BG_COLOR, fg=Config.TEXT_COLOR,
                                    insertbackground=Config.TEXT_COLOR)
        self.mobile_entry.insert(0, self.user.mobile)
        self.mobile_entry.pack(fill=tk.X, pady=(0, 25))
        
        btn_frame = tk.Frame(container, bg=Config.CARD_BG)
        btn_frame.pack()
        
        ModernButton(btn_frame, "Update", self._update_profile,
                    bg_color=Config.SUCCESS_COLOR, width=120).pack(side=tk.LEFT, padx=(0, 10))
        ModernButton(btn_frame, "Close", self.window.destroy,
                    bg_color=Config.TEXT_SECONDARY, width=120).pack(side=tk.LEFT)
    
    def _update_profile(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        mobile = self.mobile_entry.get().strip()
        
        if not all([first_name, last_name, mobile]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        if not Validator.validate_mobile(mobile):
            messagebox.showerror("Error", "Invalid Egyptian mobile number")
            return
        
        success, message = AuthService.update_profile(
            self.user.email, first_name, last_name, mobile
        )
        
        if success:
            self.user.first_name = first_name
            self.user.last_name = last_name
            self.user.mobile = mobile
            messagebox.showinfo("Success", message)
            self.window.destroy()
        else:
            messagebox.showerror("Error", message)
