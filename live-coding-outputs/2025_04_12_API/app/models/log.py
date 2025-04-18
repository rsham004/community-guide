from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ApiLogBase(SQLModel):
    """
    Base model for API log entries, containing common fields.
    """
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True, nullable=False)
    endpoint: str = Field(index=True, nullable=False)
    request_payload: Optional[str] = Field(default=None) # Store as JSON string
    response_payload: Optional[str] = Field(default=None) # Store as JSON string
    status_code: int = Field(index=True, nullable=False)
    processing_time_ms: Optional[float] = Field(default=None)

class ApiLog(ApiLogBase, table=True):
    """
    Database table model for API log entries. Includes the primary key.
    """
    __tablename__ = "api_log" # Explicit table name is good practice

    id: Optional[int] = Field(default=None, primary_key=True)

# Note: Storing payloads as TEXT (implied by str) is sufficient for the prototype.
# For complex JSON querying later, consider specific JSON types if the DB supports them well.
