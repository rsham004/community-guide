from fastapi import APIRouter

# Import both endpoint modules
from app.api.endpoints import prompts, prompt_mgmt 

api_router = APIRouter()

# Include endpoint routers here
# This router handles /analyze, /remix, /create etc. (Phase 3)
api_router.include_router(prompts.router, prefix="/prompts", tags=["Prompt Actions"]) 

# This router handles CRUD and search for saved prompts (Phase 6 & 7)
# It already has the "/prompts" prefix defined within its own router definition
api_router.include_router(prompt_mgmt.router, tags=["Prompt Management"]) 

# Add other resource routers later if needed
# e.g., api_router.include_router(users.router, prefix="/users", tags=["Users"])
