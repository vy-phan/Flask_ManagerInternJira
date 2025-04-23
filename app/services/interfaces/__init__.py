# Import interfaces
from .user_service import IUserService
from .task_service import ITaskService
from .task_detail_service import ITaskDetailService

# Export interfaces for easy import
__all__ = ['IUserService', 'ITaskService', 'ITaskDetailService'	]