# Mock Stock Market Data API (Prototype)

This project provides a simple FastAPI application that serves mock stock market data (quotes and historical prices) for development, testing, and educational purposes.

## Features

*   Get latest mock quotes for predefined symbols (e.g., `MOCK`, `FAKE`, `TEST`, `SMPL`, `DEMO`).
*   Get mock historical OHLCV data for symbols within a specified date range.
*   Automatic API documentation via Swagger UI (`/docs`) and ReDoc (`/redoc`).
*   Uses FastAPI, SQLModel, and SQLite (via `aiosqlite`).

## Project Structure

```
.
├── app/                  # Main application code
│   ├── api/              # API endpoints (routers)
│   ├── core/             # Configuration (if needed later)
│   ├── crud/             # Data generation logic
│   ├── db/               # Database session management
│   ├── models/           # SQLModel definitions
│   └── main.py           # FastAPI app entry point
├── docs/                 # Project documentation (PRD, SA, DA, API, Plan)
├── prompts/              # Prompts used for generation (if applicable)
├── tests/                # Tests (to be added in Phase 5)
├── .env                  # Environment variables (contains DATABASE_URL)
├── .gitignore            # Git ignore file (to be added)
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## Setup and Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment (using uv):**
    ```bash
    # Create the virtual environment (uv typically creates it in .venv)
    uv venv
    # Activate the environment
    # On Windows (Command Prompt/PowerShell)
    .\.venv\Scripts\activate
    # On macOS/Linux (bash/zsh)
    source .venv/bin/activate
    ```

3.  **Install dependencies (using uv):**
    ```bash
    uv pip install -r requirements.txt
    ```

## Running the Application

1.  **Ensure the `.env` file exists** in the project root directory with the `DATABASE_URL` defined (it should be created by the setup process). The default is:
    ```
    DATABASE_URL="sqlite+aiosqlite:///./mock_stock.db"
    ```

2.  **Run the FastAPI server using Uvicorn:**
    From the project root directory (where `app/` and `README.md` are located):
    ```bash
    uvicorn app.main:app --reload
    ```
    *   `app.main:app` tells Uvicorn where to find the FastAPI `app` instance.
    *   `--reload` enables auto-reloading when code changes (useful for development).

3.  **Access the API:**
    *   The API will typically be running at `http://127.0.0.1:8000`.
    *   Access the interactive documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.
    *   Access the alternative documentation (ReDoc) at `http://127.0.0.1:8000/redoc`.

## API Endpoints

*   `GET /api/v1/symbols/`: Get a list of available mock symbols.
*   `GET /api/v1/quotes/{symbol}`: Get the latest mock quote for a specific symbol.
*   `GET /api/v1/historical/{symbol}`: Get mock historical data for a symbol.
    *   Query Parameters: `start_date` (YYYY-MM-DD), `end_date` (YYYY-MM-DD). Defaults to the last 30 days.

## Running Tests

1.  **Ensure you have installed the development dependencies:**
    Make sure `pytest` and `httpx` are installed (they are included in `requirements.txt`). If you haven't installed them yet:
    ```bash
    uv pip install -r requirements.txt
    ```

2.  **Run pytest from the project root directory:**
    Make sure your virtual environment is activated.
    ```bash
    pytest
    ```
    Pytest will automatically discover and run the tests in the `tests/` directory. You should see output indicating the tests passing.

## Next Steps (Phase 5)

*   Implement unit and integration tests.
*   Add `.gitignore`.
*   Refine mock data generation logic if needed.
