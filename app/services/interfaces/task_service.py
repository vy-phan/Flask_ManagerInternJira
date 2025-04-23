from .base_service import IBaseService
from ...models import Task

class ITaskService(IBaseService[Task]):
    """Task-specific service interface"""
    pass