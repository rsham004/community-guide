# Implementation Plan: Mock Stock Market Data API (Prototype)

This plan outlines the development tasks required to build the Mock Stock Market Data API prototype based on the specifications in `product_requirements.md`, `SA.md`, `DA.md`, and `api.md`.

**Status Update (2025-04-21):** Phases 1-3 and initial documentation (Phase 4) are complete. Mock data generation was enhanced to seed the database on startup for more persistent and substantial data. Starting Phase 5 (Testing).

## Phase 1: Project Setup and Core Models (Completed)

- [x] Initialize FastAPI project repository and structure (`app/`, `tests/`, etc.) (Easy)
- [x] Configure basic environment variables (`.env`) for potential settings (Easy)
- [x] Add core dependencies to `requirements.txt`: FastAPI, Uvicorn, SQLModel, aiosqlite, python-dotenv (Easy)
- [x] Implement core SQLModel definitions (`Quote`, `HistoricalPrice`, `QuoteRead`, `HistoricalPriceRead`) in `app/models/stock.py` based on `DA.md` (Medium)
- [x] Setup basic SQLite database connection (`app/db/session.py`) using async session management (Medium)
- [x] Create basic FastAPI app instance in `app/main.py` (Easy)

## Phase 2: Mock Data Generation Logic (Completed & Enhanced)

- [x] Implement core logic for generating a single realistic mock `QuoteRead` object (`app/crud/crud_stock.py` or similar) (Medium) - *Now reads latest from DB*
- [x] Implement core logic for generating a list of realistic mock `HistoricalPriceRead` objects for a given symbol and date range (`app/crud/crud_stock.py` or similar) (Medium) - *Now reads from DB*
- [x] Define a static list or simple generation logic for available mock symbols (e.g., "AAPL", "MSFT", "GOOGL") (Easy)
- [x] Implement logic to seed initial historical data into the database on startup (`app/crud/crud_stock.py` and `app/main.py`) (Medium) - *Added Enhancement*
- [ ] (Optional) Implement logic to potentially seed/read initial data from a static file (e.g., CSV) instead of pure random generation (Medium) - *Skipped in favor of DB seeding*

## Phase 3: API Endpoint Implementation (Completed)

- [x] Create API router in `app/api/routers/stocks.py` (Easy)
- [x] Implement `GET /quotes/{symbol}` endpoint, calling mock quote generation logic (Medium) - *Updated for DB query*
- [x] Implement `GET /historical/{symbol}` endpoint with `start_date` and `end_date` query parameters, calling mock historical data generation logic (Medium) - *Updated for DB query*
- [x] Implement basic error handling within endpoints (e.g., raise `HTTPException` with 404 for unknown symbols) (Easy)
- [x] Implement validation for date query parameters in `/historical/{symbol}` (Easy)
- [x] (Optional) Implement `GET /symbols/` endpoint to return the list of available mock symbols (Easy)
- [x] Register the stock router with the main FastAPI app in `app/main.py` (Easy)
- [x] Implement dependency injection for database sessions (`app/api/deps.py`) (Easy) - *Added*

## Phase 4: Documentation & Initial Review (Partially Completed)

- [x] Verify FastAPI's automatic OpenAPI documentation (`/docs`, `/redoc`) is generated correctly and reflects the API structure (Easy)
- [x] Add descriptions, examples, and tags to endpoint definitions and models for better documentation clarity (Easy)
- [x] Create a basic `README.md` explaining how to set up, configure (env vars), run, and test the project (Easy) - *Updated for `uv`*
- [ ] Conduct initial code review for structure, clarity, and adherence to design docs (Medium) - *Pending*

## Phase 5: Testing and Refinement (In Progress)

- [x] **Unit Testing:**
    - [x] Write comprehensive unit tests for mock data generation functions (`app/crud/crud_stock.py`), covering edge cases and expected outputs (Medium)
    - [ ] Write unit tests for any utility or helper functions (Easy) - *None currently exist*
    - [ ] Aim for >80% unit test coverage for core logic modules (Medium) - *Pending measurement*
- [x] **Integration Testing:**
    - [x] Write integration tests using FastAPI's `TestClient` for the `GET /quotes/{symbol}` endpoint, testing valid symbols, invalid symbols (404), and response structure (Medium)
    - [x] Write integration tests for the `GET /historical/{symbol}` endpoint, testing valid symbols, invalid symbols (404), valid date ranges, invalid date parameters (422), default date ranges, and response structure (Complex)
    - [x] (Optional) Write integration tests for the `GET /symbols/` endpoint (Easy)
    - [x] Ensure tests cover successful responses (200 OK) and expected error responses (404, 422) (Medium)
    - [ ] Aim for >70% integration test coverage for API endpoints (Medium) - *Coverage not measured yet*
- [x] **Refinement:**
    - [x] Add `.gitignore` file (Easy)
    - [ ] Refactor code based on testing feedback and code review (Medium) - *Pending*
    - [ ] Perform final validation against PRD requirements (Easy) - *Pending*

## Final Project Structure (Target)

```
c:\repos\AI_Product_Dev\live-demos\2025_04_21_Sydney\
│   .env
│   .gitignore
│   README.md
│   requirements.txt
│
├── app/
│   │   __init__.py
│   │   main.py
│   │
│   ├── api/
│   │   │   __init__.py
│   │   │   deps.py
│   │   │
│   │   └── routers/
│   │       │   __init__.py
│   │       └── stocks.py
│   │
│   ├── core/
│   │   │   __init__.py
│   │   └── config.py
│   │
│   ├── crud/
│   │   │   __init__.py
│   │   └── crud_stock.py
│   │
│   ├── db/
│   │   │   __init__.py
│   │   └── session.py
│   │
│   ├── models/
│   │   │   __init__.py
│   │   └── stock.py
│   │
│   └── schemas/
│       │   __init__.py
│       └── stock.py
│
├── docs/
│   │   api.md
│   │   DA.md
│   │   plan.md
│   │   product_requirements.md
│   │   SA.md
│
├── prompts/
│   │   01_prompt_engineer.md
│   │   02_product_manager.md
│   │   03_solution_architect.md
│   │   04_data_architect.md
│   │   05_senior_api_developer.md
│   │   06_planner.md
│
└── tests/
    │   __init__.py
    │   conftest.py
    │
    ├── crud/
    │   │   __init__.py
    │   └── test_crud_stock.py
    │
    └── api/
        │   __init__.py
        └── test_stocks_api.py
```

---
*Generated based on 06_planner prompt and existing project documentation.*
