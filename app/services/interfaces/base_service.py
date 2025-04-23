from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, TypeVar, Generic

T = TypeVar('T')

class IBaseService(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all entities with formatted data"""
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Get an entity by ID with formatted data"""
        pass
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new entity from request data"""
        pass
    
    @abstractmethod
    def update(self, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing entity from request data"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete an entity by ID"""
        pass