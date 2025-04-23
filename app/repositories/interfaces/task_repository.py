from .base_repository import IRepository
from ...models import Task

class ITaskRepository(IRepository[Task]):
    """Task-specific repository interface"""
    pass