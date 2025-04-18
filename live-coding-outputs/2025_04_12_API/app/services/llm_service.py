import httpx
import logging
from typing import List, Dict, Any, Optional
import json

import openai
from openai import AsyncOpenAI, APIError, AuthenticationError, RateLimitError, APIConnectionError
from pydantic import ValidationError # Import ValidationError

from app.core.config import settings
from app.schemas.prompt import AnalyzeRequest, AnalyzeResponse, RemixRequest, RemixResponse, CreateRequest, CreateResponse

logger = logging.getLogger(__name__)

class LLMServiceError(Exception):
    """Custom exception for LLM service errors."""
    def __init__(self, detail: str, status_code: int = 500): # Add status_code
        self.detail = detail
        self.status_code = status_code # Store appropriate HTTP status
        super().__init__(self.detail)

class LLMService:
    """
    Service class to interact with the OpenAI API.
    """
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        if not api_key or api_key == "YOUR_LLM_API_KEY_HERE":
            logger.warning("LLM_API_KEY is not configured or is set to the default placeholder.")
            # Raise a specific error if the key is missing/invalid for OpenAI
            raise LLMServiceError("OpenAI API key is missing or invalid.", status_code=500)

        try:
            # Initialize the AsyncOpenAI client
            self._client = AsyncOpenAI(
                api_key=api_key,
                base_url=base_url, # Pass base_url if provided (for proxies etc.)
                timeout=30.0
            )
            logger.info("AsyncOpenAI client initialized.")
        except Exception as e:
            logger.exception("Failed to initialize AsyncOpenAI client.")
            raise LLMServiceError(f"Failed to initialize OpenAI client: {e}", status_code=500)

    async def close(self):
        """Closes the underlying OpenAI client's resources (if applicable)."""
        # The AsyncOpenAI client uses httpx internally, which should ideally be closed.
        # However, the OpenAI library doesn't expose a direct close method easily.
        # We rely on the underlying httpx client managed by the library to handle connections.
        # If resource leakage becomes an issue, further investigation is needed.
        logger.info("LLMService close called (OpenAI client resources managed internally).")
        pass # No explicit close needed for openai client itself currently

    # Update return type hint to include model name
    async def _call_openai_chat(self, messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo", temperature: float = 0.7, max_tokens: int = 250) -> tuple[str, str]:
        """Helper function to call the OpenAI Chat Completions API. Returns (content, model_name)."""
        try:
            logger.debug(f"Calling OpenAI API. Model: {model}, Temp: {temperature}, Max Tokens: {max_tokens}")
            response = await self._client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = response.choices[0].message.content
            model_used = response.model # Get the exact model string used by OpenAI
            logger.debug(f"OpenAI API response received from model {model_used}: {content[:100]}...")
            if not content:
                 raise LLMServiceError("Received empty response from OpenAI.", status_code=503)
            # Return both content and model name
            return content.strip(), model_used
        except AuthenticationError as e:
            logger.error(f"OpenAI Authentication Error: {e}")
            raise LLMServiceError("OpenAI API key is invalid or expired.", status_code=500) from e
        except RateLimitError as e:
            logger.error(f"OpenAI Rate Limit Error: {e}")
            raise LLMServiceError("OpenAI API rate limit exceeded. Please try again later.", status_code=429) from e
        except APIConnectionError as e:
            logger.error(f"OpenAI API Connection Error: {e}")
            raise LLMServiceError("Could not connect to OpenAI API. Please check network or configuration.", status_code=503) from e
        except APIError as e: # Catch broader OpenAI API errors
            logger.error(f"OpenAI API Error: Status={getattr(e, 'status_code', 'N/A')}, Message={getattr(e, 'message', str(e))}")
            # Use getattr for safety, default to 503 if status_code isn't present
            status_code = getattr(e, 'status_code', 503) or 503
            message = getattr(e, 'message', str(e))
            raise LLMServiceError(f"OpenAI API returned an error: {message}", status_code=status_code) from e
        except Exception as e:
            logger.exception("An unexpected error occurred during OpenAI API call.")
            # Use 503 as a general fallback for unexpected issues during the call
            raise LLMServiceError(f"Unexpected error communicating with OpenAI: {str(e)}", status_code=503) from e

    async def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        """Analyzes a prompt using the OpenAI API."""
        # --- Updated System Message ---
        system_message = """
You are an expert AI assistant specializing in prompt engineering. Your task is to analyze user-provided prompts for clarity, effectiveness, and potential issues when used with another AI model.

Respond ONLY with a valid JSON object containing three keys:
1.  `clarity_score`: An integer score from 0 to 100, representing how clear, specific, and actionable the prompt is (0=very unclear, 100=crystal clear).
2.  `issues`: A list of strings identifying potential problems. Be specific. Examples:
    *   "Ambiguous request": The goal isn't clear.
    *   "Lacks context": Important background information is missing.
    *   "Missing constraints": Doesn't specify output format, length, or style.
    *   "Target audience unclear": Doesn't specify who the output is for.
    *   "Potentially too complex/broad": The request might be too large for a single prompt.
    *   "Leading or biased language": The prompt might unduly influence the AI's response.
    *   "Conflicting instructions": Contains contradictory requirements.
3.  `suggestions`: A list of short, actionable strings suggesting concrete improvements. Examples:
    *   "Specify the desired output format (e.g., JSON, bullet points)."
    *   "Define the target audience (e.g., 'explain to a 5th grader', 'write for experts')."
    *   "Add context about [specific topic]."
    *   "Break down the request into smaller steps."
    *   "Provide examples of the desired output."
    *   "Clarify the meaning of '[ambiguous term]'."
    *   "Set a desired length or level of detail."

Analyze the user's prompt based on these criteria. If the prompt is excellent, the score should be high, and issues/suggestions lists can be empty.

Example Response for a weak prompt "Tell me about dogs":
{
  "clarity_score": 40,
  "issues": ["Ambiguous request", "Lacks context", "Missing constraints", "Potentially too broad"],
  "suggestions": ["Specify what you want to know about dogs (e.g., breeds, care, history).", "Define the desired output format or length."]
}

Example Response for a good prompt "Write a short python function that takes a list of integers and returns the sum.":
{
  "clarity_score": 95,
  "issues": [],
  "suggestions": []
}
"""
        # --- End of Updated System Message ---

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Analyze the following prompt:\n\n{request.prompt}"}
        ]

        # Use lower temperature for more deterministic analysis
        raw_response, model_used = await self._call_openai_chat(messages, temperature=0.2, max_tokens=300) # Increased max_tokens slightly

        try:
            # --- Start of indented block ---
            # Attempt to parse the JSON response from the LLM
            response_data = json.loads(raw_response)
            # Validate structure (basic check)
            if not all(k in response_data for k in ["clarity_score", "issues", "suggestions"]):
                 raise ValueError("LLM response missing required keys.")
            # Further validation could be done here if needed (e.g., type checks)
            analysis_response = AnalyzeResponse(**response_data)
            analysis_response.model_used = model_used
            return analysis_response
            # --- End of indented block ---
        except (json.JSONDecodeError, ValueError, TypeError, ValidationError) as e:
            logger.error(f"Failed to parse or validate LLM response for analyze: {e}\nRaw response: {raw_response}")
            raise LLMServiceError(f"Failed to process response from LLM: Invalid format. Details: {e}", status_code=500)


    async def remix(self, request: RemixRequest) -> RemixResponse:
        """Remixes a prompt using the OpenAI API."""
        styles_description = ", ".join(request.styles) if request.styles else "various creative styles (e.g., shorter, more detailed, simpler language)"
        system_message = f"""
You are an AI assistant that remixes prompts.
Generate exactly 3 variations of the user's prompt based on the following styles/guidelines: {styles_description}.
Respond ONLY with a JSON object containing a single key 'remixes', which is a list of 3 strings (the remixed prompts).
Example Response: {{"remixes": ["Variation 1...", "Variation 2...", "Variation 3..."]}}
"""
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Remix the following prompt:\n\n{request.prompt}"}
        ]

        # Use higher temperature for more creative variations
        raw_response, _ = await self._call_openai_chat(messages, temperature=0.8, max_tokens=500) # Allow more tokens for 3 variations

        try:
            response_data = json.loads(raw_response)
            if "remixes" not in response_data or not isinstance(response_data["remixes"], list):
                 raise ValueError("LLM response missing 'remixes' list.")
            # Ensure we return exactly 3 remixes if possible, pad/truncate if necessary (optional)
            # response_data["remixes"] = response_data["remixes"][:3]
            # while len(response_data["remixes"]) < 3:
            #     response_data["remixes"].append("...") # Placeholder if LLM didn't provide enough

            return RemixResponse(**response_data)
        except (json.JSONDecodeError, ValueError, TypeError, ValidationError) as e:
            logger.error(f"Failed to parse or validate LLM response for remix: {e}\nRaw response: {raw_response}")
            raise LLMServiceError(f"Failed to process response from LLM: Invalid format. Details: {e}", status_code=500)


    async def create(self, request: CreateRequest) -> CreateResponse:
        """Creates a prompt using the OpenAI API."""
        context_str = f"\nAdditional Context: {json.dumps(request.context)}" if request.context else ""
        system_message = """
You are an AI assistant that generates high-quality prompts based on a user's goal and context.
Create a clear, specific, and actionable prompt suitable for another AI model.
Respond ONLY with a JSON object containing a single key 'prompt', which is the generated prompt string.
Example Response: {"prompt": "Generated prompt text..."}
"""
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Generate a prompt for the following goal:\nGoal: {request.goal}{context_str}"}
        ]

        # Moderate temperature for reliable generation
        raw_response, _ = await self._call_openai_chat(messages, temperature=0.6, max_tokens=300)

        try:
            response_data = json.loads(raw_response)
            if "prompt" not in response_data or not isinstance(response_data["prompt"], str):
                 raise ValueError("LLM response missing 'prompt' string.")
            return CreateResponse(**response_data)
        except (json.JSONDecodeError, ValueError, TypeError, ValidationError) as e:
            logger.error(f"Failed to parse or validate LLM response for create: {e}\nRaw response: {raw_response}")
            raise LLMServiceError(f"Failed to process response from LLM: Invalid format. Details: {e}", status_code=500)


