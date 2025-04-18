import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession

pytestmark = pytest.mark.asyncio

async def test_search_by_text_query(client: TestClient):
    """Test searching prompts by text query."""
    # Create some test prompts
    client.post("/api/v1/prompts/", json={"title": "Python Tutorial", "full_prompt": "Explain Python programming basics"})
    client.post("/api/v1/prompts/", json={"title": "JavaScript Guide", "full_prompt": "Explain JavaScript programming basics"})
    
    # Search for prompts containing "Python"
    response = client.post(
        "/api/v1/prompts/search",
        json={"query": "Python"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) >= 1
    assert any("Python" in item["title"] for item in data["items"])
    
async def test_search_by_tags(client: TestClient):
    """Test searching prompts by tags."""
    # Create prompts with tags
    client.post(
        "/api/v1/prompts/", 
        json={"title": "Coding in Python", "full_prompt": "Python examples", "tags": ["python", "coding"]}
    )
    client.post(
        "/api/v1/prompts/", 
        json={"title": "Web Development", "full_prompt": "HTML and CSS", "tags": ["web", "coding"]}
    )
    
    # Search by tag "python"
    response = client.post(
        "/api/v1/prompts/search",
        json={"tags": ["python"]}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) >= 1
    
    # Verify all results have the "python" tag
    for item in data["items"]:
        tag_names = [tag["name"] for tag in item["tags"]]
        assert "python" in tag_names
    
async def test_search_by_query_and_tags(client: TestClient):
    """Test searching prompts by combining text query and tags."""
    # Create sample data
    client.post(
        "/api/v1/prompts/", 
        json={"title": "Advanced Python", "full_prompt": "Advanced topics in Python", "tags": ["python", "advanced"]}
    )
    client.post(
        "/api/v1/prompts/", 
        json={"title": "Python Basics", "full_prompt": "Basic Python syntax", "tags": ["python", "beginner"]}
    )
    
    # Search for advanced Python topics
    response = client.post(
        "/api/v1/prompts/search",
        json={"query": "Advanced", "tags": ["python"]}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Verify results contain both the query term and the tag
    for item in data["items"]:
        assert "Advanced" in item["title"] or "Advanced" in item["full_prompt"]
        tag_names = [tag["name"] for tag in item["tags"]]
        assert "python" in tag_names

async def test_search_pagination(client: TestClient):
    """Test pagination of search results."""
    # Create several prompts
    for i in range(5):
        client.post(
            "/api/v1/prompts/", 
            json={"title": f"Test Prompt {i}", "full_prompt": f"Content {i}", "tags": ["test"]}
        )
    
    # Search with pagination
    response = client.post(
        "/api/v1/prompts/search?skip=0&limit=2",
        json={"tags": ["test"]}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) <= 2
    assert data["page"] == 1
    assert data["size"] == 2
    
    # Get next page
    response = client.post(
        "/api/v1/prompts/search?skip=2&limit=2",
        json={"tags": ["test"]}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["page"] == 2
