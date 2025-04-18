import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime

from app.services.logging_service import log_request, _serialize_payload
from app.models.log import ApiLog
from app.schemas.prompt import AnalyzeRequest, AnalyzeResponse

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio

async def test_log_request_success(db_session: AsyncSession):
    """Test successfully logging a request."""
    endpoint = "/test/endpoint"
    status_code = 200
    req_payload = AnalyzeRequest(prompt="test")
    resp_payload = AnalyzeResponse(clarity_score=90, issues=[], suggestions=[])
    timestamp = datetime.utcnow()
    processing_time = 123.45

    await log_request(
        db=db_session,
        endpoint=endpoint,
        status_code=status_code,
        request_payload=req_payload,
        response_payload=resp_payload,
        timestamp=timestamp,
        processing_time_ms=processing_time
    )
    # The commit happens via the fixture's context manager

    # Verify the log entry was created in the test DB
    statement = select(ApiLog).where(ApiLog.endpoint == endpoint)
    results = await db_session.exec(statement)
    log_entry = results.one_or_none() # Use one_or_none for safety

    assert log_entry is not None
    assert log_entry.endpoint == endpoint
    assert log_entry.status_code == status_code
    assert log_entry.timestamp == timestamp
    assert log_entry.processing_time_ms == processing_time
    assert log_entry.request_payload == req_payload.model_dump_json()
    assert log_entry.response_payload == resp_payload.model_dump_json()

def test_serialize_payload():
    """Test payload serialization helper."""
    assert _serialize_payload(None) is None
    assert _serialize_payload({"key": "value"}) == '{"key": "value"}'
    assert _serialize_payload(AnalyzeRequest(prompt="test")) == '{"prompt":"test"}'
    assert _serialize_payload(123) == "123"
    # Test potential error case (though unlikely with standard types)
    class Unserializable: pass
    assert '"error": "Serialization failed"' in _serialize_payload(Unserializable())

# Add tests for edge cases, like logging failures (though hard to test without mocking DB errors)
