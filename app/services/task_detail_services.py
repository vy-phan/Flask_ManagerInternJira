from .interfaces.task_detail_service import ITaskDetailService
from ..repositories.interfaces.task_detail_repository import ITaskDetailRepository
from ..repositories.task_detail_repository import TaskDetailRepository
from ..models import db,Task_Detail, Task
from ..models.task_detail_assignees import Task_Detail_Assignees
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..repositories.user_repository import UserRepository
from ..repositories.task_detail_assignee_repository import TaskDetailAssigneeRepository

class TaskDetailService(ITaskDetailService):
    def __init__(self, task_detail_repository: ITaskDetailRepository = None):
        self.task_detail_repository = task_detail_repository or TaskDetailRepository()
        self.task_detail_assignee_repository = TaskDetailAssigneeRepository()  # New repository
    
    def _format_task_detail_data(self, detail: Task_Detail) -> Dict[str, Any]:
        return {
            'id': detail.id,
            'task_id': detail.task_id,
            'title': detail.title,
            'description': detail.description,
            'status': detail.status,
            'created_at': detail.created_at.isoformat() if detail.created_at else None,
            'updated_at': detail.updated_at.isoformat() if detail.updated_at else None
        }

    def get_all(self) -> List[Dict[str, Any]]:
        details = self.task_detail_repository.get_all()
        return [self._format_task_detail_data(detail) for detail in details]

    def get_by_task_id(self, task_id: int) -> List[Dict[str, Any]]:
        details = self.task_detail_repository.get_by_task_id(task_id)
        return [self._format_task_detail_data(detail) for detail in details]



    def get_by_id(self, detail_id: int) -> Optional[Dict[str, Any]]:
        detail = self.task_detail_repository.get_by_id(detail_id)
        return self._format_task_detail_data(detail) if detail else None

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            task_id = data.get('task_id')
            title = data.get('title')
            description = data.get('description', '')
            status = data.get('status', 'Đã giao')
            assignees = data.get('assignees', [])  # List of usernames

            if not all([task_id, title]):
                raise ValueError("Các trường task_id và title là bắt buộc")

            # Kiểm tra task cha có tồn tại
            task = Task.query.get(task_id)
            if not task:
                raise LookupError(f"Task với ID {task_id} không tồn tại")

            new_detail = Task_Detail(
                task_id=task_id,
                title=title,
                description=description,
                status=status,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            # Save Task_Detail
            created_detail = self.task_detail_repository.create(new_detail)

            # Save Task_Detail_Assignees
            user_repo = UserRepository()
            for username in assignees:
                user = user_repo.get_by_username(username)
                if not user:
                    raise LookupError(f"User với username '{username}' không tồn tại")
                new_assignee = Task_Detail_Assignees(
                    task_detail_id=created_detail.id,
                    user_id=user.id,
                    assigned_at=datetime.utcnow()
                )
                self.task_detail_assignee_repository.create(new_assignee)

            return self._format_task_detail_data(created_detail)
        
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Lỗi khi tạo task detail: {str(e)}")

    def update(self, detail_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            detail = self.task_detail_repository.get_by_id(detail_id)
            if not detail:
                raise LookupError("Task detail không tồn tại")

            if 'title' in data:
                detail.title = data['title']
            if 'description' in data:
                detail.description = data['description']
            if 'status' in data:
                detail.status = data['status']

            detail.updated_at = datetime.utcnow()

            updated = self.task_detail_repository.update(detail)
            return self._format_task_detail_data(updated)

        except Exception as e:
            raise Exception(f"Lỗi khi cập nhật task detail: {str(e)}")

    def delete(self, detail_id: int) -> bool:
        try:
            # Get the task detail by ID
            detail = self.task_detail_repository.get_by_id(detail_id)
            if not detail:
                return False

            # Delete related task_detail_assignees
            assignees = self.task_detail_assignee_repository.get_by_task_detail_id(detail_id)
            for assignee in assignees:
                self.task_detail_assignee_repository.delete(assignee.id)

            # Delete the task detail
            return self.task_detail_repository.delete(detail_id)
        except Exception as e:
            raise Exception(f"Lỗi khi xóa task detail: {str(e)}")
