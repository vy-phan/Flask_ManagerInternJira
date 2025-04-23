from .interfaces.task_detail_repository import ITaskDetailRepository
from ..models import db, Task_Detail
from typing import List, Optional

class TaskDetailRepository(ITaskDetailRepository):
    def get_all(self) -> List[Task_Detail]:
        """Lấy tất cả task detail từ database"""
        return Task_Detail.query.all()
    
    def get_by_id(self, task_detail_id: int) -> Optional[Task_Detail]:
        """Lấy task detail theo ID"""
        return Task_Detail.query.get(task_detail_id)
    
    def get_by_task_id(self, task_id: int) -> List[Task_Detail]:
        """Lấy tất cả task detail theo task_id"""
        return Task_Detail.query.filter_by(task_id=task_id).all()
    
    def create(self, task_detail: Task_Detail) -> Task_Detail:
        """Thêm mới một task detail"""
        try:
            db.session.add(task_detail)
            db.session.commit()
            return task_detail
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update(self, task_detail: Task_Detail) -> Task_Detail:
        """Cập nhật một task detail"""
        try:
            db.session.commit()
            return task_detail
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self, task_detail_id: int) -> bool:
        """Xoá một task detail theo ID"""
        task_detail = self.get_by_id(task_detail_id)
        if not task_detail:
            return False
        try:
            db.session.delete(task_detail)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
