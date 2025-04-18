import logging
from typing import List, Optional, Tuple, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select # select is now part of sqlalchemy directly
from sqlmodel import select # Use select from sqlmodel
from sqlalchemy import or_, and_, func, delete
from sqlalchemy.orm import selectinload, joinedload, aliased # Use selectinload for relationships, import aliased

from app.models.prompt_mgmt import Prompt, Tag, PromptTag
from app.schemas.prompt_mgmt import PromptCreate, PromptUpdate, PromptResponse, TagResponse
from app.db.session import get_async_session # Correct import for session dependency
from fastapi import Depends, HTTPException, status

logger = logging.getLogger(__name__)

class PromptManagementServiceError(Exception):
    """Custom exception for service layer errors."""
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

class PromptManagementService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_or_create_tags(self, tag_names: List[str]) -> List[Tag]:
        """Gets existing tags or creates new ones."""
        if not tag_names:
            return []

        # Find existing tags
        # Correct usage of in_ with model field
        stmt = select(Tag).where(Tag.name.in_(tag_names)) 
        result = await self.session.execute(stmt)
        existing_tags = result.scalars().all()
        existing_tag_names = {tag.name for tag in existing_tags}

        # Identify tags to create
        new_tag_names = [name for name in tag_names if name not in existing_tag_names]
        new_tags = []
        if new_tag_names:
            new_tags = [Tag(name=name) for name in new_tag_names]
            self.session.add_all(new_tags)
            # We need to flush to get IDs if we were returning them immediately,
            # but SQLAlchemy handles the association later.
            # await self.session.flush() # Not strictly needed here for association

        return list(existing_tags) + new_tags

    async def create_prompt(self, prompt_data: PromptCreate) -> Prompt:
        """Creates a new prompt with optional tags."""
        try:
            tags = await self._get_or_create_tags(prompt_data.tags or [])
            
            db_prompt = Prompt(
                title=prompt_data.title,
                description=prompt_data.description,
                full_prompt=prompt_data.full_prompt,
                tags=tags # Associate tags directly
            )
            self.session.add(db_prompt)
            await self.session.commit()
            await self.session.refresh(db_prompt, attribute_names=['tags']) # Refresh to load relationships
            logger.info(f"Prompt created with ID: {db_prompt.id}")
            return db_prompt
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"Error creating prompt: {e}")
            raise PromptManagementServiceError(f"Database error creating prompt: {str(e)}")

    async def get_prompt_by_id(self, prompt_id: int) -> Optional[Prompt]:
        """Retrieves a single prompt by its ID, including associated tags."""
        try:
            # Use selectinload to efficiently load the tags relationship
            stmt = select(Prompt).options(selectinload(Prompt.tags)).where(Prompt.id == prompt_id)
            result = await self.session.execute(stmt)
            prompt = result.scalar_one_or_none()
            if prompt:
                logger.debug(f"Prompt found with ID: {prompt_id}")
            else:
                logger.warning(f"Prompt not found with ID: {prompt_id}")
            return prompt
        except Exception as e:
            logger.exception(f"Error retrieving prompt {prompt_id}: {e}")
            raise PromptManagementServiceError(f"Database error retrieving prompt: {str(e)}")

    async def list_prompts(self, skip: int = 0, limit: int = 20) -> Tuple[Sequence[Prompt], int]:
        """Lists prompts with pagination, including tags."""
        try:
            # Count total prompts
            count_stmt = select(func.count()).select_from(Prompt)
            total_result = await self.session.execute(count_stmt)
            total = total_result.scalar_one()

            # Fetch paginated prompts with tags
            # Correct usage of desc with model field
            stmt = select(Prompt).options(selectinload(Prompt.tags)).offset(skip).limit(limit).order_by(Prompt.created_at.desc()) 
            result = await self.session.execute(stmt)
            prompts = result.scalars().all()
            logger.debug(f"Listed {len(prompts)} prompts (skip={skip}, limit={limit}, total={total})")
            return prompts, total
        except Exception as e:
            logger.exception(f"Error listing prompts: {e}")
            raise PromptManagementServiceError(f"Database error listing prompts: {str(e)}")

    async def update_prompt(self, prompt_id: int, prompt_data: PromptUpdate) -> Optional[Prompt]:
        """Updates an existing prompt."""
        try:
            db_prompt = await self.get_prompt_by_id(prompt_id) # Reuse get method to load prompt and tags
            if not db_prompt:
                logger.warning(f"Attempted to update non-existent prompt ID: {prompt_id}")
                return None

            update_data = prompt_data.dict(exclude_unset=True)

            # Handle tag updates separately
            if "tags" in update_data:
                tag_names = update_data.pop("tags") # Remove tags from main update data
                if tag_names is None: # Explicitly setting tags to null/empty
                     db_prompt.tags = []
                else:
                    db_prompt.tags = await self._get_or_create_tags(tag_names)

            # Update other fields
            for key, value in update_data.items():
                 setattr(db_prompt, key, value)

            self.session.add(db_prompt)
            await self.session.commit()
            await self.session.refresh(db_prompt, attribute_names=['tags']) # Refresh to load updated relationships
            logger.info(f"Prompt updated with ID: {prompt_id}")
            return db_prompt
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"Error updating prompt {prompt_id}: {e}")
            raise PromptManagementServiceError(f"Database error updating prompt: {str(e)}")

    async def delete_prompt(self, prompt_id: int) -> bool:
        """Deletes a prompt by its ID."""
        try:
            # Need to manually delete associations first if cascade isn't set up perfectly
            # For simplicity here, we assume cascade delete works or handle potential FK violations
            # A more robust way might involve deleting from PromptTag first.

            stmt = delete(Prompt).where(Prompt.id == prompt_id)
            result = await self.session.execute(stmt)
            await self.session.commit()

            if result.rowcount == 0:
                 logger.warning(f"Attempted to delete non-existent prompt ID: {prompt_id}")
                 return False
            else:
                 logger.info(f"Prompt deleted with ID: {prompt_id}")
                 return True
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"Error deleting prompt {prompt_id}: {e}")
            # Check for specific FK violation errors if needed
            raise PromptManagementServiceError(f"Database error deleting prompt: {str(e)}")


    async def search_prompts(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        skip: int = 0,
        limit: int = 20
    ) -> Tuple[Sequence[Prompt], int]:
        """Searches for prompts by query text and/or tags."""
        try:
            stmt = select(Prompt).options(selectinload(Prompt.tags))
            filters = []
            if query:
                # Correct usage of ilike with model fields
                query_filter = or_(
                    Prompt.title.ilike(f"%{query}%"), 
                    Prompt.description.ilike(f"%{query}%"), 
                    Prompt.full_prompt.ilike(f"%{query}%") 
                )
                filters.append(query_filter)

            if tags:
                # Ensure prompt has ALL specified tags
                # Correct usage of in_ with model field
                tag_filter_stmt = select(Tag.id).where(Tag.name.in_(tags)) 
                tag_ids = (await self.session.execute(tag_filter_stmt)).scalars().all()
                
                if len(tag_ids) != len(tags):
                     # One of the requested tags doesn't exist, so no prompt can match all tags
                     logger.debug(f"Search query included non-existent tags: {tags}. Returning empty.")
                     return [], 0

                # Subquery to find prompts linked to ALL required tags
                prompt_alias = aliased(PromptTag)
                subquery = (
                    select(prompt_alias.prompt_id)
                    .where(prompt_alias.tag_id.in_(tag_ids))
                    .group_by(prompt_alias.prompt_id)
                    .having(func.count(prompt_alias.tag_id) == len(tag_ids))
                )
                # Correct usage of in_ with model field
                filters.append(Prompt.id.in_(select(subquery.c.prompt_id))) 


            if filters:
                stmt = stmt.where(and_(*filters))

            # Get total count matching filters
            count_stmt = select(func.count()).select_from(stmt.subquery()) # Count from the filtered statement
            total_result = await self.session.execute(count_stmt)
            total = total_result.scalar_one()

            # Apply ordering, pagination and execute final query
            # Correct usage of desc with model field
            final_stmt = stmt.order_by(Prompt.created_at.desc()).offset(skip).limit(limit) 
            result = await self.session.execute(final_stmt)
            prompts = result.scalars().unique().all() # Use unique() because of joins/loads

            logger.debug(f"Searched prompts (query='{query}', tags={tags}, skip={skip}, limit={limit}). Found {len(prompts)} of {total} total.")
            return prompts, total

        except Exception as e:
            logger.exception(f"Error searching prompts: {e}")
            raise PromptManagementServiceError(f"Database error searching prompts: {str(e)}")


# Dependency function
async def get_prompt_mgmt_service(
    session: AsyncSession = Depends(get_async_session)
) -> PromptManagementService:
    """Provides an instance of the PromptManagementService."""
    return PromptManagementService(session=session)
