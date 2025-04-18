import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.prompt_mgmt import Prompt, Tag, PromptTag

pytestmark = pytest.mark.asyncio

async def test_create_prompt(db_session: AsyncSession):
    """Test creating a basic prompt."""
    prompt = Prompt(title="Test Title", full_prompt="Test content")
    db_session.add(prompt)
    await db_session.commit()
    await db_session.refresh(prompt)
    
    assert prompt.id is not None
    assert prompt.title == "Test Title"
    assert prompt.full_prompt == "Test content"
    assert prompt.tags == []  # No tags initially

async def test_create_tag(db_session: AsyncSession):
    """Test creating a tag."""
    tag = Tag(name="test_tag")
    db_session.add(tag)
    await db_session.commit()
    await db_session.refresh(tag)
    
    assert tag.id is not None
    assert tag.name == "test_tag"
    assert tag.prompts == []  # No prompts associated yet

async def test_prompt_tag_association(db_session: AsyncSession):
    """Test associating prompts with tags."""
    # Create prompt and tags
    prompt = Prompt(title="Tagged Prompt", full_prompt="Has tags")
    tag1 = Tag(name="tag1")
    tag2 = Tag(name="tag2")
    
    # Add to session and associate
    db_session.add(prompt)
    db_session.add(tag1)
    db_session.add(tag2)
    await db_session.commit()
    
    # Associate tags with prompt
    prompt.tags = [tag1, tag2]
    await db_session.commit()
    
    # Query to verify association
    stmt = select(Prompt).where(Prompt.id == prompt.id)
    result = await db_session.exec(stmt)
    fetched_prompt = result.one()
    
    assert len(fetched_prompt.tags) == 2
    assert {tag.name for tag in fetched_prompt.tags} == {"tag1", "tag2"}

    # Verify relationship from tag side
    stmt = select(Tag).where(Tag.name == "tag1")
    result = await db_session.exec(stmt)
    fetched_tag = result.one()
    
    assert len(fetched_tag.prompts) == 1
    assert fetched_tag.prompts[0].title == "Tagged Prompt"

async def test_unique_tag_name_constraint(db_session: AsyncSession):
    """Test that tag names must be unique."""
    # Create first tag
    tag1 = Tag(name="unique_tag")
    db_session.add(tag1)
    await db_session.commit()
    
    # Try to create another tag with same name
    tag2 = Tag(name="unique_tag")
    db_session.add(tag2)
    
    # Should fail with IntegrityError due to unique constraint
    with pytest.raises(Exception) as excinfo:
        await db_session.commit()
    
    # SQLite will report UNIQUE constraint failed error
    assert "UNIQUE constraint failed" in str(excinfo.value) or "unique constraint" in str(excinfo.value).lower()
    await db_session.rollback()
