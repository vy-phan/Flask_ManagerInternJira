# Import interfaces
from .interfaces.user_repository import IUserRepository
from .upload_repository import UploadRepository

# Import implementations
from .user_repository import UserRepository

# Export classes for easy import
__all__ = ['IUserRepository', 'UserRepository']