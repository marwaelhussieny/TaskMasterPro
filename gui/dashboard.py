import tkinter as tk
from tkinter import ttk, messagebox
from config.settings import Config
from services.task_service import TaskService
from gui.widgets import ModernButton
from gui.task_form import TaskFormWindow
from gui.profile_window import ProfileWindow
from gui.users_window import UsersWindow
from gui.activity_window import ActivityLogWindow

class Dashboard:
    """Main dashboard after login"""
    
    def __init__(self, parent, user, on_logout):
        self.parent = parent
        self.user = user
        self.on_logout = on_logout
        
        self.frame = tk.Frame(parent, bg=Config.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self._create_ui()
        self._check_reminders()
    
    def _create_ui(self):
        # Top bar
        top_bar = tk.Frame(self.frame, bg=Config.CARD_BG, height=60)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        tk.Label(top_bar, text=Config.APP_NAME, font=Config.FONT_HEADING,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR).pack(side=tk.LEFT, padx=20)
        
        user_label = tk.Label(top_bar, text=f"{self.user.first_name} {self.user.last_name}",
                             font=Config.FONT_NORMAL, bg=Config.CARD_BG, fg=Config.TEXT_SECONDARY)
        user_label.pack(side=tk.RIGHT, padx=10)
        
        ModernButton(top_bar, "Logout", self.on_logout, bg_color=Config.DANGER_COLOR,
                    width=100, height=35).pack(side=tk.RIGHT, padx=20)
        
        # Main content area
        content = tk.Frame(self.frame, bg=Config.BG_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self._create_stats_section(content)
        self._create_task_section(content)
        
        if self.user.role == "Admin":
            self._create_admin_section(content)
    
    def _create_stats_section(self, parent):
        stats_frame = tk.Frame(parent, bg=Config.BG_COLOR)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(stats_frame, text="Overview", font=Config.FONT_HEADING,
                bg=Config.BG_COLOR, fg=Config.TEXT_COLOR).pack(anchor='w', pady=(0, 10))
        
        stats = TaskService.get_task_statistics(self.user.email, 
                                                self.user.role == "Admin")
        
        cards_frame = tk.Frame(stats_frame, bg=Config.BG_COLOR)
        cards_frame.pack(fill=tk.X)
        
        stats_data = [
            ("Total Tasks", stats['total'], Config.PRIMARY_COLOR, 'total'),
            ("Completed", stats['completed'], Config.SUCCESS_COLOR, 'completed'),
            ("In Progress", stats['in_progress'], Config.WARNING_COLOR, 'in_progress'),
            ("To-Do", stats['todo'], Config.SECONDARY_COLOR, 'todo')
        ]
        
        self.stat_labels = {}  # Store references to update later
        
        for label, value, color, key in stats_data:
            card = tk.Frame(cards_frame, bg=color, padx=20, pady=15)
            card.pack(side=tk.LEFT, padx=(0, 10), fill=tk.BOTH, expand=True)
            
            value_label = tk.Label(card, text=str(value), font=("Segoe UI", 28, "bold"),
                    bg=color, fg=Config.TEXT_COLOR)
            value_label.pack()
            self.stat_labels[key] = value_label  # Store reference
            
            tk.Label(card, text=label, font=Config.FONT_NORMAL,
                    bg=color, fg=Config.TEXT_COLOR).pack()
    
    def _refresh_stats(self):
        """Refresh the statistics display"""
        stats = TaskService.get_task_statistics(self.user.email, 
                                                self.user.role == "Admin")
        
        # Update the stat labels with new values
        self.stat_labels['total'].config(text=str(stats['total']))
        self.stat_labels['completed'].config(text=str(stats['completed']))
        self.stat_labels['in_progress'].config(text=str(stats['in_progress']))
        self.stat_labels['todo'].config(text=str(stats['todo']))
    
    def _create_task_section(self, parent):
        task_frame = tk.Frame(parent, bg=Config.BG_COLOR)
        task_frame.pack(fill=tk.BOTH, expand=True)
        
        header = tk.Frame(task_frame, bg=Config.BG_COLOR)
        header.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(header, text="My Tasks", font=Config.FONT_HEADING,
                bg=Config.BG_COLOR, fg=Config.TEXT_COLOR).pack(side=tk.LEFT)
        
        ModernButton(header, "+ New Task", self._show_task_form,
                    bg_color=Config.SUCCESS_COLOR, width=120, height=35).pack(side=tk.RIGHT)
        
        ModernButton(header, "Profile", self._show_profile,
                    width=100, height=35).pack(side=tk.RIGHT, padx=(0, 10))
        
        search_frame = tk.Frame(task_frame, bg=Config.BG_COLOR)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", font=Config.FONT_NORMAL,
                bg=Config.BG_COLOR, fg=Config.TEXT_COLOR).pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self._refresh_tasks())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                               font=Config.FONT_NORMAL, width=30,
                               bg=Config.CARD_BG, fg=Config.TEXT_COLOR,
                               insertbackground=Config.TEXT_COLOR)
        search_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(search_frame, text="Filter:", font=Config.FONT_NORMAL,
                bg=Config.BG_COLOR, fg=Config.TEXT_COLOR).pack(side=tk.LEFT, padx=(0, 10))
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(search_frame, textvariable=self.filter_var,
                                    values=["All", "To-Do", "In Progress", "Completed"],
                                    state='readonly', width=15)
        filter_combo.pack(side=tk.LEFT)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self._refresh_tasks())
        
        list_frame = tk.Frame(task_frame, bg=Config.BG_COLOR)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_canvas = tk.Canvas(list_frame, bg=Config.BG_COLOR,
                                     highlightthickness=0,
                                     yscrollcommand=scrollbar.set)
        self.task_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_canvas.yview)
        
        self.task_container = tk.Frame(self.task_canvas, bg=Config.BG_COLOR)
        self.task_canvas.create_window((0, 0), window=self.task_container, anchor='nw')
        
        self.task_container.bind('<Configure>',
                                lambda e: self.task_canvas.configure(
                                    scrollregion=self.task_canvas.bbox('all')))
        
        self._refresh_tasks()
    
    def _refresh_tasks(self):
        for widget in self.task_container.winfo_children():
            widget.destroy()
        
        if self.user.role == "Admin":
            tasks = TaskService.get_all_tasks()
        else:
            tasks = TaskService.get_user_tasks(self.user.email)
        
        search_term = self.search_var.get().lower()
        status_filter = self.filter_var.get()
        
        filtered_tasks = []
        for task in tasks:
            if search_term and search_term not in task.title.lower():
                continue
            if status_filter != "All" and task.status != status_filter:
                continue
            filtered_tasks.append(task)
        
        filtered_tasks.sort(key=lambda t: t.due_date or "9999-99-99")
        
        if not filtered_tasks:
            tk.Label(self.task_container, text="No tasks found",
                    font=Config.FONT_NORMAL, bg=Config.BG_COLOR,
                    fg=Config.TEXT_SECONDARY).pack(pady=50)
        else:
            for task in filtered_tasks:
                self._create_task_card(self.task_container, task)
        
        # Refresh statistics whenever tasks are refreshed
        self._refresh_stats()
    
    def _create_task_card(self, parent, task):
        card = tk.Frame(parent, bg=Config.CARD_BG, padx=15, pady=12)
        card.pack(fill=tk.X, pady=(0, 10))
        
        priority_color = Config.PRIORITY_COLORS.get(task.priority, Config.TEXT_SECONDARY)
        priority_bar = tk.Frame(card, bg=priority_color, width=5)
        priority_bar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        
        info_frame = tk.Frame(card, bg=Config.CARD_BG)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        title_frame = tk.Frame(info_frame, bg=Config.CARD_BG)
        title_frame.pack(fill=tk.X, anchor='w')
        
        tk.Label(title_frame, text=task.title, font=Config.FONT_SUBHEADING,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR).pack(side=tk.LEFT)
        
        status_color = Config.STATUS_COLORS.get(task.status, Config.TEXT_SECONDARY)
        status_badge = tk.Label(title_frame, text=task.status,
                               font=Config.FONT_SMALL, bg=status_color,
                               fg=Config.TEXT_COLOR, padx=8, pady=2)
        status_badge.pack(side=tk.LEFT, padx=(10, 0))
        
        if task.description:
            desc_text = task.description[:80] + "..." if len(task.description) > 80 else task.description
            tk.Label(info_frame, text=desc_text, font=Config.FONT_SMALL,
                    bg=Config.CARD_BG, fg=Config.TEXT_SECONDARY, wraplength=400,
                    justify=tk.LEFT).pack(anchor='w', pady=(5, 0))
        
        details_frame = tk.Frame(info_frame, bg=Config.CARD_BG)
        details_frame.pack(fill=tk.X, anchor='w', pady=(8, 0))
        
        tk.Label(details_frame, text=f"Priority: {task.priority}",
                font=Config.FONT_SMALL, bg=Config.CARD_BG,
                fg=priority_color).pack(side=tk.LEFT, padx=(0, 15))
        
        if task.due_date:
            tk.Label(details_frame, text=f"Due: {task.due_date}",
                    font=Config.FONT_SMALL, bg=Config.CARD_BG,
                    fg=Config.TEXT_SECONDARY).pack(side=tk.LEFT, padx=(0, 15))
        
        if self.user.role == "Admin":
            tk.Label(details_frame, text=f"Owner: {task.owner_email}",
                    font=Config.FONT_SMALL, bg=Config.CARD_BG,
                    fg=Config.TEXT_SECONDARY).pack(side=tk.LEFT)
        
        actions = tk.Frame(card, bg=Config.CARD_BG)
        actions.pack(side=tk.RIGHT)
        
        ModernButton(actions, "Edit", lambda t=task: self._edit_task(t),
                    bg_color=Config.SECONDARY_COLOR, width=70, height=30).pack(pady=(0, 5))
        
        ModernButton(actions, "Delete", lambda t=task: self._delete_task(t),
                    bg_color=Config.DANGER_COLOR, width=70, height=30).pack()
    
    def _show_task_form(self, task=None):
        TaskFormWindow(self.parent, self.user, self._refresh_tasks, task)
    
    def _edit_task(self, task):
        self._show_task_form(task)
    
    def _delete_task(self, task):
        if messagebox.askyesno("Confirm", f"Delete task '{task.title}'?"):
            is_admin = self.user.role == "Admin"
            success, message = TaskService.delete_task(task.task_id, 
                                                       self.user.email, is_admin)
            if success:
                messagebox.showinfo("Success", message)
                self._refresh_tasks()
            else:
                messagebox.showerror("Error", message)
    
    def _show_profile(self):
        ProfileWindow(self.parent, self.user)
    
    def _create_admin_section(self, parent):
        admin_frame = tk.Frame(parent, bg=Config.CARD_BG, padx=20, pady=15)
        admin_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Label(admin_frame, text="Admin Controls", font=Config.FONT_HEADING,
                bg=Config.CARD_BG, fg=Config.TEXT_COLOR).pack(anchor='w', pady=(0, 10))
        
        btn_frame = tk.Frame(admin_frame, bg=Config.CARD_BG)
        btn_frame.pack(anchor='w')
        
        ModernButton(btn_frame, "View All Users", self._view_users,
                    width=150, height=35).pack(side=tk.LEFT, padx=(0, 10))
        
        ModernButton(btn_frame, "Activity Log", self._view_activity,
                    width=150, height=35).pack(side=tk.LEFT)
    
    def _view_users(self):
        UsersWindow(self.parent)
    
    def _view_activity(self):
        ActivityLogWindow(self.parent)
    
    def _check_reminders(self):
        upcoming = TaskService.get_upcoming_tasks(self.user.email)
        overdue = TaskService.get_overdue_tasks(self.user.email)
        
        messages = []
        if upcoming:
            messages.append(f"{len(upcoming)} task(s) due within 24 hours")
        if overdue:
            messages.append(f"{len(overdue)} overdue task(s)")
        
        if messages:
            messagebox.showwarning("Task Reminders", "\n".join(messages))
    
    def destroy(self):
        self.frame.destroy()