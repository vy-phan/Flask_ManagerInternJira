from .interfaces.user_service import IUserService
from ..repositories.interfaces.user_repository import IUserRepository
from ..repositories.user_repository import UserRepository
from ..models import User
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
import bcrypt
import jwt
import os
from .upload_service import UploadService
from flask import Request

class UserService(IUserService):
    def __init__(self, user_repository: IUserRepository = None):
        self.user_repository = user_repository or UserRepository()
        self.upload_service = UploadService()
    
    def _format_user_data(self, user: User) -> Dict[str, Any]:
        """Format user data for API response"""
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'birth_year': user.birth_year,
            'phone': user.phone,
            'gender': user.gender,
            'avatar': user.avatar,
            'start_date': user.start_date.isoformat() if user.start_date else None,
            'cv_link': user.cv_link,
            'role': user.role.value if user.role else None,
            'is_verified': user.is_verified,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
        
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all users with formatted data"""
        users = self.user_repository.get_all()
        return [self._format_user_data(user) for user in users]
    
    def get_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Get a user by ID with formatted data"""
        user = self.user_repository.get_by_id(id)
        if not user:
            return None
        return self._format_user_data(user)
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user from request data"""
        # Hash password
        password = data['password'].encode('utf-8')  # Changed from user_data to data
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password, salt).decode('utf-8')
        
        # Parse start_date
        start_date = datetime.fromisoformat(data['start_date'])  # Changed from user_data to data
        
        # Create new user
        new_user = User(
            username=data['username'],  # Changed from user_data to data
            password_hash=password_hash,
            email=data['email'],  # Changed from user_data to data
            birth_year=data.get('birth_year'),  # Changed from user_data to data
            phone=data.get('phone'),  # Changed from user_data to data
            gender=data.get('gender', 'Nam'),  # Changed from user_data to data
            avatar=data.get('avatar'),  # Changed from user_data to data
            start_date=start_date,
            cv_link=data.get('cv_link'),  # Changed from user_data to data
            role=data.get('role'),  # Changed from user_data to data
            is_verified=data.get('is_verified', False)  # Changed from user_data to data
        )
        
        # Save to database
        created_user = self.user_repository.create(new_user)
        return self._format_user_data(created_user)
    
    def update(self, user_id: int, data: Dict[str, Any], request: Request = None) -> Dict[str, Any]:
        """Update an existing user from request data"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        # Handle file uploads if request is provided
        if request:
            # Handle avatar upload
            avatar_paths = self.upload_service.upload_files(request, 'avatar')
            if avatar_paths and len(avatar_paths) > 0:
                # Use the first uploaded avatar file
                user.avatar = avatar_paths[0]
            
            # Handle CV upload
            cv_paths = self.upload_service.upload_files(request, 'cv_link')
            if cv_paths and len(cv_paths) > 0:
                # Use the first uploaded CV file
                user.cv_link = cv_paths[0]
        
        # Update user fields from data
        if 'username' in data:
            user.username = data['username']
        if 'password' in data:
            password = data['password'].encode('utf-8')
            salt = bcrypt.gensalt()
            user.password_hash = bcrypt.hashpw(password, salt).decode('utf-8')
        if 'email' in data:
            user.email = data['email']
        if 'birth_year' in data:
            user.birth_year = data['birth_year']
        if 'phone' in data:
            user.phone = data['phone']
        if 'gender' in data:
            user.gender = data['gender']
        if 'avatar' in data and not request:  # Only update from data if not from file upload
            user.avatar = data['avatar']
        if 'start_date' in data:
            user.start_date = datetime.fromisoformat(data['start_date'])
        if 'cv_link' in data and not request:  # Only update from data if not from file upload
            user.cv_link = data['cv_link']
        if 'role' in data:
            user.role = data['role']
        if 'is_verified' in data:
            user.is_verified = data['is_verified']
        
        # Save changes
        updated_user = self.user_repository.update(user)
        return self._format_user_data(updated_user) if updated_user else None
    
    def delete(self, id: int) -> bool:
        """Delete a user by ID"""
        return self.user_repository.delete(id)

    def verify_credentials(self, email: str, password: str) -> Tuple[bool, Optional[User]]:
        """Verify user credentials and return user if valid"""
        user = self.user_repository.get_by_email(email)
        if not user:
            return False, None
            
        password_bytes = password.encode('utf-8')
        hashed_password = user.password_hash.encode('utf-8')
        if bcrypt.checkpw(password_bytes, hashed_password):
            return True, user
        return False, None
        
    def generate_access_token(self, user_id: int) -> str:
        user = self.user_repository.get_by_id(user_id)
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=15),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'role': user.role.value if user.role else None  # Thêm role vào token
        }
        return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    
    def generate_refresh_token(self, user_id: int) -> str:
        """Generate a long-lived refresh token"""
        payload = {
            'exp': datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            os.getenv('SECRET_KEY'),
            algorithm='HS256'
        )
    
    def verify_token(self, token: str) -> Tuple[bool, Optional[Dict]]:
        """Verify a JWT token and return the payload if valid"""
        try:
            payload = jwt.decode(
                token,
                os.getenv('SECRET_KEY'),
                algorithms=['HS256']
            )
            return True, payload

        # Token quá thời hạn 
        except jwt.ExpiredSignatureError:
            return False, {'error': 'Token has expired'}

        # Token không hợp lệ 
        except jwt.InvalidTokenError:
            return False, {'error': 'Invalid token'}
            
    def get_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user data from a valid token"""
        is_valid, payload = self.verify_token(token)
        if not is_valid or 'sub' not in payload:
            return None
            
        user_id = payload['sub']
        return self.get_by_id(user_id)


    
