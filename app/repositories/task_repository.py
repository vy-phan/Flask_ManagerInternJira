from .interfaces.task_repository import ITaskRepository
from ..models import db, Task, TaskAttachment
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
        
    def create_attachment(self, task_id: int, file_path: str) -> TaskAttachment:
        """Create a new attachment for a task"""
        try:
            attachment = TaskAttachment(
                task_id=task_id,
                file_path=file_path
            )
            db.session.add(attachment)
            db.session.commit()
            return attachment
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
    
    def delete(self, task_id: int) -> bool:
        """Delete a task by ID and its attachments"""
        task = self.get_by_id(task_id)
        if not task:
            return False
        
        try:
            # Xóa các tệp đính kèm (cả bản ghi trong DB và tệp vật lý nếu cần)
            for attachment in task.attachments:
                # Xóa tệp vật lý (tùy chọn)
                if os.path.exists(attachment.file_path):
                    os.remove(attachment.file_path)
                db.session.delete(attachment)
            
            # Xóa nhiệm vụ
            db.session.delete(task)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e