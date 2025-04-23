from .interfaces.task_service import ITaskService
from ..repositories.interfaces.task_repository import ITaskRepository
from ..repositories.task_repository import TaskRepository
from ..models import Task, TaskAttachment  # Nhập thêm TaskAttachment
from typing import List, Optional, Dict, Any
from datetime import datetime

class TaskService(ITaskService):
    def __init__(self, task_repository: ITaskRepository = None):
        self.task_repository = task_repository or TaskRepository()
    
    def _format_task_data(self, task: Task) -> Dict[str, Any]:
        """Format task data for API response"""
        return {
            'id': task.id,
            'code': task.code,
            'title': task.title,
            'description': task.description,
            'deadline': task.deadline.isoformat() if task.deadline else None,
            'status': task.status,
            'created_by': task.created_by,
            'created_at': task.created_at.isoformat() if task.created_at else None,
            'attachments': [  # Thêm thông tin tệp đính kèm
                {
                    'id': attachment.id,
                    'file_path': attachment.file_path,
                    'uploaded_at': attachment.uploaded_at.isoformat() if attachment.uploaded_at else None
                }
                for attachment in task.attachments
            ]
        }
        
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all tasks with formatted data"""
        tasks = self.task_repository.get_all()
        return [self._format_task_data(task) for task in tasks]
    
    def get_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get a task by ID with formatted data"""
        task = self.task_repository.get_by_id(task_id)
        if not task:
            return None
        return self._format_task_data(task)
    
    def create(self, data: Dict[str, Any], file_paths: List[str] = None) -> Dict[str, Any]:
        """Create a new task from request data and handle attachments"""
        try:
            # Validate required fields
            required_fields = ['code', 'title', 'deadline', 'created_by']
            for field in required_fields:
                if field not in data or not data[field]:
                    raise ValueError(f"Missing required field: {field}")

            # Validate deadline
            deadline = datetime.fromisoformat(data['deadline'])
            
            # Validate status with Vietnamese values
            valid_statuses = ['Đã giao', 'Đang thực hiện', 'Đã hoàn thành']
            status = data.get('status', 'Đã giao')
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")

            # Create new task
            new_task = Task(
                code=data['code'],
                title=data['title'],
                description=data.get('description'),
                deadline=deadline,
                status=status,
                created_by=data['created_by']
            )
            
            # Save task to database
            created_task = self.task_repository.create(new_task)

            # Lưu các tệp đính kèm nếu có
            if file_paths:
                for file_path in file_paths:
                    self.task_repository.create_attachment(created_task.id, file_path)

            # Format and return the created task
            return self._format_task_data(created_task)
            
        except Exception as e:
            raise Exception(f"Error creating task: {str(e)}")
    
    def update(self, task_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing task from request data"""
        try:
            task = self.task_repository.get_by_id(task_id)
            if not task:
                raise ValueError(f"Task with ID {task_id} not found")
            
            # Convert English status to Vietnamese if needed
            status_map = {
                'assigned': 'Đã giao',
                'in_progress': 'Đang thực hiện',
                'completed': 'Đã hoàn thành'
            }
            if 'status' in data:
                data['status'] = status_map.get(data['status'], data['status'])
                
            # Validate status with Vietnamese values
            valid_statuses = ['Đã giao', 'Đang thực hiện', 'Đã hoàn thành']
            if 'status' in data and data['status'] not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")

            # Update task fields from data
            if 'code' in data:
                task.code = data['code']
            if 'title' in data:
                task.title = data['title']
            if 'description' in data:
                task.description = data['description']
            if 'deadline' in data:
                task.deadline = datetime.fromisoformat(data['deadline'])
            if 'status' in data:
                task.status = data['status']
            if 'created_by' in data:
                task.created_by = data['created_by']
            
            # Save changes
            updated_task = self.task_repository.update(task)
            return self._format_task_data(updated_task) if updated_task else None
            
        except Exception as e:
            raise Exception(f"Error updating task: {str(e)}")
    
    def delete(self, task_id: int) -> bool:
        """Delete a task by ID"""
        try:
            return self.task_repository.delete(task_id)
        except Exception as e:
            raise Exception(f"Error deleting task: {str(e)}")