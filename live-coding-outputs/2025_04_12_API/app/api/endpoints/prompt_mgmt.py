import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status, Response # Added Response

# Corrected schema imports and added missing ones
from app.schemas.prompt_mgmt import (
    PromptCreate, 
    PromptUpdate, 
    PromptResponse, 
    PaginatedPromptResponse, 
    PromptSearchQuery
)
# Corrected service import and added custom exception
from app.services.prompt_mgmt_service import (
    PromptManagementService, 
    get_prompt_mgmt_service, 
    PromptManagementServiceError
)

logger = logging.getLogger(__name__)

# Define the router with a prefix and tags for better organization in docs
router = APIRouter(
    prefix="/prompts",
    tags=["Prompt Management"]
)

# --- Phase 6: CRUD Endpoints ---

@router.post("/", response_model=PromptResponse, status_code=status.HTTP_201_CREATED)
async def create_prompt(
    prompt_in: PromptCreate,
    service: PromptManagementService = Depends(get_prompt_mgmt_service)
):
    """
    Creates a new prompt with optional tags.
    """
    try:
        # The service now returns the Prompt model instance
        created_prompt = await service.create_prompt(prompt_data=prompt_in)
        # Convert the Prompt model instance to PromptResponse schema before returning
        return PromptResponse.from_orm(created_prompt)
    except PromptManagementServiceError as e:
        logger.error(f"API Error creating prompt: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.exception("Unexpected API error creating prompt")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error creating prompt: {str(e)}"
        )

@router.get("/", response_model=PaginatedPromptResponse)
async def list_prompts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return"),
    service: PromptManagementService = Depends(get_prompt_mgmt_service)
):
    """
    Lists prompts with pagination.
    """
    try:
        prompts, total = await service.list_prompts(skip=skip, limit=limit)
        # Convert each Prompt model to PromptResponse
        items = [PromptResponse.from_orm(p) for p in prompts]
        return PaginatedPromptResponse(
            items=items,
            total=total,
            page=(skip // limit) + 1,
            size=limit
        )
    except PromptManagementServiceError as e:
        logger.error(f"API Error listing prompts: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.exception("Unexpected API error listing prompts")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error listing prompts: {str(e)}"
        )

@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
    prompt_id: int,
    service: PromptManagementService = Depends(get_prompt_mgmt_service)
):
    """
    Retrieves a specific prompt by its ID.
    """
    try:
        prompt = await service.get_prompt_by_id(prompt_id=prompt_id)
        if not prompt:
            logger.warning(f"Prompt not found in API endpoint: ID {prompt_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
        # Convert Prompt model to PromptResponse
        return PromptResponse.from_orm(prompt)
    except PromptManagementServiceError as e:
        logger.error(f"API Error getting prompt {prompt_id}: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.exception(f"Unexpected API error getting prompt {prompt_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error getting prompt: {str(e)}"
        )

@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: int,
    prompt_in: PromptUpdate,
    service: PromptManagementService = Depends(get_prompt_mgmt_service)
):
    """
    Updates an existing prompt. Allows partial updates.
    """
    try:
        updated_prompt = await service.update_prompt(prompt_id=prompt_id, prompt_data=prompt_in)
        if not updated_prompt:
            logger.warning(f"Attempted to update non-existent prompt in API: ID {prompt_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
        # Convert Prompt model to PromptResponse
        return PromptResponse.from_orm(updated_prompt)
    except PromptManagementServiceError as e:
        logger.error(f"API Error updating prompt {prompt_id}: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.exception(f"Unexpected API error updating prompt {prompt_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error updating prompt: {str(e)}"
        )

@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(
    prompt_id: int,
    service: PromptManagementService = Depends(get_prompt_mgmt_service)
):
    """
    Deletes a prompt by its ID.
    """
    try:
        deleted = await service.delete_prompt(prompt_id=prompt_id)
        if not deleted:
            logger.warning(f"Attempted to delete non-existent prompt in API: ID {prompt_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prompt not found")
        # Return No Content response
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except PromptManagementServiceError as e:
        logger.error(f"API Error deleting prompt {prompt_id}: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.exception(f"Unexpected API error deleting prompt {prompt_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error deleting prompt: {str(e)}"
        )


# --- Phase 7: Search Endpoint (Corrected) ---

# Corrected path to be relative to the router prefix "/prompts"
@router.post("/search", response_model=PaginatedPromptResponse)
async def search_prompts(
    request: PromptSearchQuery,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return"),
    service: PromptManagementService = Depends(get_prompt_mgmt_service)
):
    """
    Searches for prompts based on query text and/or tags.
    """
    try:
        prompts, total = await service.search_prompts(
            query=request.query,
            tags=request.tags,
            skip=skip,
            limit=limit
        )
        
        # FIX: Convert list of Prompt models to list of PromptResponse schemas
        items = [PromptResponse.from_orm(p) for p in prompts]
        
        return PaginatedPromptResponse(
            items=items, # Use the converted list
            total=total,
            page=(skip // limit) + 1,
            size=limit
        )
    except PromptManagementServiceError as e:
        logger.error(f"API Error searching prompts: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.exception(f"Unexpected API error searching prompts")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error searching prompts: {str(e)}"
        )
