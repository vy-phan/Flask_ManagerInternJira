# Import interfaces
from .user_repository import IUserRepository
from .task_repository import ITaskRepository

# Export interfaces for easy import
__all__ = ['IUserRepository', 'ITaskRepository']