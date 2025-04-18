import logging
import json
from datetime import datetime
from typing import Optional, Any, Dict, Union
from pydantic import BaseModel
from fastapi import Request, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.log import ApiLog

logger = logging.getLogger(__name__)

def _serialize_payload(payload: Optional[Any]) -> Optional[str]:
    """Safely serialize payload to JSON string."""
    if payload is None:
        return None
    try:
        if isinstance(payload, BaseModel):
            # Use Pydantic's serialization for its models
            return payload.model_dump_json()
        elif isinstance(payload, dict) or isinstance(payload, list):
             # Use standard json for dicts/lists
             return json.dumps(payload)
        else:
             # Attempt to convert other types to string
             return str(payload)
    except Exception as e:
        logger.error(f"Failed to serialize payload for logging: {e}", exc_info=True)
        return json.dumps({"error": "Serialization failed", "details": str(e)})

class LoggingService:
    """Service for logging API requests and responses."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_request(
        self,
        request: Request,
        response: Optional[Response] = None,
        status_code: Optional[int] = None,
        processing_time_ms: Optional[float] = None,
        error_detail: Optional[str] = None,
    ) -> ApiLog:
        """
        Logs details of an API request and its response to the database.
        
        Args:
            request: The FastAPI request object.
            response: The FastAPI response object (optional).
            status_code: Override response status code (useful for errors).
            processing_time_ms: Processing time in milliseconds.
            error_detail: Optional error message for failed requests.
            
        Returns:
            The created ApiLog entry.
        """
        try:
            # Extract endpoint from request
            endpoint = f"{request.method} {request.url.path}"
            
            # Extract and serialize request body if available
            request_body = None
            if hasattr(request, "body"):
                try:
                    # Try to decode request body
                    if await request.body():
                        # Handle both JSON and form data
                        if request.headers.get("content-type", "").startswith("application/json"):
                            try:
                                body_json = await request.json()
                                request_body = json.dumps(body_json)
                            except json.JSONDecodeError:
                                body_text = (await request.body()).decode("utf-8")
                                request_body = f"Non-JSON body: {body_text[:500]}..." if len(body_text) > 500 else body_text
                        else:
                            # For non-JSON requests, just store as string with content type
                            body_text = (await request.body()).decode("utf-8")
                            content_type = request.headers.get("content-type", "unknown")
                            request_body = f"Content-Type: {content_type}, Body: {body_text[:500]}..." if len(body_text) > 500 else body_text
                except Exception as e:
                    logger.warning(f"Failed to extract request body: {e}")
                    request_body = f"Error extracting request body: {str(e)}"
            
            # Extract response data or use error detail
            response_data = None
            if response:
                # For responses, get status code from response or override
                status_code = status_code or response.status_code
                
                # Attempt to get response body - this is complex with FastAPI
                # In reality, we would need middleware to capture the response body before sending
                # For now, just use error_detail or a placeholder
                response_data = error_detail or "Response body not captured in prototype"
            else:
                # If no response object (e.g., during error handling), use the status code and error detail
                status_code = status_code or 500  # Default to 500 if no status provided
                response_data = error_detail or "No response data available"
            
            # Create ApiLog entry
            log_entry = ApiLog(
                endpoint=endpoint,
                request_payload=request_body,
                response_payload=response_data,
                status_code=status_code,
                processing_time_ms=processing_time_ms
            )
            
            # Save to database
            self.session.add(log_entry)
            await self.session.commit()
            await self.session.refresh(log_entry)
            
            logger.debug(f"API request logged: {endpoint} - Status: {status_code}")
            return log_entry
            
        except Exception as e:
            logger.error(f"Failed to log API request: {e}", exc_info=True)
            # Don't re-raise; logging shouldn't break the API
            return None
