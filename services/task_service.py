
from models.task import Task
from data.storage import Storage
from config.settings import Config
from datetime import datetime, timedelta

class TaskService:
    """Task management service"""
    
    @staticmethod
    def get_all_tasks():
        """Get all tasks from storage"""
        tasks_data = Storage.read_json(Config.TASKS_FILE, default=[])
        return [Task.from_dict(t) for t in tasks_data]
    
    @staticmethod
    def save_tasks(tasks):
        """Save tasks to storage"""
        tasks_data = [t.to_dict() for t in tasks]
        return Storage.write_json(Config.TASKS_FILE, tasks_data)
    
    @staticmethod
    def create_task(title, description, priority, status, due_date, owner_email):
        """Create a new task"""
        tasks = TaskService.get_all_tasks()
        
        new_task = Task(
            title=title,
            description=description,
            priority=priority,
            status=status,
            due_date=due_date,
            owner_email=owner_email
        )
        
        tasks.append(new_task)
        TaskService.save_tasks(tasks)
        Storage.log_activity(owner_email, "Task Created", title)
        
        return True, "Task created successfully"
    
    @staticmethod
    def get_user_tasks(email):
        """Get tasks for a specific user"""
        all_tasks = TaskService.get_all_tasks()
        return [t for t in all_tasks if t.owner_email == email]
    
    @staticmethod
    def update_task(task_id, **kwargs):
        """Update task fields"""
        tasks = TaskService.get_all_tasks()
        
        for task in tasks:
            if task.task_id == task_id:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                
                TaskService.save_tasks(tasks)
                Storage.log_activity(task.owner_email, "Task Updated", task.title)
                return True, "Task updated successfully"
        
        return False, "Task not found"
    
    @staticmethod
    def delete_task(task_id, user_email, is_admin=False):
        """Delete a task"""
        tasks = TaskService.get_all_tasks()
        
        for i, task in enumerate(tasks):
            if task.task_id == task_id:
                if is_admin or task.owner_email == user_email:
                    tasks.pop(i)
                    TaskService.save_tasks(tasks)
                    Storage.log_activity(user_email, "Task Deleted", task.title)
                    return True, "Task deleted successfully"
                return False, "You don't have permission to delete this task"
        
        return False, "Task not found"
    
    @staticmethod
    def get_upcoming_tasks(email):
        """Get tasks due within 24 hours"""
        user_tasks = TaskService.get_user_tasks(email)
        upcoming = []
        now = datetime.now()
        
        for task in user_tasks:
            if task.due_date and task.status != "Completed":
                try:
                    due = datetime.strptime(task.due_date, "%Y-%m-%d")
                    if now <= due <= now + timedelta(days=1):
                        upcoming.append(task)
                except ValueError:
                    pass
        
        return upcoming
    
    @staticmethod
    def get_overdue_tasks(email):
        """Get overdue tasks"""
        user_tasks = TaskService.get_user_tasks(email)
        overdue = []
        now = datetime.now()
        
        for task in user_tasks:
            if task.due_date and task.status != "Completed":
                try:
                    due = datetime.strptime(task.due_date, "%Y-%m-%d")
                    if due < now:
                        overdue.append(task)
                except ValueError:
                    pass
        
        return overdue
    
    @staticmethod
    def get_task_statistics(email, is_admin=False):
        """Get task statistics"""
        if is_admin:
            tasks = TaskService.get_all_tasks()
        else:
            tasks = TaskService.get_user_tasks(email)
        
        total = len(tasks)
        completed = len([t for t in tasks if t.status == "Completed"])
        in_progress = len([t for t in tasks if t.status == "In Progress"])
        todo = len([t for t in tasks if t.status == "To-Do"])
        
        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "todo": todo
        }