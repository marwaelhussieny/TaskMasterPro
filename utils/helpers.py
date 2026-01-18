
from datetime import datetime, timedelta

def format_date(date_str):
    """Format date string to readable format"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str

def is_overdue(due_date):
    """Check if a date is overdue"""
    try:
        due = datetime.strptime(due_date, "%Y-%m-%d")
        return due < datetime.now()
    except:
        return False

def is_upcoming(due_date, days=1):
    """Check if date is within specified days"""
    try:
        due = datetime.strptime(due_date, "%Y-%m-%d")
        now = datetime.now()
        return now <= due <= now + timedelta(days=days)
    except:
        return False

def truncate_text(text, max_length=80):
    """Truncate text with ellipsis"""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def get_today():
    """Get today's date in YYYY-MM-DD format"""
    return datetime.now().strftime("%Y-%m-%d")
