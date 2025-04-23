from .base_repository import IRepository
from ...models import Task_Detail

class ITaskDetailRepository(IRepository[Task_Detail]):
    """Task_Detail-specific repository interface"""
    pass