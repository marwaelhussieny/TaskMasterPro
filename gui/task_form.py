
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config.settings import Config
from services.task_service import TaskService
from data.validator import Validator
from gui.widgets import ModernButton

class TaskFormWindow:
    """Task creation/editing form"""
    
    def __init__(self, parent, user, on_save_callback, task=None):
        self.user = user
        self.task = task
        self.on_save_callback = on_save_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Edit Task" if task else "New Task")
        self.window.geometry("500x600")
        self.window.configure(bg=Config.BG_COLOR)
        self.window.transient(parent)
        self.window.grab_set()
        
        self._create_ui()
    
    def _create_ui(self):
        container = tk.Frame(self.window, bg=Config.CARD_BG, padx=30, pady=30)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title = "Edit Task" if self.task else "Create New Task"
        tk.Label(container, text=title, font=Config.FONT_HEADING,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR).pack(pady=(0, 20))
        
        tk.Label(container, text="Task Title*", font=Config.FONT_NORMAL,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR, anchor='w').pack(fill=tk.X, pady=(0, 5))
        self.title_entry = tk.Entry(container, font=Config.FONT_NORMAL,
                                    bg=Config.BG_COLOR, fg=Config.TEXT_COLOR,
                                    insertbackground=Config.TEXT_COLOR)
        self.title_entry.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(container, text="Description", font=Config.FONT_NORMAL,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR, anchor='w').pack(fill=tk.X, pady=(0, 5))
        self.desc_text = tk.Text(container, font=Config.FONT_NORMAL, height=4,
                                bg=Config.BG_COLOR, fg=Config.TEXT_COLOR,
                                insertbackground=Config.TEXT_COLOR)
        self.desc_text.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(container, text="Priority*", font=Config.FONT_NORMAL,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR, anchor='w').pack(fill=tk.X, pady=(0, 5))
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(container, textvariable=self.priority_var,
                                     values=["Low", "Medium", "High"],
                                     state='readonly')
        priority_combo.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(container, text="Status*", font=Config.FONT_NORMAL,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR, anchor='w').pack(fill=tk.X, pady=(0, 5))
        self.status_var = tk.StringVar(value="To-Do")
        status_combo = ttk.Combobox(container, textvariable=self.status_var,
                                   values=["To-Do", "In Progress", "Completed"],
                                   state='readonly')
        status_combo.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(container, text="Due Date (YYYY-MM-DD)*", font=Config.FONT_NORMAL,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR, anchor='w').pack(fill=tk.X, pady=(0, 5))
        self.date_entry = tk.Entry(container, font=Config.FONT_NORMAL,
                                   bg=Config.BG_COLOR, fg=Config.TEXT_COLOR,
                                   insertbackground=Config.TEXT_COLOR)
        self.date_entry.pack(fill=tk.X, pady=(0, 25))
        
        if self.task:
            self.title_entry.insert(0, self.task.title)
            self.desc_text.insert('1.0', self.task.description)
            self.priority_var.set(self.task.priority)
            self.status_var.set(self.task.status)
            if self.task.due_date:
                self.date_entry.insert(0, self.task.due_date)
        
        btn_frame = tk.Frame(container, bg=Config.CARD_BG)
        btn_frame.pack()
        
        ModernButton(btn_frame, "Save", self._save_task,
                    bg_color=Config.SUCCESS_COLOR, width=120).pack(side=tk.LEFT, padx=(0, 10))
        ModernButton(btn_frame, "Cancel", self.window.destroy,
                    bg_color=Config.TEXT_SECONDARY, width=120).pack(side=tk.LEFT)
    
    def _save_task(self):
        title = self.title_entry.get().strip()
        description = self.desc_text.get('1.0', tk.END).strip()
        priority = self.priority_var.get()
        status = self.status_var.get()
        due_date = self.date_entry.get().strip()
        
        if not title:
            messagebox.showerror("Error", "Title is required")
            return
        
        if not due_date:
            messagebox.showerror("Error", "Due date is required")
            return
        
        if not Validator.validate_date(due_date):
            messagebox.showerror("Error", "Invalid date format (use YYYY-MM-DD)")
            return
        
        try:
            due = datetime.strptime(due_date, "%Y-%m-%d")
            if due < datetime.now():
                if not messagebox.askyesno("Warning", "Due date is in the past. Continue?"):
                    return
        except ValueError:
            pass
        
        if self.task:
            success, message = TaskService.update_task(
                self.task.task_id,
                title=title,
                description=description,
                priority=priority,
                status=status,
                due_date=due_date
            )
        else:
            success, message = TaskService.create_task(
                title, description, priority, status, due_date, self.user.email
            )
        
        if success:
            messagebox.showinfo("Success", message)
            self.on_save_callback()
            self.window.destroy()
        else:
            messagebox.showerror("Error", message)

