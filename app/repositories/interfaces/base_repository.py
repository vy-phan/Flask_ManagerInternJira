from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')

class IRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities from the database"""
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Get an entity by ID"""
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an existing entity"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete an entity by ID"""
        pass