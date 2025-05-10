from .interfaces.task_repository import ITaskRepository
from ..models import db, Task, TaskAttachment, Task_Detail
from typing import List, Optional
import os
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from ..services.task_detail_services import TaskDetailService

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
    # Ham xoa tat ca cac attachment cua task
    #dung de xoa tat ca cac attachment cua task khi cap nhat task
    # neu khong dung ham nay thi phai xoa tung attachment
    def delete_all_attachments_by_task_id(self, task_id: int) -> None:
        """Delete all attachments for a task by task ID"""
        attachments = TaskAttachment.query.filter_by(task_id=task_id).all()
        for attachment in attachments:
            db.session.delete(attachment)
        db.session.commit()
    
    # ham xoa mot attachment theo id cua attachment
    # dung de xoa mot attachment khi cap nhat task

    def delete_attachment_by_id(self, attachment_id: int) -> None:
        """Delete an attachment by attachment ID"""
        attachment = TaskAttachment.query.get(attachment_id)

        if attachment:
            db.session.delete(attachment)
            db.session.commit()
            file_path = attachment.file_path.split('/uploads/')[-1]
            absolute_file_path = os.path.join(os.getcwd(), 'uploads', file_path)
            if os.path.exists(absolute_file_path):
                os.remove(absolute_file_path)
        else:
            raise ValueError(f"Tệp đính kèm với ID {attachment_id} không tồn tại.")
    
    # ham them nhieu attachment cho task theo id cua task
    # dung de them nhieu attachment cho task khi cap nhat task
    def add_attachments(self, task_id: int, file_paths: List[str]) -> List[TaskAttachment]:
        """Add multiple attachments to a task by task ID"""
        attachments = []
        for file_path in file_paths:
            attachment = TaskAttachment(
                task_id=task_id,
                file_path=file_path
            )
            db.session.add(attachment)
            attachments.append(attachment)
        db.session.commit()
        return attachments
    

    def delete(self, task_id: int) -> bool:  
        """Delete a task by ID"""
        task = self.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task với ID {task_id} không tồn tại.")

        try:
            # Sử dụng TaskDetailService để xóa các task_detail liên quan
            task_detail_service = TaskDetailService()
            task_details = db.session.query(Task_Detail).filter_by(task_id=task_id).all()

            for task_detail in task_details:
                task_detail_service.delete(task_detail.id)  # Xóa task_detail và assignees liên quan

            # Xóa các tệp đính kèm (cả bản ghi trong DB và tệp vật lý nếu cần)
            for attachment in task.attachments:
                file_path = attachment.file_path.split('/uploads/')[-1]
                absolute_file_path = os.path.join(os.getcwd(), 'uploads', file_path)

                if os.path.exists(absolute_file_path):
                    os.remove(absolute_file_path)

                db.session.delete(attachment)

            # Xóa task
            db.session.delete(task)
            db.session.commit()
            return True
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Không thể xóa task vì có ràng buộc khóa ngoại.") from e
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Lỗi không xác định khi xóa task: {str(e)}")
    def count_incomplete_task_details(self, task_id: int) -> int:
        """Count all task details with status not equal to 'Hoàn thành'"""
        return db.session.query(Task_Detail).filter(
            Task_Detail.task_id == task_id,
            Task_Detail.status != 'Hoàn thành'
        ).count()
    

