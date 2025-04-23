from .interfaces.user_repository import IUserRepository
from ..models import db, User
from typing import List, Optional

class UserRepository(IUserRepository):
    def get_all(self) -> List[User]:
        """Get all users from the database"""
        return User.query.all()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        return User.query.get(user_id)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        return User.query.filter_by(username=username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        return User.query.filter_by(email=email).first()
    
    # Add error handling for database operations
    def create(self, user: User) -> User:
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e
    
    # Similar for update/delete methods
    def update(self, user: User) -> User:
        """Update an existing user"""
        db.session.commit()
        return user
    
    def delete(self, user_id: int) -> bool:
        """Delete a user by ID"""
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True