from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# --- Tagging ---

# Join table for Many-to-Many relationship between Prompt and Tag
# Needs to be defined before the models that use it if not using string references
class PromptTag(SQLModel, table=True):
    prompt_id: Optional[int] = Field(
        default=None, foreign_key="prompt.id", primary_key=True
    )
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )

class TagBase(SQLModel):
    name: str = Field(index=True, unique=True, max_length=50) # Added max_length

class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prompts: List["Prompt"] = Relationship(back_populates="tags", link_model=PromptTag)

# --- Core Prompt ---

class PromptBase(SQLModel):
    title: str = Field(index=True, max_length=255) # Added max_length
    description: Optional[str] = Field(default=None)
    full_prompt: str # SQLite uses TEXT implicitly for large strings
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    # updated_at: Optional[datetime] = Field(default=None, index=True) # Add later if needed

class Prompt(PromptBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tags: List[Tag] = Relationship(back_populates="prompts", link_model=PromptTag)

# --- Schemas for API interaction will be in app/schemas/prompt_mgmt.py ---
# Define Read/Create schemas separately to avoid exposing relationship lists directly in create requests
# and to control what's returned in responses.
