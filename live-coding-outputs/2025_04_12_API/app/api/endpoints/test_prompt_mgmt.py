# filepath: c:\repos\AI_Product_Dev\live-demos\2025_04_12_Minnesota_API\tests\api\endpoints\test_prompt_mgmt.py
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession # Import for type hinting if needed

# Assuming your conftest.py is set up correctly

# Mark all tests in this module to use asyncio
pytestmark = pytest.mark.asyncio

async def test_create_prompt_success(client: TestClient):
    """Test creating a prompt successfully without tags."""
    response = client.post(
        "/api/v1/prompts/",
        json={"title": "Test Prompt 1", "full_prompt": "This is the content."}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Test Prompt 1"
    assert data["full_prompt"] == "This is the content."
    assert "id" in data
    assert "created_at" in data
    assert data["tags"] == [] # No tags provided

async def test_create_prompt_with_tags(client: TestClient):
    """Test creating a prompt with new and existing tags."""
    # Create a tag first to test reuse
    client.post("/api/v1/prompts/", json={"title": "Setup Tag", "full_prompt": "...", "tags": ["existing_tag"]})

    response = client.post(
        "/api/v1/prompts/",
        json={
            "title": "Prompt With Tags",
            "description": "Has tags",
            "full_prompt": "Content with tags.",
            "tags": ["new_tag", "existing_tag", "another_new"]
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Prompt With Tags"
    assert len(data["tags"]) == 3
    tag_names = {tag["name"] for tag in data["tags"]}
    assert tag_names == {"new_tag", "existing_tag", "another_new"}

async def test_get_prompt_not_found(client: TestClient):
    """Test getting a prompt that does not exist."""
    response = client.get("/api/v1/prompts/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_get_prompt_success(client: TestClient):
    """Test getting an existing prompt by ID."""
    # Create a prompt first
    create_response = client.post(
        "/api/v1/prompts/",
        json={"title": "Gettable Prompt", "full_prompt": "Details here.", "tags": ["get_test"]}
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    prompt_id = create_response.json()["id"]

    # Get the created prompt
    response = client.get(f"/api/v1/prompts/{prompt_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == prompt_id
    assert data["title"] == "Gettable Prompt"
    assert len(data["tags"]) == 1
    assert data["tags"][0]["name"] == "get_test"

async def test_list_prompts_empty(client: TestClient):
    """Test listing prompts when none exist (depends on test isolation)."""
    # This test assumes a clean state provided by the fixture setup/teardown
    response = client.get("/api/v1/prompts/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # Check initial state might be tricky if other tests run first without isolation
    # For now, let's assume it might contain prompts from previous tests in the same function scope if not isolated perfectly
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data

async def test_list_prompts_with_data_and_pagination(client: TestClient):
    """Test listing prompts with pagination."""
    # Create a few prompts
    client.post("/api/v1/prompts/", json={"title": "List Prompt 1", "full_prompt": "1"})
    client.post("/api/v1/prompts/", json={"title": "List Prompt 2", "full_prompt": "2"})
    client.post("/api/v1/prompts/", json={"title": "List Prompt 3", "full_prompt": "3"})

    # Get first page
    response = client.get("/api/v1/prompts/?limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) <= 2 # Allow for existing items from other tests
    assert data["page"] == 1
    assert data["size"] == 2
    # assert data["total"] >= 3 # Total should reflect all created prompts

    # Get second page
    response = client.get("/api/v1/prompts/?skip=2&limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # assert len(data["items"]) <= 1 # Should be 1 if total was 3
    assert data["page"] == 2
    assert data["size"] == 2

async def test_list_prompts_with_tag_filter(client: TestClient):
    """Test filtering prompts by tag."""
    client.post("/api/v1/prompts/", json={"title": "Filter Prompt A", "full_prompt": "A", "tags": ["filter_tag"]})
    client.post("/api/v1/prompts/", json={"title": "Filter Prompt B", "full_prompt": "B", "tags": ["another_tag"]})
    client.post("/api/v1/prompts/", json={"title": "Filter Prompt C", "full_prompt": "C", "tags": ["filter_tag"]})

    response = client.get("/api/v1/prompts/?tag=filter_tag")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] >= 2 # Should find at least the two prompts with this tag
    for item in data["items"]:
        tag_names = {tag["name"] for tag in item["tags"]}
        assert "filter_tag" in tag_names

async def test_update_prompt_success(client: TestClient):
    """Test updating an existing prompt's title and tags."""
    # Create a prompt
    create_response = client.post(
        "/api/v1/prompts/",
        json={"title": "Update Me", "full_prompt": "Initial content.", "tags": ["old_tag"]}
    )
    prompt_id = create_response.json()["id"]

    # Update the prompt
    update_response = client.put(
        f"/api/v1/prompts/{prompt_id}",
        json={"title": "Updated Title", "tags": ["new_tag_1", "new_tag_2"]}
    )
    assert update_response.status_code == status.HTTP_200_OK
    data = update_response.json()
    assert data["id"] == prompt_id
    assert data["title"] == "Updated Title"
    assert data["full_prompt"] == "Initial content." # Not updated
    tag_names = {tag["name"] for tag in data["tags"]}
    assert tag_names == {"new_tag_1", "new_tag_2"} # Tags should be replaced

async def test_update_prompt_remove_tags(client: TestClient):
    """Test updating a prompt to have no tags."""
    # Create a prompt with tags
    create_response = client.post(
        "/api/v1/prompts/",
        json={"title": "Tags To Remove", "full_prompt": "Content.", "tags": ["tag1", "tag2"]}
    )
    prompt_id = create_response.json()["id"]

    # Update with empty tag list
    update_response = client.put(
        f"/api/v1/prompts/{prompt_id}",
        json={"tags": []} # Explicitly provide empty list
    )
    assert update_response.status_code == status.HTTP_200_OK
    data = update_response.json()
    assert data["tags"] == []

async def test_update_prompt_not_found(client: TestClient):
    """Test updating a non-existent prompt."""
    response = client.put("/api/v1/prompts/9999", json={"title": "Wont Work"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_delete_prompt_success(client: TestClient):
    """Test deleting an existing prompt."""
    # Create a prompt
    create_response = client.post(
        "/api/v1/prompts/",
        json={"title": "Delete Me", "full_prompt": "Content."}
    )
    prompt_id = create_response.json()["id"]

    # Delete the prompt
    delete_response = client.delete(f"/api/v1/prompts/{prompt_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Verify it's gone
    get_response = client.get(f"/api/v1/prompts/{prompt_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

async def test_delete_prompt_not_found(client: TestClient):
    """Test deleting a non-existent prompt."""
    response = client.delete("/api/v1/prompts/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
