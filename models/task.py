
from datetime import datetime
import uuid

class Task:
    """Task model representing a user task"""
    
    def __init__(self, task_id=None, title="", description="", priority="Medium",
                 status="To-Do", due_date=None, owner_email="", created_at=None):
        self.task_id = task_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.owner_email = owner_email
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self):
        """Convert task to dictionary"""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date,
            "owner_email": self.owner_email,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create task from dictionary"""
        return cls(**data)