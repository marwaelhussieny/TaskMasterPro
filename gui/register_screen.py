
import tkinter as tk
from tkinter import messagebox
from config.settings import Config
from services.auth_service import AuthService
from data.validator import Validator
from gui.widgets import ModernButton

class RegisterScreen:
    """Modern registration screen"""
    
    def __init__(self, parent, on_register_success, on_back):
        self.parent = parent
        self.on_register_success = on_register_success
        self.on_back = on_back
        
        self.frame = tk.Frame(parent, bg=Config.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self._create_ui()
    
    def _create_ui(self):
        container = tk.Frame(self.frame, bg=Config.CARD_BG, padx=50, pady=30)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(container, text="Create Account", font=Config.FONT_TITLE,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR).pack(pady=(0, 5))
        
        tk.Label(container, text="Fill in your details to register", font=Config.FONT_NORMAL,
                bg=Config.CARD_BG, fg=Config.TEXT_SECONDARY).pack(pady=(0, 20))
        
        self.entries = {}
        
        fields = [
            ("ID Number (14 digits)", "id_number"),
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Email", "email"),
            ("Password", "password"),
            ("Confirm Password", "confirm_password"),
            ("Mobile Number", "mobile")
        ]
        
        for label, key in fields:
            tk.Label(container, text=label, font=Config.FONT_SMALL,
                    bg=Config.CARD_BG, fg=Config.TEXT_COLOR, anchor='w').pack(fill=tk.X, pady=(0, 3))
            
            entry = tk.Entry(container, font=Config.FONT_NORMAL, width=30,
                           bg=Config.BG_COLOR, fg=Config.TEXT_COLOR,
                           insertbackground=Config.TEXT_COLOR)
            
            if "password" in key:
                entry.config(show="●")
            
            entry.pack(pady=(0, 12))
            self.entries[key] = entry
        
        tk.Label(container, text="Role", font=Config.FONT_SMALL,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR, anchor='w').pack(fill=tk.X, pady=(0, 3))
        
        self.role_var = tk.StringVar(value="Regular User")
        role_frame = tk.Frame(container, bg=Config.CARD_BG)
        role_frame.pack(fill=tk.X, pady=(0, 20))
        
        for role in ["Regular User", "Admin"]:
            tk.Radiobutton(role_frame, text=role, variable=self.role_var, value=role,
                          bg=Config.CARD_BG, fg=Config.TEXT_COLOR, 
                          selectcolor=Config.BG_COLOR, font=Config.FONT_SMALL).pack(side=tk.LEFT, padx=(0, 15))
        
        btn_frame = tk.Frame(container, bg=Config.CARD_BG)
        btn_frame.pack()
        
        ModernButton(btn_frame, "Register", self._handle_register, 
                    bg_color=Config.SUCCESS_COLOR, width=130).pack(side=tk.LEFT, padx=(0, 10))
        ModernButton(btn_frame, "Back", self.on_back, 
                    bg_color=Config.TEXT_SECONDARY, width=130).pack(side=tk.LEFT)
    
    def _handle_register(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}
        role = self.role_var.get()
        
        if not all(data.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if not Validator.validate_id_number(data['id_number']):
            messagebox.showerror("Error", "ID number must be exactly 14 digits")
            return
        
        if not Validator.validate_email(data['email']):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        valid, msg = Validator.validate_password(data['password'])
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        if data['password'] != data['confirm_password']:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if not Validator.validate_mobile(data['mobile']):
            messagebox.showerror("Error", "Invalid Egyptian mobile number (must start with 01)")
            return
        
        success, message = AuthService.register_user(
            data['id_number'], data['first_name'], data['last_name'],
            data['email'], data['password'], data['mobile'], role
        )
        
        if success:
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.on_register_success()
        else:
            messagebox.showerror("Error", message)
    
    def destroy(self):
        self.frame.destroy()
