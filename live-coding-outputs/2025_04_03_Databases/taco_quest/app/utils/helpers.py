from typing import Any, Dict, List, Optional, Type, TypeVar, Generic, Union
from sqlmodel import SQLModel, select, Session

# Define a generic type for SQLModel subclasses
T = TypeVar('T', bound=SQLModel)

class CRUDHelper(Generic[T]):
    """
    Generic class to handle CRUD operations for SQLModel classes
    """
    
    def __init__(self, model: Type[T]):
        self.model = model
    
    def create(self, session: Session, obj_in: Union[Dict[str, Any], T]) -> T:
        """Create a new record"""
        if isinstance(obj_in, dict):
            obj_data = obj_in
            db_obj = self.model(**obj_data)
        else:
            db_obj = obj_in
        
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj
    
    def get(self, session: Session, id: int) -> Optional[T]:
        """Get a record by ID"""
        return session.get(self.model, id)
    
    def get_multi(
        self, session: Session, *, skip: int = 0, limit: int = 100
    ) -> List[T]:
        """Get multiple records with pagination"""
        statement = select(self.model).offset(skip).limit(limit)
        return session.exec(statement).all()
    
    def update(
        self, session: Session, *, db_obj: T, obj_in: Union[Dict[str, Any], T]
    ) -> T:
        """Update a record"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj
    
    def delete(self, session: Session, *, id: int) -> T:
        """Delete a record"""
        obj = session.get(self.model, id)
        if obj:
            session.delete(obj)
            session.commit()
        return obj

# Create CRUD helpers for each model (to be imported where needed)
def get_crud_helper(model: Type[SQLModel]) -> CRUDHelper:
    """Get a CRUD helper for a specific model"""
    return CRUDHelper(model)
