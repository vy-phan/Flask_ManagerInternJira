from ..models import db, Task_Detail_Assignees
from typing import List, Optional

class TaskDetailAssigneeRepository:
    def create(self, assignee: Task_Detail_Assignees) -> Task_Detail_Assignees:
        """Create a new task detail assignee"""
        try:
            db.session.add(assignee)
            db.session.commit()
            return assignee
        except Exception as e:
            db.session.rollback()
            raise e

    def get_by_task_detail_id(self, task_detail_id: int) -> List[Task_Detail_Assignees]:
        """Get all assignees for a specific task detail"""
        return Task_Detail_Assignees.query.filter_by(task_detail_id=task_detail_id).all()

    def get_by_user_id(self, user_id: int) -> List[Task_Detail_Assignees]:
        """Get all task details assigned to a specific user"""
        return Task_Detail_Assignees.query.filter_by(user_id=user_id).all()

    def delete(self, assignee_id: int) -> bool:
        """Delete a task detail assignee by ID"""
        assignee = Task_Detail_Assignees.query.get(assignee_id)
        if not assignee:
            return False
        try:
            db.session.delete(assignee)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, assignee_id: int, **kwargs) -> Optional[Task_Detail_Assignees]:
        """
        Update a task detail assignee by ID.
        kwargs: fields to update (e.g., name=value)
        Returns the updated assignee or None if not found.
        """
        assignee = Task_Detail_Assignees.query.get(assignee_id)
        if not assignee:
            return None
        try:
            for key, value in kwargs.items():
                if hasattr(assignee, key):
                    setattr(assignee, key, value)
            db.session.commit()
            return assignee
        except Exception as e:
            db.session.rollback()
            raise e