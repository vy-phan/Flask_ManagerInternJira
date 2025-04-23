from .base_service import IBaseService
from ...models import User

class IUserService(IBaseService[User]):
    """User-specific service interface"""
    pass