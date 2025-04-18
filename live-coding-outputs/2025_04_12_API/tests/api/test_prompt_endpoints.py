import pytest
from httpx import AsyncClient
from fastapi import status
import respx # Import respx if mocking LLM calls during integration tests

from app.models.log import ApiLog # To check logs
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio

# --- Analyze Endpoint Tests ---

@respx.mock # Mock LLM for integration tests to avoid real calls
async def test_analyze_prompt_success(test_client: AsyncClient, db_session: AsyncSession):
    """Test successful analysis via API."""
    # Mock the LLM service call expected by this endpoint
    # Assuming LLMService uses settings.LLM_API_BASE_URL which might be None
    # Need to determine the actual base_url used by the service instance
    # For simplicity, let's assume a default or mock it if needed
    mock_base_url = "https://api.example-llm.com/v1" # Or get from settings/service
    respx.post(f"{mock_base_url}/analyze").mock(
        return_value=respx.Response(
            status.HTTP_200_OK,
            json={"clarity_score": 85, "issues": [], "suggestions": ["Looks good!"]}
        )
    )

    request_payload = {"prompt": "A valid prompt"}
    response = await test_client.post("/api/v1/prompts/analyze", json=request_payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["clarity_score"] == 85
    assert data["issues"] == []
    assert data["suggestions"] == ["Looks good!"]

    # Verify logging (optional but good)
    statement = select(ApiLog).where(ApiLog.endpoint == "/api/v1/prompts/analyze")
    log_results = await db_session.exec(statement)
    log_entry = log_results.one_or_none()
    assert log_entry is not None
    assert log_entry.status_code == status.HTTP_200_OK
    assert request_payload["prompt"] in log_entry.request_payload
    assert "Looks good!" in log_entry.response_payload

async def test_analyze_prompt_validation_error(test_client: AsyncClient):
    """Test validation error for analyze endpoint."""
    response = await test_client.post("/api/v1/prompts/analyze", json={"prompt": ""}) # Empty prompt
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@respx.mock
async def test_analyze_prompt_llm_failure(test_client: AsyncClient, db_session: AsyncSession):
    """Test 503 error when LLM service fails."""
    mock_base_url = "https://api.example-llm.com/v1"
    respx.post(f"{mock_base_url}/analyze").mock(
        return_value=respx.Response(status.HTTP_500_INTERNAL_SERVER_ERROR)
    )

    request_payload = {"prompt": "A valid prompt"}
    response = await test_client.post("/api/v1/prompts/analyze", json=request_payload)

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert "LLM API error: 500" in response.json()["detail"] # Check detail from exception handler

    # Verify logging of the error
    statement = select(ApiLog).where(ApiLog.endpoint == "/api/v1/prompts/analyze")
    log_results = await db_session.exec(statement)
    log_entry = log_results.one_or_none()
    assert log_entry is not None
    assert log_entry.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert "LLM API error: 500" in log_entry.response_payload # Check logged error detail

# --- Remix Endpoint Tests ---
# Add similar tests for /remix (success, validation, LLM failure)

# --- Create Endpoint Tests ---
# Add similar tests for /create (success, validation, LLM failure)

# --- Health Check Test ---
async def test_health_check(test_client: AsyncClient):
    """Test the health check endpoint."""
    response = await test_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
