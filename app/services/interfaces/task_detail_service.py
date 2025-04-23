from .base_service import IBaseService
from ...models import Task_Detail

class ITaskDetailService(IBaseService[Task_Detail]):
    """Task_Detail-specific service interface"""
    pass