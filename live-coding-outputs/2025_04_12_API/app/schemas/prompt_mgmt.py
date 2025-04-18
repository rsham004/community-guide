from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# --- Tag Schemas ---

class TagBase(BaseModel):
    name: str = Field(..., max_length=50)

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int
    model_config = ConfigDict(from_attributes=True) # Compatibility with ORM models

# --- Prompt Schemas ---

class PromptBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    full_prompt: str

class PromptCreate(PromptBase):
    tags: Optional[List[str]] = Field(None, description="List of tag names to associate with the prompt.")

class PromptUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    full_prompt: Optional[str] = None
    tags: Optional[List[str]] = Field(None, description="List of tag names to associate. This will replace existing tags.")

class PromptResponse(PromptBase):
    id: int
    created_at: datetime
    tags: List[TagResponse] = Field(default_factory=list) # Return associated tags
    model_config = ConfigDict(from_attributes=True)

# --- Pagination Schema ---
# Re-using the one defined previously, but placing it here for clarity if needed
# Or import from a shared location like app/schemas/common.py
class PaginatedPromptResponse(BaseModel):
    items: List[PromptResponse]
    total: int
    page: int
    size: int

# Add this if not already present
class PromptSearchQuery(BaseModel):
    query: Optional[str] = Field(None, description="Text to search for in title, description, or content")
    tags: Optional[List[str]] = Field(None, description="List of tag names to filter by (AND logic)")
