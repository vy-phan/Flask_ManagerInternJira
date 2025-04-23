from .interfaces.task_repository import ITaskRepository
from ..models import db, Task
from typing import List, Optional

class TaskRepository(ITaskRepository):
    def get_all(self) -> List[Task]:  # Changed from get_all_tasks
        """Get all tasks from the database"""
        return Task.query.all()
    
    def get_by_id(self, task_id: int) -> Optional[Task]:  # Changed from get_by_id_
        """Get a task by ID"""
        return Task.query.get(task_id)
    
    def create(self, task: Task) -> Task:  # Changed from create_task
        """Create a new task"""
        try:
            db.session.add(task)
            db.session.commit()
            return task
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update(self, task: Task) -> Task:  # Changed from update_task
        """Update an existing task"""
        try:
            db.session.commit()
            return task
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self, task_id: int) -> bool:  # Changed from delete_task
        """Delete a task by ID"""
        task = self.get_by_id(task_id)
        if not task:
            return False
        
        try:
            db.session.delete(task)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e