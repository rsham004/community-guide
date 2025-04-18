import pytest
import respx
from httpx import Response

from app.services.llm_service import LLMService, LLMServiceError, get_llm_service, close_llm_service
from app.schemas.prompt import AnalyzeRequest, RemixRequest, CreateRequest

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio

@pytest.fixture(autouse=True)
async def manage_llm_service():
    """Ensure LLM service is initialized before tests and closed after."""
    await get_llm_service() # Initialize
    yield
    await close_llm_service() # Close

@respx.mock
async def test_analyze_success():
    """Test successful analyze call."""
    llm_service = await get_llm_service()
    mock_url = f"{llm_service.base_url}/analyze"
    mock_response_payload = {
        "clarity_score": 80,
        "issues": ["Slightly vague"],
        "suggestions": ["Add more context"]
    }
    respx.post(mock_url).mock(return_value=Response(200, json=mock_response_payload))

    request = AnalyzeRequest(prompt="Test prompt")
    response = await llm_service.analyze(request)

    assert response.clarity_score == 80
    assert response.issues == ["Slightly vague"]
    assert response.suggestions == ["Add more context"]
    assert respx.calls.call_count == 1
    call = respx.calls.last
    assert call.request.url == mock_url
    assert await call.request.read() == b'{"prompt":"Test prompt","analysis_type":"clarity_and_issues"}' # Check payload

@respx.mock
async def test_analyze_llm_error():
    """Test analyze call when LLM returns an error."""
    llm_service = await get_llm_service()
    mock_url = f"{llm_service.base_url}/analyze"
    respx.post(mock_url).mock(return_value=Response(500, text="Internal LLM Error"))

    request = AnalyzeRequest(prompt="Test prompt")
    with pytest.raises(LLMServiceError, match="LLM API error: 500"):
        await llm_service.analyze(request)

# Add similar tests for remix and create, testing success and error cases
async def test_remix_success():
    # ... similar setup using respx ...
    pass

async def test_create_success():
    # ... similar setup using respx ...
    pass
