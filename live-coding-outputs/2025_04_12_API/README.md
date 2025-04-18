# PromptSculptor API (Prototype v1)

This repository contains the source code for the PromptSculptor API prototype, designed for analyzing, remixing, creating, and managing AI prompts.

## Prerequisites

*   Python 3.10+
*   [uv](https://github.com/astral-sh/uv) (for environment and package management)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    uv venv
    source .venv/bin/activate  # Linux/macOS
    # .\.venv\Scripts\activate  # Windows (Command Prompt)
    # .\.venv\Scripts\Activate.ps1 # Windows (PowerShell)
    ```

3.  **Install dependencies:**
    *(Assuming a requirements.txt file exists or will be created)*
    ```bash
    uv pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    *   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
        *(Note: You might need to create `.env.example` first if it doesn't exist, or just rename/copy the existing `.env`)*
    *   Edit the `.env` file:
        *   Replace `"YOUR_LLM_API_KEY_HERE"` with your actual API key for the chosen Large Language Model provider. **Keep this file secret and do not commit it to version control.**
        *   Adjust `DATABASE_URL` if needed (the default `sqlite+aiosqlite:///./promptsculptor_proto.db` should work for local development).
        *   Set `LLM_API_BASE_URL` if you are using a proxy or self-hosted model.

## Running the Application

1.  **Ensure the virtual environment is activated:**
    (If not already active from setup)
    ```bash
    source .venv/bin/activate  # Linux/macOS
    # .\.venv\Scripts\activate  # Windows (Command Prompt)
    # .\.venv\Scripts\Activate.ps1 # Windows (PowerShell)
    ```

2.  **Start the FastAPI server:**
    The `uvicorn` command will start the server. The `--reload` flag enables auto-reloading during development when code changes are detected.
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

3.  **Access the API:**
    *   The API will be available at `http://localhost:8000`.
    *   Auto-generated documentation (Swagger UI) is available at `http://localhost:8000/docs`.
    *   Alternative documentation (ReDoc) is available at `http://localhost:8000/redoc`.

## API Endpoints

The API is available at `http://localhost:8000`. All endpoints below are relative to this base URL.

### Prompt Actions (LLM Interaction)
These endpoints interact directly with the configured Large Language Model.

*   `POST /prompts/analyze`: Analyzes a given prompt's clarity, issues, and potential improvements.
*   `POST /prompts/remix`: Generates variations of a given prompt based on specified styles or parameters.
*   `POST /prompts/create`: Generates a new prompt based on a specified goal or description.

### Prompt Management (CRUD & Search)
These endpoints manage the storage, retrieval, and organization of prompts saved in the database.

*   `POST /prompts/`: Creates a new prompt record in the database with title, description, full prompt text, and optional tags.
*   `GET /prompts/`: Lists saved prompts with pagination.
*   `GET /prompts/{prompt_id}`: Retrieves a specific saved prompt by its unique ID.
*   `PUT /prompts/{prompt_id}`: Updates an existing saved prompt (title, description, full prompt, tags). Allows partial updates.
*   `DELETE /prompts/{prompt_id}`: Deletes a specific saved prompt by its ID.
*   `POST /prompts/search`: Searches saved prompts based on keywords in the title, description, or full prompt text, and/or by associated tags. Returns paginated results.

## Running Tests

1.  **Ensure development dependencies are installed:**
    *   If using Poetry: `poetry install --with dev`
    *   If using uv + requirements: `uv pip install pytest pytest-asyncio httpx`

2.  **Activate the virtual environment:**
    (If not already active)
    ```bash
    # Poetry:
    poetry shell
    # uv:
    source .venv/bin/activate # Linux/macOS
    # .\.venv\Scripts\activate # Windows
    ```

3.  **Run pytest:**
    From the project root directory:
    ```bash
    pytest
    ```
    Or with options (e.g., verbose):
    ```bash
    pytest -v
    ```

## Development Plan

Refer to the `design_docs/05_Plan.md` for the implementation plan and next tasks.

## License

[MIT License](LICENSE)
