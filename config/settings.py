
class Config:
    """Application configuration and theme settings"""
    
    # App Info
    APP_NAME = "TaskMaster Pro"
    VERSION = "1.0.0"
    
    # Colors - Modern Dark Theme
    PRIMARY_COLOR = "#1e3a8a"      # Deep blue
    SECONDARY_COLOR = "#3b82f6"    # Bright blue
    SUCCESS_COLOR = "#10b981"      # Green
    WARNING_COLOR = "#f59e0b"      # Orange
    DANGER_COLOR = "#ef4444"       # Red
    
    BG_COLOR = "#0f172a"           # Dark background
    CARD_BG = "#1e293b"            # Card background
    TEXT_COLOR = "#f1f5f9"         # Light text
    TEXT_SECONDARY = "#94a3b8"     # Secondary text
    
    # Priority Colors
    PRIORITY_COLORS = {
        "Low": "#10b981",
        "Medium": "#f59e0b",
        "High": "#ef4444"
    }
    
    # Status Colors
    STATUS_COLORS = {
        "To-Do": "#6366f1",
        "In Progress": "#f59e0b",
        "Completed": "#10b981"
    }
    
    # Fonts
    FONT_FAMILY = "Segoe UI"
    FONT_TITLE = (FONT_FAMILY, 24, "bold")
    FONT_HEADING = (FONT_FAMILY, 18, "bold")
    FONT_SUBHEADING = (FONT_FAMILY, 14, "bold")
    FONT_NORMAL = (FONT_FAMILY, 11)
    FONT_SMALL = (FONT_FAMILY, 9)
    
    # Storage paths
    USERS_FILE = "storage/users.json"
    TASKS_FILE = "storage/tasks.json"
    LOG_FILE = "storage/activity_log.json"
