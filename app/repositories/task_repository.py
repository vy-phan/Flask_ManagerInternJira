from .interfaces.task_repository import ITaskRepository
from ..models import db, Task, TaskAttachment, Task_Detail
from typing import List, Optional
import os
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

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
        
    def get_attachment_by_id(self, attachment_id: int) -> TaskAttachment | None:
        return TaskAttachment.query.get(attachment_id)
        
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
        """Delete a task by ID"""
        task = self.get_by_id(task_id)
        if not task:
            return False
        
        try:
            # Xóa tất cả các bản ghi trong bảng task_details liên quan đến task
            db.session.query(Task_Detail).filter_by(task_id=task_id).delete()

            # Xóa các tệp đính kèm (cả bản ghi trong DB và tệp vật lý nếu cần)
            for attachment in task.attachments:
                # Lấy đường dẫn file từ file_path
                file_path = attachment.file_path.split('/uploads/')[-1]  # Lấy tên file từ đường dẫn
                absolute_file_path = os.path.join(os.getcwd(), 'uploads', file_path)  # Tạo đường dẫn tuyệt đối

                # Xóa tệp vật lý nếu tồn tại
                if os.path.exists(absolute_file_path):
                    os.remove(absolute_file_path)

                # Xóa bản ghi đính kèm trong DB
                db.session.delete(attachment)

            # Sau khi xóa tất cả các đính kèm và task_details, xóa task
            db.session.delete(task)
            db.session.commit()
            return True
        except IntegrityError as e:  # Bắt lỗi khóa ngoại
            db.session.rollback()
            raise ValueError("Không thể xóa task vì có chi tiết công việc liên quan.") from e
        except Exception as e:
            db.session.rollback()
            raise e
    def count_incomplete_task_details(self, task_id: int) -> int:
        """Count all task details with status not equal to 'Hoàn thành'"""
        return db.session.query(Task_Detail).filter(
            Task_Detail.task_id == task_id,
            Task_Detail.status != 'Hoàn thành'
        ).count()