# --- Singleton Pattern for LLM Service ---
# ... existing get_llm_service and close_llm_service functions ...
# (No changes needed here, they will now instantiate the updated LLMService)

_llm_service_instance: Optional[LLMService] = None

async def get_llm_service() -> LLMService:
    """
    Dependency function to get the singleton LLMService instance.
    Initializes the service on first call.
    """
    global _llm_service_instance
    # Reset instance if settings change (e.g., during tests or dynamic config reload)
    # This is a simple approach; more robust handling might be needed in complex scenarios.
    # if _llm_service_instance and (_llm_service_instance.api_key != settings.LLM_API_KEY or _llm_service_instance.base_url != settings.LLM_API_BASE_URL):
    #     logger.warning("LLM settings changed, re-initializing LLMService.")
    #     await close_llm_service() # Close old instance if possible
    #     _llm_service_instance = None

    if _llm_service_instance is None:
        logger.info("Initializing LLMService instance...")
        try:
            _llm_service_instance = LLMService(
                api_key=settings.LLM_API_KEY,
                base_url=settings.LLM_API_BASE_URL
            )
        except LLMServiceError as e:
            # Log the initialization error and re-raise to prevent app startup if critical
            logger.error(f"Fatal error initializing LLM Service: {e.detail}")
            raise e # Prevent app from starting if LLM service can't init
    return _llm_service_instance

async def close_llm_service():
    """Function to close the LLM service client during application shutdown."""
    global _llm_service_instance
    if _llm_service_instance:
        logger.info("Closing LLMService client...")
        await _llm_service_instance.close()
        _llm_service_instance = None
