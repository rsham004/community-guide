# API Design Specification: Mock Stock Market Data API (Prototype)

## 1. API Overview

*   **Summary:** This API provides realistic but mock stock market data (quotes, historical prices) via a simple RESTful interface. It's intended for development, testing, and educational purposes as a prototype, utilizing FastAPI, SQLModel, and SQLite.
*   **OpenAPI Docs:** `/docs` (Swagger UI), `/redoc` (ReDoc) - Provided automatically by FastAPI.

## 2. Project Structure

A standard FastAPI project structure will be used:

```
.
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI app instance, middleware, lifespan events
│   ├── core/           # Core logic, configuration
│   │   ├── __init__.py
│   │   └── config.py
│   ├── crud/           # Data access logic (Create, Read, Update, Delete) - May be simple for mock data
│   │   ├── __init__.py
│   │   └── crud_stock.py
│   ├── db/             # Database session management
│   │   ├── __init__.py
│   │   └── session.py
│   ├── models/         # SQLModel definitions (from DA.md)
│   │   ├── __init__.py
│   │   └── stock.py
│   ├── schemas/        # Pydantic schemas (derived/used for API I/O - may overlap with models)
│   │   ├── __init__.py
│   │   └── stock.py
│   └── api/
│       ├── __init__.py
│       ├── deps.py       # Dependency injection functions (e.g., get_db)
│       └── routers/
│           ├── __init__.py
│           └── stocks.py   # Router for stock-related endpoints
├── tests/              # Unit and integration tests
├── .env                # Environment variables
├── requirements.txt    # Project dependencies
└── README.md
```

## 3. Core Dependencies

*   `fastapi`: The web framework.
*   `uvicorn[standard]`: ASGI server.
*   `sqlmodel`: ORM and data validation.
*   `sqlite+aiosqlite`: Async SQLite database driver.
*   `python-dotenv`: For managing environment variables.
*   `datetime`, `random`: For mock data generation.

## 4. Authentication & Authorization

*   **Method:** None for this prototype. All endpoints are publicly accessible.

## 5. Pydantic & SQLModel Models

*   **SQLModel:** The primary models (`Quote`, `HistoricalPrice`) defined in `docs/DA.md` will be used for database interaction (if data is persisted) and potentially as base models. They reside in `app/models/stock.py`.
*   **Pydantic Schemas:** Specific Pydantic models (`QuoteRead`, `HistoricalPriceRead` from `docs/DA.md`) will be used for API request validation (query parameters) and response serialization. These may inherit from SQLModel bases or be defined separately in `app/schemas/stock.py`.

## 6. API Endpoints

Endpoints will be grouped under a single router (`app/api/routers/stocks.py`).

### Stock Data API

*   **`GET /quotes/{symbol}`**
    *   **Description:** Retrieves the latest mock stock quote for the given symbol.
    *   **Path Parameters:** `symbol: str` (e.g., "AAPL", "MSFT")
    *   **Request Body:** None
    *   **Response(s):**
        *   `200 OK`: `QuoteRead` (defined in `DA.md`)
        *   `404 Not Found`: If the symbol is not recognized/supported.
    *   **Auth:** No

*   **`GET /historical/{symbol}`**
    *   **Description:** Retrieves mock historical price data (OHLCV) for the given symbol over a specified date range.
    *   **Path Parameters:** `symbol: str` (e.g., "AAPL", "MSFT")
    *   **Query Parameters:**
        *   `start_date: date` (Optional, defaults to 30 days ago)
        *   `end_date: date` (Optional, defaults to today)
    *   **Request Body:** None
    *   **Response(s):**
        *   `200 OK`: `List[HistoricalPriceRead]` (defined in `DA.md`)
        *   `404 Not Found`: If the symbol is not recognized/supported.
        *   `422 Unprocessable Entity`: If date parameters are invalid.
    *   **Auth:** No

*   **(Optional) `GET /symbols/`**
    *   **Description:** Retrieves a list of all available mock stock symbols.
    *   **Request Body:** None
    *   **Response(s):**
        *   `200 OK`: `List[str]` (e.g., `["AAPL", "MSFT", "GOOGL"]`)
    *   **Auth:** No

## 7. Error Handling Strategy

*   Standard HTTP status codes will be used.
*   FastAPI's default validation exceptions (`RequestValidationError`) will handle invalid request data (query params), returning `422 Unprocessable Entity`.
*   Custom `HTTPException` will be raised for specific errors:
    *   `404 Not Found`: For requests involving an unknown/unsupported stock symbol.
*   Generic server errors (`500 Internal Server Error`) will be returned for unexpected issues during data generation or processing.
*   Error responses will be in JSON format, including a `detail` field explaining the error.

## 8. Key Asynchronous Operations

*   All API endpoint functions (`/quotes/{symbol}`, `/historical/{symbol}`) will be defined using `async def`.
*   Database interactions (if implemented for reading/writing configuration or cached data) will use `aiosqlite` via SQLModel's async session management to avoid blocking the event loop.
*   Mock data generation logic itself might be synchronous but will be called within async endpoint functions. If generation becomes computationally intensive, it might be run in a separate thread pool using `fastapi.concurrency.run_in_threadpool`.

---
*Generated based on 05_senior_api_developer prompt and existing project documentation (PRD, SA, DA).*
