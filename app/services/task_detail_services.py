from .interfaces.task_detail_service import ITaskDetailService
from ..repositories.interfaces.task_detail_repository import ITaskDetailRepository
from ..repositories.task_detail_repository import TaskDetailRepository
from ..models import Task_Detail, Task
from typing import List, Dict, Any, Optional
from datetime import datetime

class TaskDetailService(ITaskDetailService):
    def __init__(self, task_detail_repository: ITaskDetailRepository = None):
        self.task_detail_repository = task_detail_repository or TaskDetailRepository()
    
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

            created = self.task_detail_repository.create(new_detail)
            return self._format_task_detail_data(created)
        
        except Exception as e:
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
            return self.task_detail_repository.delete(detail_id)
        except Exception as e:
            raise Exception(f"Lỗi khi xóa task detail: {str(e)}")
