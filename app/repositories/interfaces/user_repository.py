from .base_repository import IRepository
from ...models import User

class IUserRepository(IRepository[User]):
    """User-specific repository interface"""
    pass