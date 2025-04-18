from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# --- Analyze ---
class AnalyzeRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="The prompt text to analyze.")

class AnalyzeResponse(BaseModel):
    clarity_score: Optional[int] = Field(None, ge=0, le=100, description="Estimated clarity score (0-100). Calculation TBD.")
    issues: List[str] = Field(default_factory=list, description="List of identified potential issues (e.g., 'Vague', 'Too Long').")
    suggestions: List[str] = Field(default_factory=list, description="Brief suggestions for improvement.")
    model_used: Optional[str] = Field(None, description="The specific LLM model used for the analysis.") # Added field

# --- Remix ---
class RemixRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="The prompt text to remix.")
    styles: Optional[List[str]] = Field(None, description="Optional list of desired remix styles (e.g., 'shorter', 'more_detailed', 'simpler_language').")
    # count: Optional[int] = Field(default=3, ge=1, le=5, description="Number of variations to generate.") # Example optional parameter

class RemixResponse(BaseModel):
    remixes: List[str] = Field(..., description="List of generated prompt variations.")

# --- Create ---
class CreateRequest(BaseModel):
    goal: str = Field(..., description="A description of the desired prompt's goal or purpose.")
    context: Optional[Dict[str, Any]] = Field(None, description="Optional dictionary providing additional context (e.g., target audience, complexity level).")

class CreateResponse(BaseModel):
    prompt: str = Field(..., description="The generated prompt string.")

# --- Shared Error Model ---
class ErrorDetail(BaseModel):
    detail: str
