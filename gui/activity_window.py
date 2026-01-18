
import tkinter as tk
from config.settings import Config
from data.storage import Storage

class ActivityLogWindow:
    """Admin: View activity log"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Activity Log")
        self.window.geometry("900x600")
        self.window.configure(bg=Config.BG_COLOR)
        self.window.transient(parent)
        
        self._create_ui()
    
    def _create_ui(self):
        container = tk.Frame(self.window, bg=Config.BG_COLOR, padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(container, text="Activity Log", font=Config.FONT_HEADING,
                bg=Config.BG_COLOR, fg=Config.TEXT_COLOR).pack(anchor='w', pady=(0, 15))
        
        frame = tk.Frame(container, bg=Config.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(frame, font=Config.FONT_SMALL,
                               bg=Config.CARD_BG, fg=Config.TEXT_COLOR,
                               yscrollcommand=scrollbar.set, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        logs = Storage.read_json(Config.LOG_FILE, default=[])
        logs.reverse()
        
        for log in logs[:100]:
            timestamp = log.get('timestamp', 'N/A')
            user = log.get('user', 'N/A')
            action = log.get('action', 'N/A')
            details = log.get('details', '')
            
            entry = f"[{timestamp}] {user} - {action}"
            if details:
                entry += f": {details}"
            entry += "\n"
            
            self.log_text.insert(tk.END, entry)
        
        self.log_text.config(state='disabled')
